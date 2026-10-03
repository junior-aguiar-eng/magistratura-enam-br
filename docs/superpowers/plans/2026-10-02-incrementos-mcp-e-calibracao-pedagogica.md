# Incrementos MCP e calibração pedagógica — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Native execution recommended; delegation only when explicitly selected.

**Goal:** Melhorar continuidade e confiabilidade das questões no ChatGPT e ampliar a calibração pedagógica com ideias verificadas da skill Claude 2.2.0.

**Architecture:** Evolução incremental da árvore canônica, em duas frentes independentes. O servidor mantém estado e contratos; o widget negocia capacidades e apresenta a interação; as skills mantêm autoridade pedagógica. Auditoria quantitativa permanece separada da aprovação jurídica humana.

**Tech Stack:** Python 3.14, uv, MCP Python já fixado em uv.lock, React/TypeScript, @modelcontextprotocol/ext-apps, pytest, Vitest, Zensical/MkDocs.

**Spec:** [Especificação](../specs/2026-10-02-incrementos-mcp-e-calibracao-pedagogica.md).

## Global Constraints

- Base: `main`, `8b245f10bce3aa85fa41c2b114a46fcdc9251342`, plugin 0.7.5. Reconfirmar Git, remoto e working tree ao executar; criar branch `codex/incrementos-mcp-calibracao` se ainda inexistente.
- Toda implementação ocorre em `plugins/magistratura-enam-br`; documentação de plano/spec ocorre em `docs/superpowers`.
- Ler AGENTS e os contratos afetados; nenhuma fonte do Claude ou porcentagem não demonstrada substitui regra canônica.
- Questões mantêm cinco escolhas A–E, chave única, proteção pré-tentativa, correção integral e invalidação auditável.
- Estudo com anexo ou internet funciona sem MCP; gravação, perfil, indexação e tarefas agendadas preservam suas autorizações.
- Logs históricos permanecem legíveis e não são reescritos; a UI nunca é fonte de verdade de resultado.
- Não adicionar API paga, biblioteca de UI ou backend de coleta sem necessidade demonstrada. SDK instalado já contém sendMessage, updateModelContext e eventos de contexto.
- Atualizar README, CHANGELOG e CONTINUACAO nos commits que alterem comportamento. Regerar bundle somente a partir de fonte validada.
- Plano aprovado em 2026-10-02. Tasks 1–3 concluídas e revisadas; o pedido vigente autoriza executar e commitar somente a task 4 na mesma branch. Tasks 5–8, push, reinstalação e publicação permanecem fora desta execução.

## Review Focus

1. Timeout após tentativa efetivada: não duplicar mutação por fallback de transporte — tarefa 2.
2. Cards de sessões diferentes e estado restaurado adulterado: não trocar resposta/gabarito — tarefas 3–4.
3. Host sem mensagens, estado ou variáveis de tema: fluxo textual e interação básica utilizáveis — tarefas 2–4.
4. Prova sem gabarito definitivo, contagens sem corpus e amostras pequenas: sem aprovação ou estatística simulada — tarefas 6–7.
5. Material anexado ilegível e notícia de julgamento sem fundamentos: reconhecer limite antes de ensinar ou formular — tarefas 5 e 8.

## Ordem e entregas

| Entrega | Tarefas | Resultado revisável |
|---|---|---|
| A — interação MCP | 1–4 | Orientações do servidor, bridge, ações pós-resposta, estado, tema e fullscreen |
| B — pedagogia | 5–7 | Revisão ancorada, formatos, auditor e corpus |
| C — homologação | 8 | Comparação base/candidata e matriz de clientes |

A e B podem ser integradas separadamente. Sequência recomendada: A → B → C. A tarefa 3 depende de 1–2; a tarefa 4 depende de 2; 6–7 dependem do vocabulário da tarefa 5. Cada tarefa termina com verificação própria e commit atômico durante a execução aprovada.

## Task 1: Instruções MCP, visibilidade e saídas

