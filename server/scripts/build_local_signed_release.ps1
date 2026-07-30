[CmdletBinding()]
param(
    [string]$RepositoryRoot = '',

    [Parameter(Mandatory = $true)]
    [string]$KeystorePath,

    [Parameter(Mandatory = $true)]
    [string]$JavaHome,

    [Parameter(Mandatory = $true)]
    [string]$AndroidSdk,

    [string]$KeyAlias = 'openlps-release',

    [string]$ExpectedCertificateSha256 = (
        '50fc73ceb72d4c446ebac3c24f30b45f37772e34b1fe734db0d9f13e1ac92dc9'
    ),

    [string]$ResultPath = '',

    [switch]$Pause
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$storePasswordName = 'OPENLPS_RELEASE_STORE_PASSWORD'
$keyPasswordName = 'OPENLPS_RELEASE_KEY_PASSWORD'
$storeFileName = 'OPENLPS_RELEASE_STORE_FILE'
$keyAliasName = 'OPENLPS_RELEASE_KEY_ALIAS'

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

function Read-Secret {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Label
    )

    Write-Host ''
    Write-Host "Cole a senha de '$Label'. O texto ficara oculto."
    $secureValue = Read-Host -AsSecureString
    try {
        return Convert-SecureValue -Value $secureValue
    }
    finally {
        $secureValue.Dispose()
    }
}

function Get-Tool {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Directory,

        [Parameter(Mandatory = $true)]
        [string]$Name
    )

    $path = Join-Path $Directory $Name
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Ferramenta nao encontrada: $path"
    }
    return $path
}

if ([string]::IsNullOrWhiteSpace($RepositoryRoot)) {
    $RepositoryRoot = [System.IO.Path]::GetFullPath(
        (Join-Path $PSScriptRoot '..\..')
    )
}
else {
    $RepositoryRoot = [System.IO.Path]::GetFullPath($RepositoryRoot)
}
if ([string]::IsNullOrWhiteSpace($ResultPath)) {
    $ResultPath = Join-Path $env:TEMP 'openlps-signed-release-result.json'
}
$ResultPath = [System.IO.Path]::GetFullPath($ResultPath)

