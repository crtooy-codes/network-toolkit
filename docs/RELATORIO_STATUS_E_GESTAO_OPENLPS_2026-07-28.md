# Relatório de situação e gestão do OpenLPS

Data da verificação: 2026-07-28  
Projeto: OpenLPS Network Toolkit  
Repositório: https://github.com/crtooy-codes/network-toolkit  
Pacote Android: `com.openlps.networktoolkit`  
Versão atual de desenvolvimento: `5.0.0-dev.2` (`versionCode 501`)  
Commit validado: `879c67621cb047547b5a861b3f8bc020da59d8d9`

## 1. Resumo executivo

O OpenLPS é uma continuação comunitária de código aberto baseada no
StrykerOSS. O projeto preserva o motor root/chroot, os créditos históricos, a
licença GPL-3.0 e as licenças de terceiros, enquanto recebe identidade,
interface, caminhos, documentação, testes e infraestrutura próprios.

O responsável atual informou possuir autorização do desenvolvedor original
para continuar o trabalho. É recomendável manter uma cópia escrita dessa
autorização junto aos documentos administrativos do projeto. Além disso, a
GPL-3.0 permite estudar, modificar e redistribuir o código desde que suas
condições, avisos e disponibilização do código-fonte correspondente sejam
respeitados. Este relatório registra a situação técnica; não substitui parecer
jurídico.

O aplicativo corrigido foi compilado, reinstalado e testado em um Galaxy S10
com Android 15/LineageOS e root Magisk. O CI do GitHub também compilou o commit
publicado com sucesso.

## 2. O que foi feito até agora

- Criação do pacote independente `com.openlps.networktoolkit`
- Identidade OpenLPS e preservação dos créditos do StrykerOSS
- Chroot próprio em `/data/local/openlps/release`
- Armazenamento compartilhado em `/storage/emulated/0/OpenLPS`
- Interface inicial e navegação em português do Brasil
- Recursos iniciais em inglês, português-BR, espanhol, russo e chinês
- Aviso e consentimento para uso somente autorizado
- Estrutura de atualização com manifesto, SHA-256 e assinatura Ed25519
- Restrição de downloads aos Releases do repositório oficial
- GitHub Actions para build Android
- GitHub Pages para o serviço estático de atualização
- Backup verificado antes da troca do APK no aparelho de laboratório
- Teste de telas, root, chroot, montagens e ferramentas-base
- Correção do travamento do Terminal causado pelo antigo caminho do pacote
- Correção da tela presa em `Initializing…`
- Correção da sub-rede `0.0.0.0` no Android moderno
- Atualização dos links públicos e textos promocionais
- Restauração seletiva dos bancos históricos do aplicativo
- Publicação do commit testado na branch `main`

O relatório detalhado do aparelho está em
`docs/DEVICE_SMOKE_TEST_SM-G973F_2026-07-28.md`.

## 3. Situação atual do aplicativo

| Item | Situação |
|---|---|
| Build local | Aprovado |
| GitHub Actions | Aprovado no commit `879c676` |
| Instalação no Galaxy S10 | Aprovada |
| Root e Magisk | Funcionando |
| Alpine chroot | Funcionando |
| Terminal | Funcionando sem o travamento anterior |
| Montagens `/dev`, `/proc`, `/sys`, `/system` e armazenamento | Aprovadas |
| Nmap, Python, curl, Aircrack-ng e ferramentas-base | Presentes |
| Hydra, Nuclei, Metasploit e SearchSploit | Ainda não instalados |
| Assinatura atual do APK instalado | Debug local, não é assinatura pública |
| Artefato do CI | Debug temporário por 14 dias; não é uma Release |
| Primeira versão pública | Ainda não criada |
| Atualização automática | Implementada em código, mas desativada |

O APK atual é uma versão de desenvolvimento. Ele não deve ser distribuído como
versão pública definitiva porque usa assinatura debug e ainda existem tarefas
de release, compatibilidade e segurança operacional.

## 4. Como os “servidores” funcionam

Não há hoje um computador pessoal, VPS, banco de dados ou processo Java que
precise permanecer ligado. A infraestrutura é administrada pelo GitHub:

```text
Alteração no código
        |
        v
GitHub: branch main
        |
        +--> Android CI --> compila e testa --> artefato debug por 14 dias
        |
        +--> GitHub Pages --> site, health check, schema e manifesto pequeno
        |
        `--> GitHub Releases --> APK, chroot e outros arquivos grandes
                                  (ainda sem release publicado)

Aplicativo instalado
        |
        `--> consulta manifesto assinado a cada aproximadamente 12 horas
             --> avisa o usuário
             --> baixa APK
             --> confere tamanho e SHA-256
             --> pede confirmação do Android para instalar
```

### Estado verificado ao vivo