**Files:** modificar `references/questoes-interativas-mcp.md`, `mcp_server/server.py`, `mcp_server/schemas/question-session.schema.json` se a projeção de saída exigir schema derivado; criar `mcp_server/instructions.py`; ampliar `tests/test_mcp_transport.py`, `tests/test_mcp_ui_resource.py` e `tests/test_mcp_schemas.py`.

**Interfaces:** `load_server_instructions() -> str`, derivada de bloco delimitado `<!-- mcp-instructions:start/end -->` da referência canônica. Saída de sessão reutiliza definições existentes; não devolver schema privado em endpoint público. O registrador SDK deve anunciar instructions e schemas no protocolo negociado, sem monkey patch.

- [x] Escrever regressões `test_servidor_anuncia_instrucoes_canonicas`, `test_visibilidade_resposta_modelo_e_app` e `test_schema_saida_publica_nao_exige_gabarito`: descobrir servidor real, verificar instruções não vazias, metadados padronizados, sessão pronta sem campos privados e sessão respondida coerente. Testar annotations de leitura/escrita e ausência de nova autorização implícita.
- [x] Executar os testes e confirmar falha por ausência do novo contrato.
- [x] Implementar bloco compacto com fontes, chave única, distratores, correção integral, invalidação, sequência e fallback. Encaminhar referência humana aos contratos completos; não alegar que o ChatGPT lê arquivos locais. Testar bloco ausente/incompleto como erro de manutenção.
- [x] Definir `ui.visibility` explícita para renderizar/responder `[model, app]`; não tornar responder exclusivo do app. Conferir compatibilidade de instructions/outputs no SDK fixado antes de mudar dependência; se API não existir, registrar prova e escolher atualização mínima suportada.
- [x] Rodar `uv run python -m pytest tests/test_mcp_transport.py tests/test_mcp_ui_resource.py tests/test_mcp_schemas.py -q --basetemp=.pytest-mcp-instructions`; aprovação somente com discovery e tools/call reais, usando biblioteca sintética.
- [x] Atualizar documentação operacional e commitar a unidade após diff staged revisado.

**Registro da execução:** contratos separados em `mcp_server/outputs.py`, com RootModel/TypedDict suportados pelo SDK atual; não foi necessário modificar o schema persistido nem dependências. A asserção antiga de `tests/test_mcp_tools.py` foi alinhada à visibilidade padronizada, preservando a exclusividade do recurso UI no renderizador. Suíte integral: 374 testes aprovados; Ruff, lockfile e integração (42 checks) aprovados. Trabalho feito na branch indicada, no checkout existente; tasks 2–8 aguardam execução própria.

**Encerramento da task 1:** gate específico com 29 testes aprovados; build MkDocs estrito aprovado. Revisão independente em `8b245f1..b062ce0` sem achados críticos, importantes ou menores, com verificação adicional de erro sem vazamento e legibilidade histórica por cliente MCP real. Retry/bridge, estado entre cards, adaptação do host, corpus e desempenho pedagógico permanecem nas tasks previstas; comportamento visual e cumprimento das instruções pelo modelo não foram homologados neste ciclo.

## Task 2: Bridge padronizado e lifecycle

**Files:** criar `web/src/mcp-host.ts` e `web/src/mcp-host.test.ts`; modificar `web/src/QuestionWidget.tsx`, `web/src/contracts.ts`, `web/src/QuestionWidget.test.tsx`.

**Interfaces:** `createQuestionHost(onResult: (result: ToolResult) => void): QuestionHost`; `QuestionHost` expõe `connect(): Promise<void>`, `callTool(name: string, args: Record<string, unknown>): Promise<ToolResult>`, `close(): void` e capacidade de mensagens/contexto. Métodos opcionais da tarefa 3 serão `sendMessage(text: string): Promise<void>` e `updateContext(context: FollowUpContext): Promise<void>`. Uma instância escolhe um transporte; a UI não decide novamente a cada botão.

