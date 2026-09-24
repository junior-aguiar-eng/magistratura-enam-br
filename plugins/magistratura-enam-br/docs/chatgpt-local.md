# Conexão privada com o ChatGPT

O servidor permanece no computador e expõe `http://127.0.0.1:8765/mcp`. O Secure MCP Tunnel abre somente uma conexão HTTPS de saída para a OpenAI; não é necessário liberar porta de entrada no roteador ou firewall.

O ChatGPT não se conecta diretamente ao servidor MCP local. Sem túnel ativo, as operações do MCP — diagnóstico e busca do índice, sessões, histórico e card interativo — não ficam disponíveis nesse app. Uma conversa pode usar apenas as habilidades efetivamente carregadas na sua superfície; a instalação da skill global `$treinador-fgv-magistratura` no Codex não a instala no ChatGPT. O túnel é uma conexão privada para uso/teste em produtos compatíveis, não substitui o endpoint HTTPS público exigido para submissão pública do plugin.

Não há uma segunda versão de código para o ChatGPT: `.app.json` registra o app que usa este mesmo servidor MCP. Instalar uma versão no Codex não atualiza, por si só, a conexão nem o catálogo de ferramentas do app no ChatGPT; essa superfície exige atualização e teste próprios.

## Pré-requisitos locais

1. Crie `library-config.json` no diretório de dados do plugin com o caminho absoluto da biblioteca autorizada, `write_consent: true`, exclusões `.git`, `.estudo-juridico` e `node_modules`, e os limites documentados no schema.
2. Para validar o transporte HTTP diretamente, inicie o servidor com `uv run python -m mcp_server.server --config <arquivo> --transport streamable-http --host 127.0.0.1 --port 8765` e confirme o endpoint com um cliente MCP.
3. Para o túnel, prefira o transporte `stdio`: configure o comando do perfil para executar `uv run python -m mcp_server.server --config <arquivo> --transport stdio`. No Windows, o executável, o diretório do plugin e o arquivo de configuração devem ser passados com quoting íntegro; um caminho auxiliar sem espaços pode ser usado se a versão instalada do cliente não preservar esses argumentos.

## Túnel e registro privado

Crie o túnel em [Platform tunnel settings](https://platform.openai.com/settings/organization/tunnels), associe a organização pessoal e o workspace ChatGPT pertinente e use uma runtime API key exclusivamente no processo `tunnel-client`. A chave, o `tunnel_id`, perfis locais e identidade do túnel não pertencem ao repositório.

Inicialize e valide o perfil conforme a [documentação oficial do Secure MCP Tunnel](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels). No ChatGPT, habilite o modo desenvolvedor, crie o app privado usando a conexão Tunnel e copie o identificador técnico `plugin_asdk_app...` da URL. Esse identificador não é credencial; pode constar em `.app.json`, enquanto todo segredo continua local.

Depois de alterar ferramentas ou metadados, atualize o app no ChatGPT e teste em conversa nova. Com o túnel desligado, o ChatGPT deve falhar sem revelar caminhos ou dados; o fluxo local do Codex continua disponível por `stdio`.

Na primeira conversa após atualizar a conexão, peça `diagnosticar_acervo` e confira `library_root`, `index_path`, `index_status`, `document_count` e `generated_at`. `missing` ou `invalid` não autoriza reparo automático; `available` atesta que o manifesto foi lido, não que cada Markdown atual tenha o mesmo hash da última indexação. Teste `buscar_acervo` somente após confirmar o índice. Para a questão interativa, crie uma sessão de teste, renderize-a e confira que o gabarito só aparece após a tentativa. Registre separadamente descoberta de ferramentas, operação textual e renderização visual.

## Inicialização automática no Windows

Depois de validar manualmente o fluxo, execute `scripts/install_local_service.ps1` informando os caminhos do `tunnel-client` e do perfil, além de `-Confirm`. O instalador registra uma tarefa de logon no Agendador de Tarefas para o usuário atual, sem elevação administrativa, mantém os arquivos operacionais em `.runtime/startup` (ignorado pelo Git) e exige que `CONTROL_PLANE_API_KEY` já esteja definida no ambiente do usuário. A chave não é copiada para arquivo ou registro. Instalações anteriores baseadas em `HKCU\...\Run` são migradas automaticamente.

O script inicia imediatamente o mesmo runner que será acionado no próximo logon. Para remover a inicialização, execute `scripts/uninstall_local_service.ps1 -Confirm`. A remoção apaga apenas a entrada de inicialização e seus arquivos auxiliares; biblioteca, índice, questões, tentativas e configuração da biblioteca permanecem intactos.

O runner é um supervisor persistente e idempotente, iniciado pelo serviço do Agendador de Tarefas para não depender do shell que executou o instalador. Um mutex impede supervisores duplicados; se o túnel já estiver ativo, o supervisor acompanha essa instância e, se ela encerrar, inicia outra após cinco segundos. O Agendador mantém uma política adicional de reinício do supervisor em caso de falha. Fechar ou reiniciar uma conversa do ChatGPT não afeta esse processo. O PID do supervisor fica em `supervisor.pid`, o PID do túnel em `tunnel.pid` e os eventos de recuperação em `supervisor.log`. O stdout e o stderr do cliente ficam em `.runtime/startup/tunnel-client.stdout.log` e `tunnel-client.stderr.log`, respectivamente. A cópia local do perfil também fica nessa pasta ignorada pelo Git, visível ao contexto real do Agendador.

Para confirmar que o cliente está operacional antes de testar no ChatGPT, consulte `/readyz` na porta de health configurada no perfil (8080 por padrão) e obtenha `ready`; se a resposta remota ainda disser que o cliente não foi visto, confira também esses logs e a associação do `tunnel_id`. Não execute uma segunda instância manual com a mesma porta de health. A desinstalação encerra primeiro o supervisor e depois o túnel, sem apagar biblioteca ou histórico.

## Verificação pontual do índice no Windows

Após a primeira indexação explícita, `scripts/install_index_sync.ps1` pode registrar uma tarefa independente do túnel, no escopo do usuário. Ela executa `python -m mcp_server.index_sync` no login e a cada dez minutos, sem processo de indexação residente. Cada execução confere os hashes dos Markdown elegíveis, reaproveita as entradas inalteradas e só substitui atomicamente `index.json` quando houve inclusão, alteração ou remoção. A busca MCP permanece somente leitura. Como não há monitor contínuo, uma mudança pode levar até dez minutos para aparecer; o login também dispara uma verificação. Não há chamada à API para essa checagem local.

Com PowerShell aberto na pasta do plugin, informe os caminhos reais de `uv` e do arquivo de configuração local:

```powershell
.\scripts\install_index_sync.ps1 -UvPath (Get-Command uv).Source -ConfigPath 'C:\caminho\library-config.json' -Confirm
```

O resultado da última execução fica em `.runtime/index-sync/last-run.json`. `missing` e `invalid` são falhas explícitas: a tarefa não cria nem repara silenciosamente o índice; use `indexar_acervo` com confirmação após examinar a causa. Para remover apenas essa verificação, execute `scripts/uninstall_index_sync.ps1 -Confirm`. O túnel, a biblioteca, o índice e o histórico são preservados.
