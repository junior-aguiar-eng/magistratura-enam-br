# Orquestracao de fluxos e fontes 0.5.0 - Plano de implementacao

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implementar ambientacao fluida, estado conversacional, transicoes inteligentes e governanca de fontes no Estudo Juridico Avancado, sem misturar competencias nem transformar o inicio do estudo em formulario.

**Architecture:** Uma camada compartilhada de contratos descrevera rota, modalidade, pendencia, transicao e politica de fontes. A skill `acompanhar-percurso-magistratura` coordenara entrada e mudancas de rota, enquanto as quatro skills executoras preservarao suas autoridades e consumirao o mesmo protocolo.

**Tech Stack:** Codex plugin manifest, Markdown skills, JSON Schema, Python 3.14, `uv`, pytest, Ruff e avaliacoes comportamentais em sessoes novas.

**Spec:** `docs/superpowers/specs/2026-09-04-orquestracao-fluxos-fontes-design.md`

## Restricoes globais

- Preservar todas as capacidades, contratos pedagogicos, persistencia local e testes da `0.4.1`.
- Nao transformar ambientacao em formulario, entrevista, wizard obrigatorio ou menu repetitivo.
- Aplicar `observar -> inferir -> comunicar -> executar`.
- Fazer no maximo uma pergunta quando a ambiguidade impedir materialmente o avanco.
- Nao mudar rota por mera mencao incidental a outro tema.
- Nao descartar tentativa, remediacao ou atividade pendente silenciosamente.
- Nao persistir rota, fonte ou preferencia inferida sem consentimento expresso.
- Tratar STF, STJ e Planalto como fontes primarias centrais.
- Tratar Dizer o Direito, JOTA e Thomson Reuters / Revista dos Tribunais como fontes secundarias aprovadas e limitadas.
- Nao usar fonte secundaria como prova isolada de vigencia, tese, resultado, modulacao ou estado processual.
- Nao apresentar busca como portfolio de noticias, cards ou lista extensa de links.
- Uma fase somente termina quando todas as suas tasks, validacoes, documentacao e gates estiverem concluidos.
- Depois da conclusao integral, o commit da fase e o push imediato da branch sao automaticos, sem nova autorizacao intermediaria.
- Commit parcial nao caracteriza fase concluida; falha no commit ou no push mantem a fase aberta ate a publicacao bem-sucedida.
- PR, merge, tag e release permanecem gates separados do fechamento automatico de cada fase.

## Protocolo obrigatorio de fechamento de fase

1. Concluir todas as tasks e entregas previstas para a fase.
2. Executar todos os testes e gates definidos para a fase.
3. Corrigir qualquer falha antes de declarar a fase concluida.
4. Preparar somente os artefatos da fase, preservando alteracoes nao relacionadas.
5. Criar o commit com a mensagem prevista para a fase.
6. Executar imediatamente o push da branch de implementacao.
7. Registrar SHA, branch, resultado do push e evidencias dos gates executados.

Se o commit ou o push falhar, a fase pode estar implementada, mas nao esta encerrada ate a publicacao bem-sucedida.

---

## Visao das fases

| Fase | Entrega completa | Gate principal |
|---|---|---|
| 0 | Baseline `0.4.1` de entrada, roteamento, transicao e fontes | Variancia e falhas atuais documentadas |
| 1 | Contratos compartilhados de rota, transicao e fontes | Schemas e invariantes aprovados sem mudar comportamento |
| 2 | Orquestrador conversacional e ambientacao fluida | Entrada generica orienta e pedido especifico executa |
| 3 | Transicoes, suspensao e retomada nas cinco skills | Nenhuma mistura ou perda silenciosa de pendencia |
| 4 | Governanca de acervo, pesquisa e apresentacao de fontes | Modos respeitados e fontes secundarias subordinadas |
| 5 | Gatilhos personalizados, identidade e documentacao | Interface oferece rotas claras sem prometer memoria |
| 6 | Evals integrados, compatibilidade e release `0.5.0` | Qualidade juridica e pedagogica nao inferiores a `0.4.1` |

---

## Fase 0: congelar o comportamento da 0.4.1

### Objetivo

Registrar como a versao atual reage a pedidos genericos, diretos, ambiguos, mudancas de assunto, atividades pendentes e diferentes comandos de fonte.

### Task 0.1: ampliar o catalogo comportamental