- [x] Escrever testes de host com ambos os bridges, somente SDK, somente OpenAI, aprovação seguida de entrada e resultado, timeout, isError, desmontagem e notificação atrasada. Usar SDK real com host simulado como nos testes atuais.
- [x] Executar `npm test -- --run src/mcp-host.test.ts src/QuestionWidget.test.tsx` e capturar RED para a prioridade padronizada e lifecycle.
- [x] Implementar negociação por capacidades. Falha inequívoca antes de enviar pode selecionar bridge legado; timeout de chamada enviada não provoca retry por outro transporte. Solicitar estado por leitura para reconciliação quando disponível.
- [x] Tratar `ontoolinput` apenas como entrada de renderização contendo session_id; aguardar resultado validado. Ignorar entradas privadas e parciais como conteúdo público. Normalizar envelopes sem renderizar `_meta` oculto.
- [x] Reexecutar testes: uma resposta efetivada seguida de timeout produz no máximo um envio de mutação; resultado de sessão antiga não substitui a atual; unmount remove listeners/conexão.
- [x] Atualizar referência MCP, validar TypeScript e commitar a unidade.

**Registro da execução:** `bindSession` ancora também a questão inicial. A incerteza de confirmação bloqueia repetição por sessão; consulta pronta não autoriza reenvio. Vitest passa a descobrir `.ts` além de `.tsx`. O gate obrigatório de auditoria encontrou uma cadeia vulnerável sem versão corrigida em `vite-plugin-singlefile`; um plugin Vite limitado ao único HTML substitui esse empacotador, com teste de incorporação e escape de JS/CSS/assets. Não foi acrescentada biblioteca de UI ou dependência de runtime. Métodos de mensagens/contexto e fullscreen permanecem nas tasks 3 e 4.

**Encerramento da task 2:** 37 testes web e 374 Python aprovados; TypeScript, build, auditoria npm sem vulnerabilidades, Ruff, lockfile, integração e MkDocs estrito aprovados. A revisão independente de `04c1be8..cce81f5` confirmou dois achados importantes de carregamento indefinido. Resultado malformado e cancelamento foram reproduzidos RED e corrigidos, com suíte web integral verde e bundle regenerado; resultados de sessão antiga permanecem descartados. Não houve achado crítico ou menor confirmado. Homologação no ChatGPT real continua na task 8.

## Task 3: Continuidade entre card e conversa

**Files:** modificar `mcp_server/server.py`, `web/src/QuestionWidget.tsx`, `web/src/contracts.ts`, `web/src/mcp-host.ts`; criar `web/src/question-followup.ts`, `web/src/question-followup.test.ts`; ampliar `tests/test_mcp_tools.py`, `tests/test_mcp_transport.py` e `web/src/QuestionWidget.test.tsx`.

**Interfaces:** ferramenta `obter_questao(session_id: str)` retorna `QuestionRepository.get_session(session_id)` em modo read-only, sem template de UI. `FollowUpAction = explain_error | deepen_distinction | new_question`; `FollowUpContext = { schema_version: "1.0.0", session_id, action, subject, topic, state }`; `buildFollowUp(question: Question, action: FollowUpAction): { text: string; context: FollowUpContext }`.

- [x] Escrever testes: pronta não libera correção em obter_questao; respondida devolve correção; invalidada devolve estado público e motivo; consulta não muda logs. Ações indisponíveis pré-tentativa; explain_error somente em erro; invalidada permite apenas new_question com aviso.
- [x] Confirmar RED para a consulta e para os botões.
- [x] Implementar consulta com annotations de leitura e saída tipada da tarefa 1. Construir mensagens curtas citando session_id e ação; servidor revalida estado antes do aprofundamento. Mensagem não inclui resposta privada nem inventa diagnóstico de erro.
- [x] Implementar `App.sendMessage` e `App.updateModelContext` se negociados; usar `sendFollowUpMessage` quando somente bridge OpenAI estiver disponível. Sem suporte, mostrar texto copiável. Atualização de contexto não impede o texto autossuficiente de ser enviado, mas falha de mensagem exibe erro e permite tentativa explícita.
- [x] Testar duas instâncias de card, double-click e mudança de sessão durante envio. Atualizar contexto substituindo o anterior, sem acumular respostas. Nenhuma ação registra tentativa, altera perfil ou cria sessão automaticamente.
- [x] Rodar testes Python de tools/transporte e Vitest de followup/widget; documentar o fluxo e commitar.

