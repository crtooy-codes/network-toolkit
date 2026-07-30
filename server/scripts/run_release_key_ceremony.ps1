[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$PythonPath,

    [string]$RepositoryRoot = '',

    [string]$UsbRoot = 'D:\OpenLPS-Key-Vault',

    [string]$BackupVault = (
        Join-Path $env:USERPROFILE `
            'OneDrive\OpenLPS-Recovery\OpenLPS-Key-Vault.kdbx'
    ),

    [string]$ExpectedUsbSerial = ''
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$manifestPasswordName = 'OPENLPS_MANIFEST_KEY_PASSWORD'
$storePasswordName = 'OPENLPS_RELEASE_STORE_PASSWORD'
$keyPasswordName = 'OPENLPS_RELEASE_KEY_PASSWORD'
$minimumPasswordLength = 24

function Convert-SecureValue {
    param(
        [Parameter(Mandatory = $true)]
        [Security.SecureString]$Value
    )

    $pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($Value)
    try {
        return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer)
    }
    finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer)
    }
}

function Read-ConfirmedSecret {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Label
    )

    while ($true) {
        Write-Host ''
        Write-Host "Cole a senha de '$Label'. O texto ficara oculto."
        $firstSecure = Read-Host -AsSecureString
        Write-Host "Cole novamente a senha de '$Label' para confirmar."
        $secondSecure = Read-Host -AsSecureString

        $first = Convert-SecureValue -Value $firstSecure
        $second = Convert-SecureValue -Value $secondSecure
        $firstSecure.Dispose()
        $secondSecure.Dispose()

        if ($first -ne $second) {
            $first = $null
            $second = $null
            Write-Warning 'As duas entradas nao coincidem. Tente novamente.'
            continue
        }
        if ($first.Length -lt $minimumPasswordLength) {
            $first = $null
            $second = $null
            Write-Warning (
                "A senha precisa ter pelo menos " +
                "$minimumPasswordLength caracteres."
            )
            continue
        }
        if ($first.Contains("`r") -or $first.Contains("`n")) {
            $first = $null
            $second = $null
            Write-Warning 'A senha nao pode conter quebra de linha.'
            continue
        }

        $second = $null
        return $first
    }
}

function Get-ActiveDefaultRoutes {
    return @(
        Get-NetRoute -AddressFamily IPv4 -DestinationPrefix '0.0.0.0/0' `
            -ErrorAction SilentlyContinue |
            Where-Object {
                $_.State -eq 'Alive' -and
                $_.NextHop -ne '0.0.0.0'
            }
    )
}

function Assert-Offline {
    $defaultRoutes = @(Get-ActiveDefaultRoutes)
    if ($defaultRoutes.Count -gt 0) {
        throw (
            'O computador ainda possui rota ativa para a Internet. ' +
            'Desconecte Wi-Fi e cabo de rede antes de continuar.'
        )
    }
}

function Wait-ForOffline {
    while ($true) {
        $defaultRoutes = @(Get-ActiveDefaultRoutes)
        if ($defaultRoutes.Count -eq 0) {
            Write-Host ''
            Write-Host 'Modo offline confirmado.' -ForegroundColor Green
            return
        }

        Write-Host ''
        Write-Warning 'Ainda existe conexao de rede ativa:'
        foreach ($route in $defaultRoutes) {
            Write-Host (
                '  Interface: {0} | Proximo salto: {1}' -f
                $route.InterfaceAlias,
                $route.NextHop
            )
        }
        Read-Host (
            'Desconecte Wi-Fi/cabo e pressione ENTER para ' +
            'verificar novamente'
        ) | Out-Null
    }
}

function Assert-Usb {
    if (-not (Test-Path -LiteralPath $UsbRoot -PathType Container)) {
        throw "A pasta segura do pendrive nao existe: $UsbRoot"
    }
    $driveRoot = [System.IO.Path]::GetPathRoot(
        [System.IO.Path]::GetFullPath($UsbRoot)
    )
    $drive = [System.IO.DriveInfo]::new($driveRoot)
    if (-not $drive.IsReady -or
        $drive.DriveType -ne [System.IO.DriveType]::Removable) {
        throw "O destino nao e uma unidade removivel pronta: $driveRoot"
    }

    if ($ExpectedUsbSerial) {
        $letter = $driveRoot.Substring(0, 1)
        $partition = Get-Partition -DriveLetter $letter
        $disk = Get-Disk -Number $partition.DiskNumber
        if ($disk.SerialNumber.Trim() -ne $ExpectedUsbSerial) {
            throw 'O numero de serie do pendrive nao corresponde ao esperado.'
        }
    }
}

function Assert-VaultCopies {
    $primaryVault = Join-Path $UsbRoot 'OpenLPS-Key-Vault.kdbx'
    if (-not (Test-Path -LiteralPath $primaryVault -PathType Leaf)) {
        throw "Cofre mestre nao encontrado: $primaryVault"
    }
    if (-not (Test-Path -LiteralPath $BackupVault -PathType Leaf)) {
        throw "Copia de recuperacao nao encontrada: $BackupVault"
    }

    $primaryHash = (
        Get-FileHash -LiteralPath $primaryVault -Algorithm SHA256
    ).Hash
    $backupHash = (
        Get-FileHash -LiteralPath $BackupVault -Algorithm SHA256
    ).Hash
    if ($primaryHash -ne $backupHash) {
        throw (
            'O cofre do pendrive e a copia de recuperacao estao ' +
            'diferentes. Sincronize e valide antes da cerimonia.'
        )
    }
}