**Files:**

- Modify: `plugins/magistratura-enam-br/evals/pedagogia/evals.json`
- Create: `plugins/magistratura-enam-br/evals/pedagogia/roteamento-fontes-0.4.1.md`
- Modify: `plugins/magistratura-enam-br/evals/pedagogia/rubrica.md`
- Test: `plugins/magistratura-enam-br/tests/test_evals_pedagogicos.py`

- [x] Criar casos para clique generico, tema direto, questao direta, curadoria, comparacao e planejamento.
- [x] Criar casos de mudanca de tema, modalidade e skill, com e sem atividade pendente.
- [x] Criar casos para `acervo_exclusivo`, material com atualizacao oficial e pesquisa completa.
- [x] Criar casos negativos: mencao incidental que nao deve mudar rota, fonte secundaria tentando substituir fonte oficial e pedido sem material que nao pode alegar acesso ao acervo.
- [x] Atualizar o schema de eval apenas se os campos atuais nao representarem `turns`, `expected_route`, `expected_transition` e `source_policy`.

### Task 0.2: executar baseline

- [x] Executar cada caso em tres sessoes novas com a release `0.4.1`.
- [x] Registrar a resposta integral apenas em armazenamento local temporario; versionar somente sintese, metricas e trechos anonimizados indispensaveis.
- [x] Medir acerto de skill, modalidade, tema, politica de fontes, quantidade de perguntas, repeticao de ambientacao e preservacao de pendencia.
- [x] Registrar como defeito o inicio arbitrario de questao ou tema diante do prompt generico atual.
- [x] Aplicar rubrica humana de naturalidade, clareza da transicao, rigor juridico e ausencia de efeito "portfolio de noticias".

### Gate da fase 0

- Todos os cenarios executados tres vezes ou indisponibilidade justificada individualmente.
- Baseline identifica variancia e nao confunde teste estrutural com comportamento do modelo.
- Nenhuma instrucao de producao alterada antes do fechamento do baseline.

**Fechamento automatico:** commit `test(plugin): baseline conversational routing and sources` e push imediato da branch.

---

## Fase 1: definir contratos compartilhados

### Objetivo

Estabelecer um vocabulario unico para rota, modalidade, etapa, pendencia, transicao e politica de fontes.

### Task 1.1: criar contrato conversacional

**Files:**

- Create: `plugins/magistratura-enam-br/references/contrato-fluxos-conversacionais.md`
- Create: `plugins/magistratura-enam-br/modelos/pedagogia/session-route.schema.json`
- Create: `plugins/magistratura-enam-br/modelos/pedagogia/transition.schema.json`
- Test: `plugins/magistratura-enam-br/tests/test_contrato_fluxos_conversacionais.py`

**Interfaces:**

```text
session-route: schema_version, skill_ativa, modalidade_ativa, tema_ativo,
               etapa, pendencia, rota_suspensa, politica_fontes
transition: from, to, kind, reason, requires_confirmation, preserves
```

- [x] Escrever fixtures validas para continuidade, mudanca de tema, mudanca de modalidade, mudanca de skill, suspensao, retomada e encerramento.
- [x] Escrever fixtures invalidas para skill inexistente, modalidade pertencente a outra skill, retomada sem rota suspensa e persistencia implicita.
- [x] Implementar schemas com `additionalProperties: false` e versao explicita.
- [x] Documentar que os objetos sao internos e nao devem aparecer como formulario ou YAML para o candidato.

### Task 1.2: criar contrato de fontes

**Files:**

- Create: `plugins/magistratura-enam-br/references/politica-fontes-juridicas.md`
- Create: `plugins/magistratura-enam-br/modelos/pedagogia/source-policy.schema.json`
- Create: `plugins/magistratura-enam-br/modelos/pedagogia/trusted-source-registry.schema.json`
- Create: `plugins/magistratura-enam-br/references/fontes-confiaveis.json`
- Test: `plugins/magistratura-enam-br/tests/test_politica_fontes.py`