**Registro da execução:** `obter_questao` fica disponível ao modelo/app para leitura antes do envio e revalidação pelo modelo. Foi necessário atualizar o teste anterior de visibilidade e acrescentar CSS mínimo para a nova seção. A consulta não rouba foco da ação: o efeito da correção depende de sessão/estado. Suíte completa: 377 testes Python e 57 web aprovados; TypeScript/build, Ruff, lockfile, integração, documentação estrita e auditoria npm sem vulnerabilidades aprovados. Nenhuma nova dependência ou alteração de logs. Homologação no ChatGPT real permanece pendente.

**Encerramento da task 3:** revisão independente de `1934373..d79bd59` confirmou uma janela de envio antigo após `tool-input` de outra sessão, antes de seu `tool-result`. Reproduzido RED e corrigido com `sendMessage(text, sessionId)`, que verifica sessão no adaptador antes de despachar e após confirmar. Falha ordinária de contexto continua não bloqueando mensagem autossuficiente. Os 57 testes web passaram após a correção; nenhum achado crítico ou menor foi confirmado.

## Task 4: Estado visual, tema do host e fullscreen

**Files:** criar `web/src/question-ui-state.ts` e `web/src/question-ui-state.test.ts`; modificar `web/src/mcp-host.ts`, `web/src/contracts.ts`, `web/src/QuestionWidget.tsx`, `web/src/styles.css` e testes do widget.

**Interfaces:** `QuestionUiState = { schema_version: "1.0.0", session_id, selected_option?: OptionId, expanded: { distractors: boolean, sources: boolean } }`; `restoreUiState(raw: unknown, question: Question): QuestionUiState`. Whitelist exata; somente ready restaura escolha pendente. Bridge OpenAI usa widgetState/setWidgetState; host sem armazenamento conserva apenas estado React.

Extender `QuestionHost` com `requestDisplayMode(mode: "inline" | "fullscreen"): Promise<void>` e observação de modo confirmado pelo host. Negociar capacidade e modos disponíveis; usar `App.requestDisplayMode({ mode })` como caminho padrão e `window.openai.requestDisplayMode({ mode })` no bridge legado. `displayMode` pertence ao host, não ao snapshot persistido da questão. Nunca usar a Fullscreen API do navegador para substituir a apresentação controlada pelo ChatGPT.

- [x] Escrever casos de snapshot adulterado, outra sessão, campo privado, answered/invalidated e host sem persistência. Correção/gabarito nunca aparece no snapshot salvo; resultado efetivo do servidor vence seleção antiga.
- [x] Confirmar RED; implementar leitura validada e salvamento síncrono após mudança significativa, sem efeito que sobrescreva snapshot antes da restauração.
- [x] Acrescentar teste de mudança de tema e aplicação de `hostContext.styles.variables`; aplicar helpers do SDK quando presentes, mantendo fallback CSS. Registrar handler antes da conexão e remover ao fechar.
- [x] Escrever testes RED para **Expandir para estudar** → solicitação fullscreen e **Voltar ao chat** → inline; solicitação recusada ou modo diferente do pedido conserva apresentação real. Host sem suporte não oferece controle inoperante. Notificação de mudança externa atualiza o botão sem novo envio.
- [x] Implementar expansão por clique, com controle de solicitação pendente e erro acessível; adaptar layout ao modo efetivo. Preservar sessão, escolha, painéis, correção e proteção pré-tentativa ao entrar/sair. Não disparar mutações MCP nem abrir fullscreen automaticamente após resposta ou restauração.
- [x] Verificar teclado, foco, zoom 200%, viewport 360 px, temas claro/escuro e reduce-motion. Painéis expandidos não preservam conteúdo privado anterior.
- [x] Validar fullscreen com questão e correção longas: coluna de leitura confortável, rolagem completa de fontes/distratores e composer/áreas reservadas pelo host acessíveis. Testar expansão e retorno durante ready, answered e invalidated sem perda nem troca de sessão.
- [x] Rodar Vitest, `npm run lint`, `npm run build`; regenerar `web/dist/index.html`. Usar nova URI visual versionada em `mcp_server/resources.py` se o host mantiver cache, preservando aliases anteriores e seus testes.
- [x] Documentar que estado de widget não equivale a memória entre sessões; commitar.

