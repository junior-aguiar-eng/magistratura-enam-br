# Instalação

## Requisitos

- Codex com suporte a plugins;
- Git, autenticação e autorização de leitura no repositório privado para a instalação pelo marketplace Git;
- `uv` no `PATH` para executar o servidor MCP local de questões (o projeto fixa Python 3.14 em `.python-version`);
- uma nova tarefa do Codex após a instalação.

## Versão estável

```powershell
codex plugin marketplace add junior-aguiar-eng/magistratura-enam-br --ref v0.7.2
codex plugin add magistratura-enam-br@magistratura-enam-br
```

A instalação é local por computador. Ela não é sincronizada automaticamente entre máquinas ou usuários.

A versão instalada pelo comando acima é o snapshot estável `v0.7.2`. A candidata `0.7.3` da branch `codex/organizacao-qualidade-plugin`, incluindo `diagnosticar_acervo`, não entra nessa instalação por tag; seu piloto local requer instalar a branch explicitamente. Ela ainda não é uma release estável.

No Windows, também é possível instalar a partir de um ZIP descompactado em pasta permanente com `.\INSTALAR.ps1` na raiz do repositório. Use `.\INSTALAR.ps1 -InstalarDependencias` para preparar as dependências Python do plugin. A conexão privada do ChatGPT e a inicialização automática do túnel são opcionais e exigem configuração separada.

O Codex usa a configuração MCP local por `stdio`. O ChatGPT exige conexão remota; para este servidor privado, o [Secure MCP Tunnel](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels) fornece essa conexão sem abrir porta de entrada. A instalação do plugin no Codex não demonstra que o app do ChatGPT esteja conectado, nem instala automaticamente nele uma habilidade global avulsa do Codex.

## Atualização

Cada release deve ser consumida por tag explícita. Atualize o snapshot do marketplace para a nova tag, reinstale o plugin e abra uma nova tarefa para carregar a nova versão.

!!! warning "Acesso privado"
    Uma GitHub Release não torna público um repositório privado. Somente contas autorizadas conseguem obter o marketplace e instalar o plugin.