$resolvedKeystore = (
    Resolve-Path -LiteralPath $KeystorePath -ErrorAction Stop
).Path
$repositoryPrefix = $RepositoryRoot.TrimEnd('\') + '\'
if ($resolvedKeystore.StartsWith(
        $repositoryPrefix,
        [StringComparison]::OrdinalIgnoreCase
    )) {
    throw 'O keystore privado nao pode ficar dentro do repositorio.'
}

$gradle = Get-Tool -Directory $RepositoryRoot -Name 'gradlew.bat'
$keytool = Get-Tool -Directory (Join-Path $JavaHome 'bin') -Name 'keytool.exe'
$buildToolsRoot = Join-Path $AndroidSdk 'build-tools'
$buildTools = Get-ChildItem -LiteralPath $buildToolsRoot -Directory |
    Sort-Object { [version]$_.Name } -Descending |
    Select-Object -First 1
if (-not $buildTools) {
    throw "Android Build Tools nao encontrado em: $buildToolsRoot"
}
$apksigner = Get-Tool -Directory $buildTools.FullName -Name 'apksigner.bat'
$aapt = Get-Tool -Directory $buildTools.FullName -Name 'aapt.exe'

$storePassword = $null
$keyPassword = $null
$oldJavaHome = $env:JAVA_HOME
$oldAndroidHome = $env:ANDROID_HOME
$oldAndroidSdkRoot = $env:ANDROID_SDK_ROOT
$scriptExitCode = 0

try {
    Write-Host 'OpenLPS - Build local assinado'
    Write-Host 'Nenhuma senha sera mostrada ou gravada por este script.'
    Write-Host "Keystore: $resolvedKeystore"

    $storePassword = Read-Secret -Label 'APK Keystore - Store Password'
    $keyPassword = Read-Secret -Label 'APK Keystore - Key Password'
    if ([string]::IsNullOrEmpty($storePassword) -or
        [string]::IsNullOrEmpty($keyPassword)) {
        throw 'As duas senhas sao obrigatorias.'
    }
    if ($storePassword -eq $keyPassword) {
        throw 'As senhas do cofre e da chave precisam ser diferentes.'
    }

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
        $storeFileName,
        $resolvedKeystore,
        'Process'
    )
    [Environment]::SetEnvironmentVariable(
        $keyAliasName,
        $KeyAlias,
        'Process'
    )
    $storePassword = $null
    $keyPassword = $null

    $nativeErrorPreference = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        $certificateOutput = & $keytool `
            -list `
            -v `
            -keystore $resolvedKeystore `
            -storepass:env $storePasswordName `
            -alias $KeyAlias 2>&1 | Out-String
        $certificateExitCode = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $nativeErrorPreference
    }
    if ($certificateExitCode -ne 0) {
        throw "O keystore nao pode ser validado.`n$certificateOutput"
    }
    $certificateSha256 = ''
    if ($certificateOutput -match 'SHA256:\s*([0-9A-Fa-f:]+)') {
        $certificateSha256 = $Matches[1].Replace(':', '').ToLowerInvariant()
    }
    if ($certificateSha256 -ne $ExpectedCertificateSha256.ToLowerInvariant()) {
        throw (
            'A impressao digital do certificado nao corresponde ao ' +
            'registro publico permanente. Observada: ' +
            "$certificateSha256. Esperada: " +
            "$($ExpectedCertificateSha256.ToLowerInvariant())."
        )
    }

    $env:JAVA_HOME = $JavaHome
    $env:ANDROID_HOME = $AndroidSdk
    $env:ANDROID_SDK_ROOT = $AndroidSdk

    $releaseDirectory = [System.IO.Path]::GetFullPath(
        (Join-Path $RepositoryRoot 'app\build\outputs\apk\release')
    )
    $expectedReleaseDirectory = (
        $RepositoryRoot.TrimEnd('\') +
        '\app\build\outputs\apk\release'
    )
    if (-not $releaseDirectory.Equals(
            $expectedReleaseDirectory,
            [StringComparison]::OrdinalIgnoreCase
        )) {
        throw 'Diretorio de saida release inesperado.'
    }
    if (Test-Path -LiteralPath $releaseDirectory) {
        Remove-Item -LiteralPath $releaseDirectory -Recurse -Force
    }

    Push-Location $RepositoryRoot
    try {
        $nativeErrorPreference = $ErrorActionPreference
        $ErrorActionPreference = 'Continue'
        try {
            & $gradle `
                ':app:assembleRelease' `
                '--no-daemon' `
                '--no-configuration-cache' `
                '--console=plain'
            $gradleExitCode = $LASTEXITCODE
        }
        finally {
            $ErrorActionPreference = $nativeErrorPreference
        }
        if ($gradleExitCode -ne 0) {
            throw "O Gradle falhou com codigo $gradleExitCode."
        }
    }
    finally {
        Pop-Location
    }

    $apk = Get-ChildItem -LiteralPath $releaseDirectory -File -Filter '*.apk' |
        Where-Object { $_.Name -notmatch 'unsigned' } |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1
    if (-not $apk) {
        throw 'O APK release assinado nao foi encontrado.'
    }

    $nativeErrorPreference = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        $verifyOutput = & $apksigner `
            verify `
            --verbose `
            --print-certs `
            $apk.FullName 2>&1 | Out-String
        $verifyExitCode = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $nativeErrorPreference
    }
    if ($verifyExitCode -ne 0) {
        throw "A assinatura do APK nao foi validada.`n$verifyOutput"
    }
    $apkCertificateSha256 = ''
    if ($verifyOutput -match (
            'Signer #1 certificate SHA-256 digest:\s*([0-9A-Fa-f]+)'
        )) {
        $apkCertificateSha256 = $Matches[1].ToLowerInvariant()
    }
    if ($apkCertificateSha256 -ne
        $ExpectedCertificateSha256.ToLowerInvariant()) {
        throw 'O APK foi assinado com um certificado inesperado.'
    }

    $badging = & $aapt dump badging $apk.FullName | Select-Object -First 1
    $apkHash = (
        Get-FileHash -LiteralPath $apk.FullName -Algorithm SHA256
    ).Hash

    Write-Host ''
    Write-Host 'BUILD ASSINADO E VERIFICADO.' -ForegroundColor Green
    Write-Host "APK: $($apk.FullName)"
    Write-Host "SHA-256: $apkHash"
    Write-Host "Certificado SHA-256: $apkCertificateSha256"
    Write-Host "Pacote: $badging"

    $result = [ordered]@{
        Status = 'success'
        ApkPath = $apk.FullName
        ApkSHA256 = $apkHash
        CertificateSHA256 = $apkCertificateSha256
        PackageBadging = [string]$badging
    } | ConvertTo-Json
    [System.IO.File]::WriteAllText(
        $ResultPath,
        $result,
        [Text.UTF8Encoding]::new($false)
    )
}
catch {
    $scriptExitCode = 1
    $errorMessage = $_.Exception.Message
    $result = [ordered]@{
        Status = 'failed'
        Error = $errorMessage
    } | ConvertTo-Json
    [System.IO.File]::WriteAllText(
        $ResultPath,
        $result,
        [Text.UTF8Encoding]::new($false)
    )

    Write-Host ''
    Write-Host 'BUILD ASSINADO FALHOU.' -ForegroundColor Red
    Write-Host $errorMessage -ForegroundColor Red
}
finally {
    foreach ($name in @(
        $storePasswordName,
        $keyPasswordName,
        $storeFileName,
        $keyAliasName
    )) {
        [Environment]::SetEnvironmentVariable($name, $null, 'Process')
    }
    $env:JAVA_HOME = $oldJavaHome
    $env:ANDROID_HOME = $oldAndroidHome
    $env:ANDROID_SDK_ROOT = $oldAndroidSdkRoot
    $storePassword = $null
    $keyPassword = $null
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()

    if ($Pause) {
        Write-Host ''
        Read-Host 'Pressione ENTER para fechar esta janela' | Out-Null
    }
}

exit $scriptExitCode