- Site: `https://crtooy-codes.github.io/network-toolkit/` — online
- Health check:
  `https://crtooy-codes.github.io/network-toolkit/health.json` — online
- Schema:
  `https://crtooy-codes.github.io/network-toolkit/schema/manifest-v1.schema.json`
  — online
- Repositório — público, branch padrão `main`, licença GPL-3.0
- Releases — nenhuma versão publicada
- `v1/manifest.json` — ainda não publicado
- `v1/manifest.json.sig` — ainda não publicado
- Estado do serviço — `pre-release`
- Atualizações remotas — desabilitadas

Esse estado é intencional e seguro: sem chave pública fixada no aplicativo e
sem manifesto assinado, o aplicativo rejeita atualizações remotas.

## 5. O que pode ser administrado

### Mudanças que exigem um APK novo

- Novas funções e telas
- Correção de bugs
- Mudança de permissões Android
- Mudança do comportamento root/chroot
- Atualização de scripts empacotados
- Mudança da chave pública do manifesto
- Atualização de bibliotecas e SDK Android

Essas mudanças são feitas no código, passam por testes e recebem um
`versionCode` maior antes da publicação.

### Mudanças de servidor que não exigem APK novo

Depois que a atualização assinada for ativada:

- Notícia exibida dentro do aplicativo
- Notificação administrativa
- Changelog
- Endereço e hash de uma nova versão do APK
- Endereço e hash de uma nova versão do chroot
- Marcação de atualização normal ou obrigatória

Esses dados ficam no manifesto assinado. Mesmo sendo uma mudança “do
servidor”, ela precisa ser assinada com a chave privada Ed25519 offline. Isso
impede que uma invasão simples ao site envie um APK adulterado aos usuários.

### Mudanças apenas no site

Arquivos dentro de `server/public/` são publicados automaticamente no GitHub
Pages quando chegam à branch `main`. Isso serve para página de status,
documentação pública e arquivos pequenos.

## 6. Processo para criar uma nova atualização

1. Criar uma branch com nome descritivo, por exemplo
   `feature/nova-funcao` ou `fix/correcao-terminal`.
2. Alterar o código e os recursos necessários.
3. Aumentar em `app/build.gradle`:
   - `versionCode`: sempre maior que todas as versões anteriores;
   - `versionName`: nome legível, por exemplo `5.0.0-dev.3` ou `5.0.0-rc.1`.
4. Executar build, testes, lint e testes no aparelho de laboratório.
5. Revisar o diff e confirmar que não existem senhas, chaves ou dados
   pessoais.
6. Fazer merge na `main` somente depois do CI aprovado.
7. Gerar o APK release usando sempre a mesma chave de assinatura OpenLPS.
8. Conferir certificado, tamanho e SHA-256 do APK.
9. Criar uma tag e um GitHub Release, inicialmente como pré-lançamento.
10. Anexar o APK release e, quando aplicável, o chroot ou módulo.
11. Gerar `manifest.json` com versão, URLs, tamanhos, hashes e changelog.
12. Validar o manifesto contra o schema.
13. Assinar os bytes exatos do manifesto com a chave Ed25519 offline.
14. Publicar em `server/public/v1/`:
    - `manifest.json`
    - `manifest.json.sig`
15. Aguardar o GitHub Pages concluir e verificar os dois arquivos ao vivo.
16. Testar a atualização em um aparelho de laboratório já instalado.
17. Somente então anunciar a versão ao público.

O usuário final receberá a notificação quando o aplicativo consultar o
manifesto. O Android ainda solicitará permissão para instalar aplicativos
dessa fonte e mostrará sua tela normal de confirmação.

## 7. Preparação obrigatória para a primeira versão pública

Existem duas chaves diferentes:

### Chave de assinatura do APK

- Mantém a identidade Android do aplicativo
- Precisa ser a mesma em todas as futuras versões
- Se for perdida, os usuários não poderão atualizar o app instalado
- Deve possuir pelo menos duas cópias offline, criptografadas e testadas

### Chave Ed25519 do manifesto

- Assina o arquivo que anuncia APK, chroot, notícias e notificações
- A chave privada fica offline
- Somente a chave pública de 32 bytes entra no código do aplicativo
- Deve ser diferente da chave do APK

O aplicativo atual contém
`MANIFEST_PUBLIC_KEY_BASE64 = ""`. Portanto, ele rejeita qualquer manifesto.
A primeira versão pública precisa fixar a chave pública correta no código e ser
distribuída como instalação inicial confiável. As atualizações automáticas
começam a funcionar da segunda versão pública em diante.

O APK instalado no aparelho de laboratório usa assinatura debug. A primeira
versão release terá outra assinatura e exigirá uma reinstalação única nesse
aparelho, com backup prévio. Depois disso, todas as versões públicas deverão
usar a mesma chave release.

