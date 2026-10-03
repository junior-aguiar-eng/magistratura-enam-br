# Estudo Jurídico Avançado

Plugin profissional para bacharéis em Direito voltado ao estudo de alta complexidade para Magistratura e Exame Nacional da Magistratura (ENAM). Ele reúne estudo dogmático integrado, casos, questões, curadoria de informativos, comparação de materiais e planejamento de revisão de jurisprudência.

## Skills disponíveis

| Skill | Finalidade |
| --- | --- |
| `comparar-materiais-enam` | Compara versões de materiais do ENAM por tema e subtema, com quadro de deltas rastreáveis. |
| `curar-informativos-stf-stj` | Seleciona e comenta julgados de informativos do STF e do STJ. |
| `estudar-direito-magistratura` | Integra dogmática, legislação e jurisprudência e conduz casos, objetiva, discursiva, oral e revisão. |
| `planejar-jurisprudencia` | Organiza a revisão espaçada de julgados já selecionados. |
| `acompanhar-percurso-magistratura` | Apresenta as frentes disponíveis, orienta a escolha da skill e consolida o percurso sem executar automaticamente outra skill. |

Cada skill lê `AGENTS.md` antes de atuar. As diretrizes preservam rigor jurídico, uso proporcional de fontes oficiais, estudo ativo e fronteiras claras entre curadoria, estudo, comparação e planejamento.

A candidata local da task 5 explicita revisão ancorada no trecho acessível, formatos direto, numerado, V/F e associação e desenhos de soluções, matriz e fundamento. Mantém cinco alternativas, chave única e correção individual após tentativa, sem quotas de formato ou mudança do schema MCP. As [capturas e a avaliação posterior](evals/pedagogia/task5/README.md) permanecem pendentes de revisão jurídica humana; os testes locais não demonstram superioridade geral nem aprovam novas diretrizes permanentes.

A [validação da task 8](evals/pedagogia/task8/README.md) registra 42 capturas
comparativas, MCP stdio real na CLI e ensaio de anexo sem MCP no ChatGPT.
Os incrementos compõem a versão 0.8.0. A [preparação da release](evals/pedagogia/release-0.8.0/README.md)
acrescenta doze capturas e corrige a apresentação de pesquisa antes da
tentativa, a declaração de reutilização e a classificação de assertivas
arábicas. O [corpus oficial ENAM 2026.1](evals/pedagogia/calibracao-enam/enam-2026.1-tipo1/README.md)
foi adquirido; sua classificação revisada, aprovação jurídica humana e
card/fullscreen no ChatGPT são gates separados da publicação.

## Questões interativas locais

O plugin inclui um servidor MCP local e um widget moderno para questões objetivas. O modelo continua criando cada questão dinamicamente; a skill `estudar-direito-magistratura` define substância jurídica, dificuldade, cinco alternativas, gabarito único e correção integral. O MCP indexa Markdown autorizado, mantém o gabarito fora do navegador, renderiza a atividade e grava questões e tentativas na biblioteca local.

O Codex inicia o servidor empacotado por `stdio`. O ChatGPT usa o mesmo servidor por conexão privada do Secure MCP Tunnel. Consulte [docs/chatgpt-local.md](docs/chatgpt-local.md) para configuração, inicialização automática opcional e limites de segurança.

O servidor transmite orientações de fontes, qualidade das questões, proteção do gabarito, correção integral e fallback em `initialize.instructions`, extraídas da [referência canônica](references/questoes-interativas-mcp.md). Assim, clientes conectados somente ao MCP recebem essas regras sem precisar ler arquivos locais. As ferramentas anunciam schemas de saída; sessões reutilizam o contrato canônico com projeções pública e corrigida, sem aceitar projeção privada. `renderizar_questao`, `responder_questao` e `obter_questao` ficam disponíveis ao modelo e ao app; as demais ferramentas ficam disponíveis ao modelo. Busca na internet e leitura de anexos continuam dependendo do host.