- [x] Definir `acervo_exclusivo`, `acervo_com_validacao_oficial` e `pesquisa_juridica_completa`.
- [x] Cadastrar STF, STJ e Planalto como fontes primarias com finalidades permitidas.
- [x] Cadastrar Dizer o Direito, JOTA e Thomson Reuters / Revista dos Tribunais como fontes secundarias, com limites explicitos.
- [x] Exigir verificacao do dominio canonico durante a implementacao e impedir correspondencia insegura por substring.
- [x] Exigir inclusao deliberada no registro para qualquer nova fonte; "site conceituado" nao autoriza busca aberta.
- [x] Proibir que fonte secundaria confirme isoladamente vigencia, tese, resultado, modulacao ou transito em julgado.

### Task 1.3: integrar os contratos ao verificador

**Files:**

- Modify: `plugins/magistratura-enam-br/scripts/verificar_integracao.py`
- Modify: `plugins/magistratura-enam-br/tests/test_verificar_integracao.py`

- [x] Fazer o verificador exigir os quatro schemas, as duas referencias e o registro de fontes.
- [x] Validar nomes das cinco skills e modalidades aceitas.
- [x] Validar que toda fonte secundaria declare `limitations` e toda primaria declare `authoritative_for`.
- [x] Confirmar que nenhum comportamento das skills mudou nesta fase.

### Gate da fase 1

- Contratos validos e cobertos por fixtures positivas e negativas.
- Registro de fontes fechado por inclusao explicita.
- Suite `0.4.1` permanece verde e as saidas continuam inalteradas.

**Fechamento automatico:** commit `feat(plugin): define conversational and source contracts` e push imediato da branch.

---

## Fase 2: transformar acompanhamento em orquestrador conversacional

### Objetivo

Fazer a entrada generica apresentar o ambiente e encaminhar o candidato sem produzir conteudo arbitrario ou expor contratos tecnicos.

### Task 2.1: implementar ambientacao contextual

**Files:**

- Modify: `plugins/magistratura-enam-br/skills/acompanhar-percurso-magistratura/SKILL.md`
- Modify: `plugins/magistratura-enam-br/skills/acompanhar-percurso-magistratura/references/roteamento.md`
- Create: `plugins/magistratura-enam-br/skills/acompanhar-percurso-magistratura/references/ambientacao-conversacional.md`
- Modify: `plugins/magistratura-enam-br/tests/test_roteamento_percurso.py`
- Create: `plugins/magistratura-enam-br/tests/test_ambientacao_plugin.py`

- [ ] Substituir a saida YAML obrigatoria por comunicacao natural; manter estrutura apenas como raciocinio interno ou artefato solicitado.
- [ ] Definir apresentacao breve das cinco frentes somente para pedido generico.
- [ ] Fazer uma unica pergunta compacta quando tema ou finalidade forem indispensaveis.
- [ ] Fazer pedido especifico ignorar a ambientacao e seguir diretamente para a skill correta.
- [ ] Proibir escolha arbitraria de disciplina, tema ou modalidade.

### Task 2.2: estabelecer precedencia de roteamento

- [ ] Prioridade 1: invocacao explicita de skill ou modalidade.
- [ ] Prioridade 2: objetivo e insumo inequivocos.
- [ ] Prioridade 3: continuidade da rota ativa.
- [ ] Prioridade 4: inferencia conservadora com default seguro.
- [ ] Prioridade 5: uma pergunta quando nenhuma rota segura puder ser escolhida.
- [ ] Testar near-miss entre estudo de julgado, curadoria de informativo e planejamento de revisao.
- [ ] Testar que uma citacao incidental a outro ramo nao altera a rota.

### Gate da fase 2

- Clique generico apresenta e orienta sem iniciar questao.
- Pedidos diretos nao recebem menu ou introducao redundante.
- Nenhuma resposta apresenta YAML por padrao.
- Tres execucoes por cenario atingem o roteamento esperado sem regressao juridica.

**Fechamento automatico:** commit `feat(plugin): add conversational study orchestrator` e push imediato da branch.

---

## Fase 3: implementar transicoes, suspensao e retomada

### Objetivo

Manter coerencia quando o candidato muda conteudo, metodo ou modulo, sem bloquear o estudo com confirmacoes desnecessarias.

### Task 3.1: criar protocolo de transicao

**Files:**

- Create: `plugins/magistratura-enam-br/skills/acompanhar-percurso-magistratura/references/transicoes-inteligentes.md`
- Create: `plugins/magistratura-enam-br/tests/test_transicoes_rota.py`

