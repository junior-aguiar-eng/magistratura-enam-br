# Instalação

## Requisitos

- Codex com suporte a plugins;
- Git para a instalação pelo marketplace Git público;
- `uv` no `PATH` para executar o servidor MCP local de questões (o projeto fixa Python 3.14 em `.python-version`);
- uma nova tarefa do Codex após a instalação.

## Versão estável

```powershell
codex plugin marketplace add junior-aguiar-eng/magistratura-enam-br --ref v0.7.5
codex plugin add magistratura-enam-br@magistratura-enam-br
```

A instalação é local por computador. Ela não é sincronizada automaticamente entre máquinas ou usuários.

A versão instalada pelo comando acima é `v0.7.5`, incluindo diagnóstico do acervo, sincronização opcional do índice e correções da auditoria de questões, eventos e widget. A instalação não ativa tarefas agendadas nem indexa o acervo automaticamente.

No Windows, também é possível instalar a partir de um ZIP descompactado em pasta permanente com `.\INSTALAR.ps1` na raiz do repositório. Use `.\INSTALAR.ps1 -InstalarDependencias` para preparar as dependências Python do plugin. A conexão privada do ChatGPT e a inicialização automática do túnel são opcionais e exigem configuração separada.

O Codex usa a configuração MCP local por `stdio`. O ChatGPT exige conexão remota; para este servidor privado, o [Secure MCP Tunnel](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels) fornece essa conexão sem abrir porta de entrada. A instalação do plugin no Codex não demonstra que o app do ChatGPT esteja conectado, nem instala automaticamente nele uma habilidade global avulsa do Codex.

## Atualização

Cada release deve ser consumida por tag explícita. Atualize o snapshot do marketplace para a nova tag, reinstale o plugin e abra uma nova tarefa para carregar a nova versão.

O repositório e suas releases são públicos. O acervo, os registros de estudo e as credenciais permanecem locais e não fazem parte da distribuição.

## Candidata dos incrementos MCP e pedagogia

As tasks 1–8 foram executadas localmente na branch
`codex/incrementos-mcp-calibracao`. A versão 0.8.0 é proposta: os comandos
de instalação estável acima continuam consumindo v0.7.5. Validar stdio
em uma sessão efêmera da CLI não substitui reinstalação do plugin nem
homologação do card no ChatGPT.

Para homologar a candidata no ChatGPT, é necessário identificar sua
conexão MCP, cliente/capacidades e versão efetivamente servida. O fullscreen
depende do modo concedido pelo host; recusa deve manter o fluxo utilizável.
Até essa verificação, fullscreen, reconstrução visual e ações do card
permanecem pendentes em host real. O ensaio com material anexado usa
instruções fornecidas manualmente, sem provar instalação da candidata.

Depois de uma publicação autorizada, compare o cache instalado com a árvore
da tag e abra tarefa nova. Para rollback, retorne ao snapshot v0.7.5 do
marketplace e reinstale, preservando acervo/configuração/registros locais.
Não é necessário apagar dados de estudo para trocar a versão do código.