function Invoke-ReleaseTool {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments
    )

    & $PythonPath $releaseTool @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "A ferramenta de release falhou com codigo $LASTEXITCODE."
    }
}

function Write-Inventory {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Root
    )

    $inventoryPath = Join-Path $Root 'key-inventory.sha256'
    $lines = @(
        Get-ChildItem -LiteralPath $Root -Recurse -File |
            Where-Object { $_.FullName -ne $inventoryPath } |
            Sort-Object FullName |
            ForEach-Object {
                $relative = $_.FullName.Substring($Root.Length + 1)
                $hash = (
                    Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256
                ).Hash.ToLowerInvariant()
                "$hash  $relative"
            }
    )
    [System.IO.File]::WriteAllLines(
        $inventoryPath,
        $lines,
        [Text.UTF8Encoding]::new($false)
    )
}

if ([string]::IsNullOrWhiteSpace($RepositoryRoot)) {
    $RepositoryRoot = [System.IO.Path]::GetFullPath(
        (Join-Path $PSScriptRoot '..\..')
    )
}
else {
    $RepositoryRoot = [System.IO.Path]::GetFullPath($RepositoryRoot)
}
$releaseTool = Join-Path `
    $RepositoryRoot 'server\scripts\release_key_tool.py'
$templateManifest = Join-Path `
    $RepositoryRoot 'server\manifest.template.json'
$pendingRoot = Join-Path $UsbRoot 'Pending-Key-Import'
$apkOutput = Join-Path $pendingRoot 'apk'
$manifestOutput = Join-Path $pendingRoot 'manifest'

$storePassword = $null
$keyPassword = $null
$manifestPassword = $null

try {
    Write-Host 'OpenLPS - Cerimonia permanente de chaves'
    Write-Host 'Nenhuma senha sera mostrada ou gravada por este script.'

    Wait-ForOffline
    Assert-Usb
    Assert-VaultCopies

    if (-not (Test-Path -LiteralPath $PythonPath -PathType Leaf)) {
        throw "Python nao encontrado: $PythonPath"
    }
    if (-not (Test-Path -LiteralPath $releaseTool -PathType Leaf)) {
        throw "Ferramenta de release nao encontrada: $releaseTool"
    }
    if (-not (Test-Path -LiteralPath $templateManifest -PathType Leaf)) {
        throw "Manifesto de teste nao encontrado: $templateManifest"
    }
    if (Test-Path -LiteralPath $pendingRoot) {
        throw (
            'A pasta Pending-Key-Import ja existe. Nada foi sobrescrito: ' +
            $pendingRoot
        )
    }

    $storePassword = Read-ConfirmedSecret `
        -Label 'APK Keystore - Store Password'
    $keyPassword = Read-ConfirmedSecret `
        -Label 'APK Keystore - Key Password'
    $manifestPassword = Read-ConfirmedSecret `
        -Label 'Manifest Ed25519 Password'

    if ($storePassword -eq $keyPassword -or
        $storePassword -eq $manifestPassword -or
        $keyPassword -eq $manifestPassword) {
        throw 'As tres senhas precisam ser diferentes.'
    }

    Assert-Offline

    [Environment]::SetEnvironmentVariable(
        $storePasswordName,
        $storePassword,
        'Process'
    )
    [Environment]::SetEnvironmentVariable(
        $keyPasswordName,
        $keyPassword,
        'Process'
    )
    [Environment]::SetEnvironmentVariable(
        $manifestPasswordName,
        $manifestPassword,
        'Process'
    )
    $storePassword = $null
    $keyPassword = $null
    $manifestPassword = $null

    New-Item -ItemType Directory -Path $pendingRoot | Out-Null

    Invoke-ReleaseTool -Arguments @(
        'generate-apk',
        '--output-dir', $apkOutput
    )
    Invoke-ReleaseTool -Arguments @(
        'generate-manifest',
        '--output-dir', $manifestOutput
    )

    $testSignature = Join-Path $pendingRoot 'test-manifest.json.sig'
    Invoke-ReleaseTool -Arguments @(
        'sign-manifest',
        '--private-key',
        (Join-Path $manifestOutput 'manifest-ed25519-private.pem'),
        '--manifest', $templateManifest,
        '--signature', $testSignature
    )
    Invoke-ReleaseTool -Arguments @(
        'verify-manifest',
        '--public-key',
        (Join-Path $manifestOutput 'manifest-ed25519-public.pem'),
        '--manifest', $templateManifest,
        '--signature', $testSignature
    )
    Remove-Item -LiteralPath $testSignature -Force

    Write-Inventory -Root $pendingRoot

    Write-Host ''
    Write-Host 'CERIMONIA CONCLUIDA E VERIFICADA.' -ForegroundColor Green
    Write-Host "Material criptografado aguardando importacao em:"
    Write-Host $pendingRoot
    Write-Host ''
    Read-Host 'Pressione ENTER para fechar esta janela' | Out-Null
}
catch {
    Write-Host ''
    Write-Host 'CERIMONIA INTERROMPIDA.' -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host 'Nenhum arquivo existente foi sobrescrito.'
    Read-Host 'Pressione ENTER para fechar esta janela' | Out-Null
    exit 1
}
finally {
    foreach ($name in @(
        $storePasswordName,
        $keyPasswordName,
        $manifestPasswordName
    )) {
        [Environment]::SetEnvironmentVariable($name, $null, 'Process')
    }
    $storePassword = $null
    $keyPassword = $null
    $manifestPassword = $null
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