- [ ] Especificar `CONTINUAR`, `MUDAR_TEMA`, `MUDAR_MODALIDADE`, `MUDAR_SKILL`, `SUSPENDER`, `RETOMAR` e `ENCERRAR`.
- [ ] Comunicar transicao inequivoca em uma frase e prosseguir na mesma resposta.
- [ ] Solicitar confirmacao somente quando uma pendencia seria abandonada ou uma acao persistente seria executada.
- [ ] Preservar tema quando houver apenas mudanca de modalidade.
- [ ] Preservar pendencia suspensa somente na conversa ou em checkpoint explicitamente fornecido.

### Task 3.2: integrar as cinco skills

**Files:**

- Modify: `plugins/magistratura-enam-br/skills/estudar-direito-magistratura/SKILL.md`
- Modify: `plugins/magistratura-enam-br/skills/estudar-direito-magistratura/references/ambientacao-e-calibracao.md`
- Modify: `plugins/magistratura-enam-br/skills/curar-informativos-stf-stj/SKILL.md`
- Modify: `plugins/magistratura-enam-br/skills/comparar-materiais-enam/SKILL.md`
- Modify: `plugins/magistratura-enam-br/skills/planejar-jurisprudencia/SKILL.md`
- Modify: `plugins/magistratura-enam-br/skills/acompanhar-percurso-magistratura/SKILL.md`
- Test: `plugins/magistratura-enam-br/tests/test_integracao_fluxos_skills.py`

- [ ] Fazer cada skill reconhecer continuidade dentro do proprio dominio.
- [ ] Fazer cada skill devolver mudanca de autoridade ao orquestrador sem executar a outra skill silenciosamente.
- [ ] Manter a resposta do turno util: anunciar e encaminhar, sem reiniciar entrevista.
- [ ] Proibir repeticao da ambientacao quando rota, tema e politica ja estiverem claros.
- [ ] Proibir alegacao de retomada entre sessoes sem estado fornecido.

### Task 3.3: proteger atividades pendentes

- [ ] Testar questao aguard, discursiva em elaboracao, curadoria incompleta, comparacao sem segundo documento e remediacao aberta.
- [ ] Distinguir suspender, encerrar e substituir.
- [ ] Nao registrar tentativa, erro ou abandono apenas porque o candidato mudou de assunto.
- [ ] Manter persistencia submetida ao contrato de confirmacao existente.

### Gate da fase 3

- Todas as classes de transicao possuem teste estrutural e tres execucoes comportamentais.
- Mudancas evidentes fluem sem pergunta; perdas materiais exigem uma unica decisao.
- Nenhuma atividade incompleta e descartada ou persistida silenciosamente.

**Fechamento automatico:** commit `feat(plugin): add intelligent route transitions` e push imediato da branch.

---

## Fase 4: operacionalizar a governanca de fontes

### Objetivo

Permitir estudo exclusivo pelo acervo, acervo com validacao oficial ou pesquisa completa, preservando rigor e sobriedade editorial.

### Task 4.1: integrar politica de fontes ao acervo

**Files:**

- Modify: `plugins/magistratura-enam-br/references/protocolo-uso-do-acervo.md`
- Modify: `plugins/magistratura-enam-br/references/diretrizes-estudo-juridico-brasileiro.md`
- Modify: `plugins/magistratura-enam-br/AGENTS.md`
- Test: `plugins/magistratura-enam-br/tests/test_governanca_fontes.py`

- [ ] Fazer `acervo_exclusivo` bloquear busca e complemento externo.
- [ ] Fazer `acervo_com_validacao_oficial` pesquisar apenas quando atualidade ou precisao puderem mudar materialmente.
- [ ] Fazer `pesquisa_juridica_completa` consultar primeiro a fonte primaria aplicavel.
- [ ] Declarar limitacao quando o modo exclusivo nao permitir certificar atualidade.
- [ ] Tratar preferencia inferida como estado efemero, nunca como perfil persistente.

### Task 4.2: integrar fontes nas skills juridicas

**Files:**

- Modify: `plugins/magistratura-enam-br/skills/estudar-direito-magistratura/SKILL.md`
- Modify: `plugins/magistratura-enam-br/skills/curar-informativos-stf-stj/SKILL.md`
- Modify: `plugins/magistratura-enam-br/skills/comparar-materiais-enam/SKILL.md`
- Modify: `plugins/magistratura-enam-br/skills/planejar-jurisprudencia/SKILL.md`
- Test: `plugins/magistratura-enam-br/tests/test_fontes_por_skill.py`