O card prefere o SDK MCP Apps e usa o bridge OpenAI quando a inicialização ou as capacidades exigidas estiverem indisponíveis. Cada instância mantém um transporte. Se a resposta enviada não puder ser confirmada, consulta o estado por leitura e bloqueia a repetição até receber resultado conclusivo; não reenvia a tentativa por outro bridge. Entradas parciais ou privadas e resultados de sessões antigas não substituem a questão atual.

Após a tentativa, o card permite pedir explicação do erro, aprofundamento da distinção ou outra questão sobre o ponto estudado. Esses pedidos consultam a sessão atual e seguem para o chat, sem registrar nova tentativa ou gerar questão automaticamente. `obter_questao` recupera a projeção autorizada sem reabrir card; o modelo deve revalidá-la antes de atender. Sessão invalidada oferece somente outra questão com aviso. Quando o host não aceita mensagens, o pedido fica disponível para copiar.

Quando o host oferece os modos inline e fullscreen, o botão **Expandir para estudar** solicita a apresentação ampliada e **Voltar ao chat** retorna ao card. O retorno continua disponível quando o card está em fullscreen e o host permite inline, mesmo que retire novas expansões. O modo mostrado acompanha a confirmação e as notificações do host; expandir não envia resposta nem cria atividade. A coluna de leitura permite rolagem de questões e correções longas, com espaço para as áreas reservadas pelo host e adaptação ao tema/variáveis de estilo recebidos.