**Registro da execução:** 377 testes Python e 91 web aprovados. Restauração validada, armazenamento opcional, tema/variáveis e negociação de fullscreen implementados sem mutação de ferramentas. QA visual usa navegador com host sintético: teclado, 360 px, zoom 200%, temas e movimento reduzido; longos painéis/fontes rolam sem bloquear o composer simulado. ChatGPT real permanece na task 8. `openai/ui.availableDisplayModes` é anunciado no conteúdo dos dois recursos, além da inicialização do SDK. Sem evidência de cache do host, URIs v2/v1 preservadas; reavaliar no host real.

## Task 5: Revisão ancorada, formatos e desenhos

**Files:** modificar `skills/estudar-direito-magistratura/SKILL.md`, `references/questoes-interativas-mcp.md`, `skills/estudar-direito-magistratura/references/questoes-fgv-enam.md`, `references/revisao.md` da mesma skill e `references/cenarios-avaliacao.md`; criar `tests/test_formatos_questoes.py` e ampliar `tests/test_contrato_questoes_fgv.py`, `tests/test_contrato_acervo_markdown.py`.

**Interfaces:** vocabulário de formato `direto | numerado | vf | associacao`, usado no auditor/corpus. Sem novo campo obrigatório na sessão MCP: formatos são expressos pelo prompt e cinco alternativas existentes. Desenhos `solucoes | matriz | fundamento` são orientações de geração, não evidências de desempenho.

- [ ] Acrescentar cenários de revisão de trecho enviado agora, material anterior inacessível, nota/notícia sem fundamento, V/F e associação, matriz de competência/efeito e mesma conclusão com fundamento distinto. Assertivas recebem análise individual após tentativa; nenhuma combinação tem duas escolhas corretas.
- [ ] Rodar testes contratuais existentes e novos; confirmar RED das novas instruções. Esses testes só demonstram vinculação/estrutura, não qualidade semântica.
- [ ] Explicitar ancoragem nas instruções de revisão, reaproveitando protocolo de acervo. Incluir formatos e desenhos sem porcentagem fixa, sem variedade forçada numa questão única e sem reduzir correção após acerto.
- [ ] Adicionar critérios humanos aos cenários: suporte oficial/material, núcleo funcional, plausibilidade, unicidade, comparação dos distratores e limite de fonte. Manter chave/rubrica fora da apresentação ao candidato.
- [ ] Executar cenário pertinente em sessão limpa com saída capturada e rubrica posterior antes de aprovar mudança substancial. Se revisão humana estiver indisponível, registrar candidato pendente; não trocar por teste de strings.
- [ ] Atualizar diretriz permanente em AGENTS apenas para comportamento aprovado e compatível com suas travas; atualizar docs e commitar.

## Task 6: Auditor quantitativo de blocos

**Files:** criar `scripts/auditar_questoes.py`, `tests/test_auditar_questoes.py` e `modelos/pedagogia/question-block-audit.schema.json`; documentar em `evals/pedagogia/README.md`.