- [ ] Estudo: usar acervo como base e separar complemento ou atualizacao.
- [ ] Curadoria: exigir informativo oficial e usar secundarias apenas como apoio.
- [ ] Comparacao: nao introduzir pesquisa externa se o escopo for comparar exclusivamente os documentos fornecidos.
- [ ] Planejamento: nao pesquisar novo julgado quando a tarefa for apenas organizar itens ja selecionados.
- [ ] Fazer transicao de politica apenas quando o pedido alterar efetivamente o escopo de fontes.

### Task 4.3: controlar apresentacao e rastreabilidade

- [ ] Integrar fontes ao texto juridico, sem manchetes, cards ou lista de resultados.
- [ ] Usar secao final compacta `Base consultada` somente quando houver consulta externa relevante.
- [ ] Identificar fonte secundaria por natureza editorial.
- [ ] Evitar URLs brutas no corpo, sem tentar suprimir citacoes automaticas da plataforma.
- [ ] Testar divergencia entre apostila e lei vigente, resumo editorial e tese oficial, e noticia de julgamento sem acordao confirmado.

### Gate da fase 4

- `acervo_exclusivo` apresenta zero consulta externa nos cenarios de teste.
- Pesquisa completa confirma afirmacoes determinantes em fonte primaria.
- Dizer o Direito, JOTA e Thomson Reuters / Revista dos Tribunais nunca aparecem como autoridade oficial.
- Saidas mantem rastreabilidade sem aparencia de clipping de noticias.

**Fechamento automatico:** commit `feat(plugin): add controlled legal source policies` e push imediato da branch.

---

## Fase 5: personalizar gatilhos e documentar a experiencia

### Objetivo

Representar as rotas na interface do Codex e explicar o comportamento sem expor complexidade interna.

### Task 5.1: configurar prompts iniciais

**Files:**

- Modify: `plugins/magistratura-enam-br/.codex-plugin/plugin.json`
- Test: `plugins/magistratura-enam-br/tests/test_manifest_interface.py`

- [ ] Converter `interface.defaultPrompt` em lista com jornada guiada, tema juridico, treino, informativos, comparacao e revisao jurisprudencial.
- [ ] Fazer cada prompt indicar intencao suficiente para o roteamento correspondente.
- [ ] Manter a jornada guiada como unica entrada que apresenta o ambiente.
- [ ] Validar o manifesto com o validador oficial do plugin.
- [ ] Corrigir caminhos de icones das skills para que todos resolvam dentro de `assets/`, eliminando o aviso de `..` observado no smoke da `0.4.1`.

### Task 5.2: atualizar documentacao

**Files:**

- Modify: `README.md`
- Modify: `docs/site/primeiros-passos.md`
- Modify: `docs/site/arquitetura-pedagogica.md`
- Modify: `docs/site/privacidade-e-persistencia.md`
- Create: `docs/site/fontes-e-pesquisa.md`
- Modify: `mkdocs.yml`

- [ ] Explicar os tres modos de fontes e seus defaults.
- [ ] Explicar transicoes sem sugerir memoria automatica.
- [ ] Mostrar exemplos naturais, sem reproduzir schemas internos ao candidato comum.
- [ ] Documentar que fontes secundarias complementam, mas nao substituem, STF, STJ e Planalto.
- [ ] Manter documentacao publica sem dados pessoais, logs ou materiais protegidos.

### Gate da fase 5

- Prompts aparecem corretamente na superficie disponivel do Codex.
- Cada gatilho inicia a rota prevista em tres sessoes novas.
- Documentacao Zensical e Material constroi sem erro.
- Nenhum icone e ignorado por caminho invalido.

**Fechamento automatico:** commit `docs(plugin): present guided flows and source policies` e push imediato da branch.

---

## Fase 6: avaliar, compatibilizar e preparar a release 0.5.0

### Objetivo

Demonstrar que a nova arquitetura melhora previsibilidade e fluidez sem reduzir qualidade juridica, privacidade ou capacidades existentes.

### Task 6.1: executar matriz comportamental final

**Files:**

- Modify: `plugins/magistratura-enam-br/evals/pedagogia/evals.json`
- Create: `plugins/magistratura-enam-br/evals/pedagogia/relatorio-orquestracao-0.5.0.md`