## 8. Como agir em caso de problema

### Uma atualização foi publicada com bug

Não reduzir o `versionCode`. Corrigir o código e publicar uma nova versão com
`versionCode` maior. Android normalmente não aceita downgrade como atualização.

### O manifesto está errado

Remover temporariamente os dois arquivos do manifesto faz o cliente falhar de
forma segura e parar de oferecer a atualização. Em seguida, publicar um novo
manifesto válido e assinado.

### A chave do APK foi perdida

Não é possível atualizar instalações existentes com outra chave. Será
necessário criar outro pacote ou solicitar reinstalação manual. Por isso o
backup offline da chave é uma tarefa crítica.

### A chave do manifesto foi perdida

Uma nova chave pode ser criada, mas os aplicativos antigos não confiarão nela.
Será necessário distribuir manualmente, ainda com a mesma chave de APK, uma
versão que fixe a nova chave pública.

### O GitHub Pages ficou fora do ar

O aplicativo continua funcionando offline com o chroot já instalado. Ele
simplesmente não receberá notícias ou atualização enquanto o serviço estiver
indisponível.

## 9. O que ainda falta

### Prioridade crítica — antes da primeira versão pública

1. Criar e guardar a chave release do APK.
2. Criar a chave Ed25519 do manifesto e fixar somente a chave pública no app.
3. Criar um processo reproduzível de release assinado.
4. Publicar e validar o primeiro APK release como pré-lançamento.
5. Substituir o fallback atual do chroot upstream por um artefato controlado
   pelo projeto, com tamanho e SHA-256 obrigatórios. O fallback atual aceita o
   download sem hash fixado quando não existe manifesto, o que precisa ser
   eliminado antes da versão pública.
6. Testar instalação e atualização com a mesma assinatura release.
7. Remover caminhos privados fixos restantes e usar `Context` quando possível.
8. Corrigir branding antigo ainda presente, como notícias padrão e nomes
   internos `stryker`.
9. Limpar o README, que ainda mistura documentação OpenLPS e StrykerOSS.
10. Parar de depender das chaves debug variáveis do computador/CI; usuários
    públicos devem receber somente APKs assinados pela chave release oficial.

### Prioridade alta

1. Aumentar a cobertura de testes; hoje há poucos testes automatizados.
2. Criar testes de manifesto adulterado, hash incorreto, arquivo truncado,
   falta de espaço, retomada e assinatura inválida.
3. Testar Android 7, Android 12 e Android 15.
4. Testar os módulos opcionais Hydra, Nuclei, Metasploit, SearchSploit e
   ExploitDB em laboratório.
5. Reduzir o débito de lint atualmente não bloqueante.
6. Planejar atualização do `targetSdk`, hoje em 28, sem quebrar root,
   armazenamento e instalação de pacotes.
7. Criar `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, changelog e
   avisos de terceiros mais claros.
8. Proteger a branch `main`, exigir CI aprovado e ativar autenticação de dois
   fatores nas contas mantenedoras.
9. Definir schemas estritos para cada notícia e notificação e restringir URLs
   externas permitidas.

### Evolução posterior

1. Migrar gradualmente namespace e identificadores internos para OpenLPS.
2. Modernizar telas para Material 3/Kotlin/Compose sem reescrever o motor de
   uma vez.
3. Criar canal estável e canal de pré-lançamento.
4. Avaliar distribuição adicional, mantendo GitHub Releases como fonte
   oficial.
5. Criar uma matriz pública de aparelhos, kernels e adaptadores compatíveis.

## 10. Rotina de gestão recomendada

### Toda alteração

- Trabalhar em branch separada
- Descrever o objetivo e o risco
- Testar antes de merge
- Exigir CI aprovado
- Atualizar changelog/documentação

### Toda versão

- Aumentar `versionCode`
- Usar a chave release oficial
- Verificar certificado, SHA-256 e tamanho
- Testar instalação e atualização
- Criar Release e manifesto assinado
- Verificar Pages e aparelho de laboratório

### Todo mês

- Revisar dependências e alertas do GitHub
- Conferir expiração/estado dos workflows
- Validar acesso às cópias das chaves sem expô-las
- Testar o health check e uma atualização em ambiente de laboratório
- Revisar issues, contribuições e documentação

## 11. Regra prática de administração

Não se altera uma função importante diretamente no “servidor”. A função é
alterada no código do aplicativo, testada e publicada em um APK com versão
maior. O servidor apenas informa, de forma assinada, qual versão oficial deve
ser baixada e pode entregar notícias, notificações e arquivos do núcleo.

Essa separação mantém o OpenLPS aberto para contribuições, mas impede que
qualquer pessoa que edite uma página pública controle automaticamente os
aparelhos dos usuários.
