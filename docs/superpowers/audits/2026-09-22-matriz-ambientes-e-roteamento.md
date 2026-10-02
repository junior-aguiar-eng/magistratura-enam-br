# Matriz de ambientes e roteamento

Estado inspecionado em 2026-09-24 no checkout `magistratura-enam-br`, branch `codex/organizacao-qualidade-plugin`, base `8a0949d` (`v0.7.2`). Esta matriz descreve contratos do pacote e verificações locais; não equivale a homologação de cada cliente.

| Superfície | Como carrega habilidades | Como conecta MCP | Onde persiste | Estado observado e limite |
| --- | --- | --- | --- | --- |
| Codex com `magistratura-enam-br` | Cinco skills declaradas em `.codex-plugin/plugin.json` | Servidor local por `stdio` em `.mcp.json` | Biblioteca configurada por `library-config.json`; estado em `<library_root>/.estudo-juridico` | `codex plugin list --json` mostrou `0.7.2` instalado e habilitado. O smoke em fixture passou; a instalação ainda não contém a nova ferramenta desta branch. |
| Codex com `$treinador-fgv-magistratura` | Skill global fora deste repositório | Usa ferramentas disponíveis ao cliente, sem servidor MCP próprio declarado por este plugin | Estado da conversa ou JSONL local somente quando autorizado conforme a skill externa | Instalação local identificada; sua fonte, versão e comportamento não são controlados por este repositório. Invocação nominal diferencia o destino. |
| ChatGPT com app `Estudo Jurídico Avançado` | Registro em `.app.json`; disponibilidade das cinco skills depende do pacote/cliente e deve ser testada na sessão | MCP remoto por Secure MCP Tunnel para o servidor local | Mesmo servidor e biblioteca local quando o túnel aponta para esta instalação | Mapeamento do app presente; `/readyz` em `127.0.0.1:8080` retornou HTTP 404 em 2026-09-24. Ferramentas e UI no ChatGPT não foram homologadas. |
| Outros clientes MCP | Não presumido | Depende do suporte do cliente ao protocolo e à configuração do servidor | Depende da instalação e da raiz configurada | Claude, Cursor e outros não foram testados neste checkout. O widget pode exigir suporte a MCP Apps; ferramentas textuais têm contrato separado. |

## Regra de escolha

Invocação nominal de `$treinador-fgv-magistratura` usa a habilidade externa somente quando disponível. Se ausente, a indisponibilidade deve ser dita antes de oferecer o estudo do plugin. Pedido genérico de questão FGV/ENAM, sem nomear a habilidade externa, segue a modalidade de questões de `estudar-direito-magistratura` no plugin. A coexistência dos pacotes não garante seleção automática idêntica em todos os clientes; a instrução nominal remove a ambiguidade para o usuário.

O catálogo pedagógico contém três cenários de aceitação para essas situações, inclusive o positivo com a skill externa disponível. Só sua estrutura foi testada; nenhum dos três foi executado comportamentalmente no cliente correspondente.

O plugin não compartilha automaticamente histórico ou gabarito com a skill global. A existência do MCP não comprova índice criado ou atualizado. O índice pode ficar fora da pasta do plugin: a raiz da biblioteca é escolhida pelo usuário, e o estado local fica em `.estudo-juridico` dentro dela.

## Evidência do smoke local

Com acervo sintético temporário, passaram `test_fluxo_mcp_completo_preserva_gabarito_ate_tentativa`, `test_config_bundled_inicia_servidor_stdio_real` e `test_diagnostico_sem_indice_informa_caminhos_sem_escrever` (3 testes). Eles comprovam descoberta `stdio`, indexação, busca, sessão, renderização e correção após tentativa no ambiente de teste; não comprovam que a biblioteca pessoal esteja sincronizada, nem renderização visual no ChatGPT. O endpoint de saúde do túnel não estava pronto, então o smoke remoto não foi executado.

Fontes de capacidade da plataforma: [arquitetura de plugins](https://developers.openai.com/plugins/concepts/plugins) e [Secure MCP Tunnel](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels). O túnel serve a conexão privada de teste e não é via de submissão pública do plugin.
