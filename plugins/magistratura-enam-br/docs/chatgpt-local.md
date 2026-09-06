# Conexão privada com o ChatGPT

O servidor permanece no computador e expõe `http://127.0.0.1:8765/mcp`. O Secure MCP Tunnel abre somente uma conexão HTTPS de saída para a OpenAI; não é necessário liberar porta de entrada no roteador ou firewall.

## Pré-requisitos locais

1. Crie `library-config.json` no diretório de dados do plugin com o caminho absoluto da biblioteca autorizada, `write_consent: true`, exclusões `.git`, `.estudo-juridico` e `node_modules`, e os limites documentados no schema.
2. Para validar o transporte HTTP diretamente, inicie o servidor com `uv run python -m mcp_server.server --config <arquivo> --transport streamable-http --host 127.0.0.1 --port 8765` e confirme o endpoint com um cliente MCP.
3. Para o túnel, prefira o transporte `stdio`: configure o comando do perfil para executar `uv run python -m mcp_server.server --config <arquivo> --transport stdio`. No Windows, o executável, o diretório do plugin e o arquivo de configuração devem ser passados com quoting íntegro; um caminho auxiliar sem espaços pode ser usado se a versão instalada do cliente não preservar esses argumentos.

## Túnel e registro privado

Crie o túnel em [Platform tunnel settings](https://platform.openai.com/settings/organization/tunnels), associe a organização pessoal e o workspace ChatGPT pertinente e use uma runtime API key exclusivamente no processo `tunnel-client`. A chave, o `tunnel_id`, perfis locais e identidade do túnel não pertencem ao repositório.

Inicialize e valide o perfil conforme a [documentação oficial do Secure MCP Tunnel](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels). No ChatGPT, habilite o modo desenvolvedor, crie o app privado usando a conexão Tunnel e copie o identificador técnico `plugin_asdk_app...` da URL. Esse identificador não é credencial; pode constar em `.app.json`, enquanto todo segredo continua local.

Depois de alterar ferramentas ou metadados, atualize o app no ChatGPT e teste em conversa nova. Com o túnel desligado, o ChatGPT deve falhar sem revelar caminhos ou dados; o fluxo local do Codex continua disponível por `stdio`.

## Inicialização automática no Windows

Depois de validar manualmente o fluxo, execute `scripts/install_local_service.ps1` informando os caminhos do `tunnel-client` e do perfil, além de `-Confirm`. O instalador usa somente a chave `Run` de `HKCU`, sem privilégio administrativo, grava apenas caminhos operacionais em `%LOCALAPPDATA%` e exige que `CONTROL_PLANE_API_KEY` já esteja definida no ambiente do usuário. A chave não é copiada para arquivo ou registro.

O script inicia imediatamente o mesmo runner que será acionado no próximo logon. Para remover a inicialização, execute `scripts/uninstall_local_service.ps1 -Confirm`. A remoção apaga apenas a entrada de inicialização e seus arquivos auxiliares; biblioteca, índice, questões, tentativas e configuração da biblioteca permanecem intactos.

O runner é um supervisor persistente e idempotente. Um mutex impede supervisores duplicados; se o túnel já estiver ativo, o supervisor acompanha essa instância e, se ela encerrar, inicia outra após cinco segundos. Fechar ou reiniciar uma conversa do ChatGPT não afeta esse processo. O PID do supervisor fica em `supervisor.pid`, o PID do túnel em `tunnel.pid` e os eventos de recuperação em `supervisor.log`. O stdout e o stderr do cliente ficam em `%LOCALAPPDATA%\Estudo Jurídico Avançado\startup\tunnel-client.stdout.log` e `tunnel-client.stderr.log`, respectivamente.

Para confirmar que o cliente está operacional antes de testar no ChatGPT, consulte `http://127.0.0.1:8080/readyz` e obtenha `ready`; se a resposta remota ainda disser que o cliente não foi visto, confira também esses logs e a associação do `tunnel_id`. Não execute uma segunda instância manual com a mesma porta de health. A desinstalação encerra primeiro o supervisor e depois o túnel, sem apagar biblioteca ou histórico.