O estado visual restaura somente a escolha pendente da mesma sessão ainda pronta e a abertura dos painéis. No ChatGPT, `widgetState`/`setWidgetState` são usados quando disponíveis, inclusive com ferramentas no SDK; em outros hosts o estado pode existir apenas enquanto o componente permanece aberto. O snapshot exclui gabarito, correção, fontes e modo de apresentação. Questão respondida obedece ao servidor, e invalidação limpa seleção/painéis. Isso não equivale a memória de estudo entre sessões ou persistência de perfil. As APIs seguem a [referência oficial do bridge](https://developers.openai.com/plugins/reference).

Antes da primeira busca, `diagnosticar_acervo` informa a raiz configurada, o caminho do índice, sua existência, a data de geração e a quantidade registrada de documentos. A ferramenta é somente de leitura. Conexão MCP e índice existente não demonstram que os arquivos Markdown atuais estão sincronizados; a primeira indexação e o reparo de um índice inválido continuam exigindo `indexar_acervo` com confirmação explícita. Após a primeira indexação, `SINCRONIZAR_ACERVO.bat` permite verificar o índice por duplo clique. Opcionalmente, um verificador de execução curta pode conferir o índice no login e a cada dez minutos, atualizar apenas quando o conteúdo mudou e encerrar; ele não altera a ferramenta de busca nem mantém monitor residente. A instalação está em [docs/chatgpt-local.md](docs/chatgpt-local.md).

## Correções locais da auditoria

Questões prontas validam a cobertura dos quatro distratores e exigem fontes quando marcadas como verificadas. `invalidar_questao(session_id, motivo)` permite retirar uma questão defeituosa mesmo após a tentativa, preservando os logs e excluindo a atividade do perfil e dos relatórios reconstruídos. Eventos novos registram o resultado objetivo sem presumir diagnóstico de erro ou domínio. Dados históricos não são migrados automaticamente.

`indexar_acervo(confirmar_gravacao_local=true)` também reconstrói índices inválidos; a troca do arquivo só ocorre após concluir a leitura da biblioteca. A sincronização automática continua sem reparar índices ausentes ou inválidos.

O widget usa o SDK MCP Apps e apresenta fontes, exceções e armadilhas após a resposta. A validação comportamental pode ser registrada com `scripts/registrar_execucao_pedagogica.py`; veja [o protocolo do benchmark](evals/pedagogia/benchmark-juridico/README.md). Aprovação jurídica humana e homologação visual em host real permanecem verificações distintas dos testes locais.

## Ambiente de desenvolvimento

O [auditor quantitativo de blocos](evals/pedagogia/README.md#auditor-quantitativo-de-blocos--task-6) lê Markdown ou JSON de questões e separa erros estruturais, avisos editoriais e checagens omitidas. Ausência de gabarito completo conserva resultado parcial; heurísticas não substituem revisão jurídica. Relatórios com chaves são privados de autoria, inclusive pelas distribuições de letras. A comparação empírica com perfil de corpus permanece pendente na task 7.

O projeto usa `uv` e Python 3.14. Instale as dependências de desenvolvimento com:

```powershell
uv sync --all-groups
```

Não crie ambiente virtual manualmente nem use `pip install` para os scripts internos. O ambiente, caches e arquivos temporários não fazem parte da distribuição.

## Validação

Execute, a partir desta pasta:

```powershell
uv lock --check
uv run python -m pytest tests skills/planejar-jurisprudencia/tests skills/comparar-materiais-enam/tests skills/curar-informativos-stf-stj/tests
uv run ruff check .
uv run python scripts/verificar_integracao.py
cd web
npm ci
npm audit --audit-level=moderate
npm test -- --run
npm run lint
npm run build
```

O verificador interno é somente leitura: ele valida arquivos distribuíveis, contrato do manifesto e das skills, JSON, sintaxe Python, coerência de versão e o lockfile, sem criar artefatos no código-fonte.

O workflow de raiz `.github/workflows/validar.yml` executa esses gates e instala o bundle com o CLI do Codex em cada `push` e pull request.

## Estrutura relevante

- `.codex-plugin/plugin.json`: manifesto canônico do plugin.
- `AGENTS.md`: diretrizes obrigatórias para manutenção e execução das skills.
- `CHANGELOG.md`: histórico de alterações publicáveis.
- `CONTINUACAO.md`: estado técnico e roteiro de manutenção.
- `mcp_server/`: indexação recursiva de Markdown, sessões privadas, histórico e transporte MCP.
- `web/`: código e artefato compilado do widget de questões.
- `modelos/pedagogia/`: schemas versionados de evento, perfil reconstruível e recomendação de revisão.
- `references/contrato-pedagogico.md`: taxonomia comum e limites de inferência entre as cinco skills.
- `references/persistencia-pedagogica-local.md`: comandos explícitos, reconstrução, exportação e exclusão dos dados locais.
- `scripts/eventos_aprendizagem.py` e `scripts/perfil_candidato.py`: log append-only e perfil reconstruível, sem rede ou caminho oculto.
- `skills/`: instruções, referências, modelos, scripts e testes de cada skill.

Consulte o [changelog](CHANGELOG.md) antes de atualizar ou publicar o plugin.

## Acompanhamento e persistência

A instalação funciona sem perfil e sem histórico: as cinco skills podem ser usadas diretamente, e a ausência de dados prévios é tratada como ausência de evidência. Persistência é opcional, local e acionada somente por pedido expresso, confirmação e caminho indicado pelo candidato. Leitura, uso na sessão, gravação e exclusão são autorizações distintas.

No estudo dogmático, legislação e jurisprudência entram no ponto em que instituem, delimitam, excepcionam, atualizam ou aplicam o conceito. Referências legais permanecem cirúrgicas; fontes jurisprudenciais oficiais consultadas são reunidas ao final da resposta, sem transformar a exposição em glossário ou boletim.

O acompanhamento unificado recomenda a skill adequada, mas não executa escrita nem promete memória automática. Relatórios locais são gerados apenas mediante formato explícito:

```powershell
uv run python scripts/relatorio_aprendizagem.py --entrada eventos.jsonl --inicio 2026-09-01 --fim 2026-09-30 --formato markdown
```

Planilhas antigas continuam usando a política fixa como padrão. A política adaptativa permanece em modo sombra e não substitui datas sem opt-in. O fechamento de remediação exige evento validado e confirmação explícita.

## Corpus e calibração

O [contrato de calibração por edição/caderno](evals/pedagogia/calibracao-enam/README.md) oferece schema de metadados/classificações e CLI somente leitura. `scripts/calibrar_provas.py` gera perfil descritivo recomputável, com cobertura e exclusões; o auditor pode comparar formatos quando a referência for fornecida e elegível. Nenhum corpus oficial é distribuído ou coletado automaticamente: o perfil empírico permanece pendente até seleção e conferência documental próprias, sem quotas ou aprovação jurídica automática.