**Interfaces:** definir `AuditQuestion` como dataclass com `id: str`, `format: Literal["direto", "numerado", "vf", "associacao"]`, `prompt: str` e `alternatives: list[tuple[str, str]]`; preservar duplicatas na lista para detectá-las antes de construir dicionário. `parse_question_block(text: str, *, format: Literal["markdown", "json"]) -> list[AuditQuestion]`; JSON aceita array das projeções de sessão existentes, usando session_id como id. `audit_question_block(questions: list[AuditQuestion], answers: dict[str, str] | None = None, profile: dict | None = None) -> dict`. Resultado: `schema_version`, `questions_count`, `errors`, `warnings`, `not_checked`, `metrics`; métricas incluem amostra/denominador. CLI leitura: `--questoes PATH --formato markdown|json [--gabarito PATH] [--perfil PATH]`; imprime JSON, sem salvar nem alterar entradas.

- [ ] Testar cinco A, ausência de E, ID duplicado, chave fora de A–E, gabaritos contraditórios, arquivo vazio, assertivas multilinha, Markdown estilizado e formato não interpretável. Todos os erros impedem aprovação estrutural; não assumir bloco válido por contar cinco linhas.
- [ ] Testar vazamento explícito de solução; não marcar toda ocorrência de “correta” no comando como gabarito antecipado. Gabarito separado nunca é anexado à saída pré-tentativa.
- [ ] Testar bloco sem chave ou com chave parcial: resultados devem informar checagens omitidas e usar denominador apenas dos itens elegíveis; não tratar cobertura parcial como aprovação global.
- [ ] Confirmar RED; implementar parser determinístico e análise somente leitura. Letras repetidas, extensão e absolutos produzem métricas/avisos, sem invalidar conteúdo por heurística isolada.
- [ ] Medir todos os tamanhos; emitir alerta agregado de extensão/absolutos apenas com ≥8 itens elegíveis e padrão >75%, explicitando que o limiar é heurística do projeto, não estatística oficial. Sem perfil, não aplicar quota de formato nem declarar bloco fiel ao ENAM. Gabarito sequencial é aviso, não reprovação jurídica.
- [ ] Rodar `uv run python -m pytest tests/test_auditar_questoes.py -q --basetemp=.pytest-block-audit`; inputs permanecem byte a byte idênticos, saídas validam schema. Documentar fronteira da revisão humana e commitar.

## Task 7: Corpus e calibração de simulado

**Files:** criar `modelos/pedagogia/exam-corpus.schema.json`, `scripts/calibrar_provas.py`, `tests/test_calibrar_provas.py`, `evals/pedagogia/calibracao-enam/README.md`; modificar referência de questões da skill e catálogo `evals/pedagogia/evals.json` para os cenários novos.

**Interfaces:** `validate_corpus(corpus: dict) -> None`; `build_calibration_profile(corpus: dict) -> dict`. Perfil inclui origem/hash/edição/tipo, quantidade total e revisada, distribuição de formatos, fonte do ponto e disciplina; dificuldade editorial informa autor/método. Perfil é consumido pelo auditor da tarefa 6 e pela sessão apenas quando fornecido/disponível.

- [ ] Testar corpus sem fonte oficial, sem hash, gabarito provisório, questão anulada, revisão ausente e classificação não resolvida. Entradas incompletas/anuladas não alimentam distribuição de itens válidos; toda exclusão aparece na cobertura.
- [ ] Confirmar RED; implementar schema e geração read-only. Não converter duração, extensão ou disciplina em dificuldade objetiva. Classificação manual exige revisor/data/nota; perfil não contém respostas pessoais.
- [ ] Documentar coleta de corpus oficial como etapa própria. Versionar metadados e classificação, não republicar cadernos completos nem gerar números fictícios para preencher exemplo. Sem corpus disponível, entregar mecanismo validado e declarar perfil empírico pendente.
- [ ] Calibrar bloco novo com corpus selecionado pelo usuário; variar demanda cognitiva sem enfraquecer distratores/âncoras. Preservar a exigência de alta complexidade do treino. Não usar a proporção 75/25 do Claude como default estatístico.
- [ ] Rodar testes do corpus/auditor e revisar amostra rotulada. Divergência entre classificadores permanece registrada; não resolver por média automática.
- [ ] Documentar o perfil comprovado ou a pendência; commitar separadamente do MCP.

