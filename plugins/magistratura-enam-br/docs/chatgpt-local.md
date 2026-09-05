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