- [ ] Reexecutar todos os casos novos tres vezes em sessoes independentes.
- [ ] Comparar com o baseline `0.4.1`: acerto de rota, perguntas por abertura, transicoes corretas, pendencias preservadas e politica de fontes.
- [ ] Aplicar revisao humana cega a amostra equivalente de respostas `0.4.1` e `0.5.0`.
- [ ] Bloquear release diante de regressao juridica, mistura de skills, busca no modo exclusivo, memoria ficticia ou descarte silencioso.

### Task 6.2: executar regressao tecnica e documental

- [ ] Executar suite completa com `--basetemp` isolado no Windows.
- [ ] Executar Ruff e `uv lock --check`.
- [ ] Executar verificador de integracao e validador do plugin.
- [ ] Construir Zensical e Material for MkDocs em modo estrito.
- [ ] Confirmar que nenhum arquivo de perfil, rota ou log e criado durante testes conversacionais sem opt-in.

### Task 6.3: versionar e preparar distribuicao

**Files:**

- Modify: `plugins/magistratura-enam-br/.codex-plugin/plugin.json`
- Modify: `plugins/magistratura-enam-br/pyproject.toml`
- Modify: `plugins/magistratura-enam-br/uv.lock`
- Modify: `plugins/magistratura-enam-br/CHANGELOG.md`
- Modify: `plugins/magistratura-enam-br/CONTINUACAO.md`
- Modify: `.github/workflows/validar.yml`
- Modify: `.github/workflows/docs.yml`

- [ ] Sincronizar versao `0.5.0` em manifesto, projeto e lock.
- [ ] Registrar migracao comportamental: `defaultPrompt`, ambientacao, transicoes e fontes.
- [ ] Preservar compatibilidade dos schemas pedagogicos existentes ou fornecer migracao explicita.
- [ ] Incluir todos os testes novos no CI.
- [ ] Preparar notas de release sem declarar eficacia pedagogica nao medida.

### Task 6.4: gates de publicacao

- [ ] Criar automaticamente o commit final da fase apos todos os gates locais.
- [ ] Executar automaticamente o push da branch imediatamente apos o commit.
- [ ] Abrir PR e aguardar CI de validacao e documentacao.
- [ ] Revisar e incorporar na branch padrao.
- [ ] Criar tag e release `v0.5.0` sobre o commit incorporado.
- [ ] Reinstalar exclusivamente a tag `v0.5.0` em ambiente limpo.
- [ ] Executar smoke de cada gatilho, de uma transicao, de retomada e de cada politica de fontes.

### Gates finais

```powershell
uv sync --all-groups
uv lock --check
uv run python -m pytest tests skills/planejar-jurisprudencia/tests skills/comparar-materiais-enam/tests skills/curar-informativos-stf-stj/tests --basetemp=.pytest-release-050
uv run ruff check .
uv run python scripts/verificar_integracao.py
uv run python "C:\Users\Boni Jr\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" .
uv run zensical build --clean --config-file ../../mkdocs.yml
uv run mkdocs build --strict --config-file ../../mkdocs.yml --site-dir ../../site-material
```

### Gate da fase 6

- Todos os cenarios tecnicos e comportamentais aprovados.
- Qualidade juridica nao inferior a `0.4.1`.
- Entrada generica, pedidos diretos e transicoes funcionam sem entrevista.
- Politicas de fontes respeitadas nas cinco skills.
- Release instalada e validada em nova sessao do Codex.

**Fechamento automatico:** commit `feat(plugin): release conversational architecture 0.5.0` e push imediato da branch.

---

## Dependencias e ordem obrigatoria

1. A fase 0 congela o baseline antes de qualquer mudanca comportamental.
2. A fase 1 define contratos consumidos pelas demais fases.
3. A fase 2 implementa a entrada e o roteamento sem antecipar persistencia nova.
4. A fase 3 aplica o protocolo de transicao a todas as skills.
5. A fase 4 adiciona governanca de fontes sobre o fluxo ja estabilizado.
6. A fase 5 expõe a arquitetura na interface e na documentacao.
7. A fase 6 compara, valida e publica; nao corrige silenciosamente gate pendente de fase anterior.

Cada fase produz uma entrega completa e revisavel. Implementacao de schema, prompt ou arquivo-base sem seus testes, execucoes comportamentais e documentacao correspondente nao conclui a fase.