## Task 8: Comparação, homologação e entrega

**Files:** criar `docs/superpowers/audits/2026-10-02-validacao-incrementos-mcp-calibracao.md`; atualizar documentação de desenvolvimento/instalação, CHANGELOG e CONTINUACAO. Usar `scripts/registrar_execucao_pedagogica.py`, `evals/pedagogia/evals.json` e schema de execução existentes; resultados pessoais ficam fora do Git.

- [ ] Capturar antes/depois: questão direta, V/F, associação, revisão de material novo e simulado calibrado. Três sessões limpas por caso/versão, mesmo modelo/cliente e fontes. Usar snapshot de baseline separado, sem instalar versão antiga sobre a instalação ativa; base já capturada pode ser usada se metadados comprovarem equivalência.
- [ ] Aplicar rubrica posterior: suporte jurídico, unicidade, qualidade dos distratores, correção após acerto/erro, ancoragem e ausência de gabarito antes da tentativa. Identificar revisor; usar hashes e registrar variabilidade. Não afirmar ganho de qualidade sem comparação efetivamente revisada.
- [ ] Rodar gate Python completo: `uv run python -m pytest tests skills/planejar-jurisprudencia/tests skills/comparar-materiais-enam/tests skills/curar-informativos-stf-stj/tests -q --basetemp=.pytest-incrementos-final`; Ruff, `uv lock --check` e `scripts/verificar_integracao.py` sem erros.
- [ ] Rodar `npm ci`, `npm audit --audit-level=moderate`, `npm test -- --run`, `npm run lint`, `npm run build`. Verificar bundle distribuível sem caches/ambientes. Se dependências mudarem, executar auditoria Python do lockfile.
- [ ] Construir Zensical e MkDocs estrito conforme workflow atual.
- [ ] Homologar chat sem MCP com anexo legível; pesquisa STF/STJ por cliente com busca; Codex stdio; ChatGPT MCP-only por conexão real; card com resposta, invalidação, botão pós-resposta, reconstrução visual, troca de tema, fullscreen/retorno e permissão negada. Conferir expansão com conteúdo longo, modo recusado e apresentação móvel. Registrar versão do cliente, capacidades e resultado; testes simulados não marcam esse gate como aprovado.
- [ ] Se host/conta/revisor estiver indisponível, entregar código validado com esse gate pendente e motivo concreto. Não inventar disponibilidade nem marcar cenário como realizado.
- [ ] Revisar diff completo, documentar achados e corrigir regressões. Propor versão 0.8.0 para conjunto A+B; se frentes forem publicadas separadamente, decidir versão pelo diff efetivo. Uma versão futura aqui é proposta, não release criada.
- [ ] Após autorização específica de entrega, executar commit/push/CI/merge/tag/release/reinstalação e comparar cache com árvore publicada. Snapshot atual 0.7.5 permanece referência de rollback; publicação não equivale a homologação humana.

## Fora da primeira entrega

MCP Events, uploads dentro do card, OCR e monitoramento automático de tribunais não são dependências das tarefas acima. MCP Events exige estudo de disponibilidade Work/Cloud, endpoint autenticado, assinaturas duráveis, webhooks, deduplicação/replay e revogação; só avançar mediante demanda e plano próprio. O evento pedagógico JSONL existente não é uma implementação de MCP Events. Fullscreen integra a tarefa 4 por solicitação expressa de Boni.

## Critério de conclusão

Plano executado exige tarefas implementadas, gates registrados, correção integral preservada, fallback textual utilizável e documentação fiel. Corpus empírico, revisão jurídica e homologação em host real são evidências separadas: qualquer pendência precisa constar expressamente no relatório final. Contagem de testes e suporte do SDK não demonstram melhora do desempenho jurídico por si só.
