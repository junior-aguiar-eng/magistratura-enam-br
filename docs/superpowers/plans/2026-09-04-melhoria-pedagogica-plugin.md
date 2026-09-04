# Melhoria pedagógica do plugin Magistratura ENAM BR - Plano de implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transformar o plugin em um ambiente pedagógico local, integrado, mensurável e progressivamente adaptativo, preservando as quatro skills e o controle do candidato.

**Architecture:** Um log append-only de eventos pedagógicos será a fonte canônica; o perfil do candidato será uma projeção reconstruível e opcional. As skills continuarão isoladas por domínio e se integrarão por schemas compartilhados, enquanto adaptação e orquestração serão introduzidas somente depois de avaliações comportamentais e gates de compatibilidade.

**Tech Stack:** Python 3.14, `uv`, JSON Schema, JSONL, Markdown, pytest, Ruff, openpyxl e infraestrutura atual de plugins/skills do Codex.

**Spec:** `docs/superpowers/specs/2026-09-04-ambientacao-pedagogica-design.md`

## Restrições globais

- Preservar as quatro skills atuais e suas fronteiras de domínio.
- Persistência local, explícita, opcional e sem dados pessoais obrigatórios.
- Usar o log JSONL append-only como fonte canônica e o perfil como projeção reconstruível.
- Manter a política fixa de revisão como padrão até a aprovação do modo adaptativo em sombra.
- Manter correção completa como padrão até opção expressa por feedback adaptativo.
- Não criar conta, nuvem, telemetria, banco remoto, gamificação ou agenda geral automática.
- Usar Python `>=3.14,<3.15`, `uv` e dependências já presentes sempre que suficientes.
- Alterar comportamento somente após teste falhar pela ausência da capacidade e cenário comportamental revelar o baseline.
- Atualizar `AGENTS.md`, `README.md`, `CHANGELOG.md` e `CONTINUACAO.md` quando a fase modificar contrato, comportamento, versão ou validação.
- Executar ao final de cada fase a suíte canônica, Ruff, `uv lock --check`, verificador de integração e validador do plugin.

---

## Visão das fases

| Fase | Entrega independente | Gate para avançar |
|---|---|---|
| 0 | Baseline pedagógico e harness de avaliação | Casos executados e variância documentada |
| 1 | Taxonomia e schemas compartilhados | Contratos válidos e nenhuma mudança de comportamento |
| 2 | Log local e perfil reconstruível | Persistência explícita, atômica e reversível |
| 3 | Estudo e feedback adaptativos opt-in | Qualidade não inferior ao baseline |
| 4 | Revisão de jurisprudência adaptativa em sombra | Sugestões determinísticas e compatibilidade da planilha |
| 5 | Ciclo integrado entre as quatro skills | Remediação fecha o ciclo sem transporte ambíguo |
| 6 | Orquestração fina, observabilidade e release | Evals ampliados, documentação e migração aprovadas |

---

## Fase 0: estabelecer baseline pedagógico

### Objetivo

Medir o comportamento atual antes de alterar prompts, contratos ou fluxos. Os testes atuais continuarão válidos, mas deixarão de ser tratados como prova suficiente de eficácia pedagógica.

### Task 0.1: criar catálogo de avaliações comportamentais

**Files:**

- Create: `plugins/magistratura-enam-br/evals/pedagogia/evals.json`
- Create: `plugins/magistratura-enam-br/evals/pedagogia/rubrica.md`
- Create: `plugins/magistratura-enam-br/evals/pedagogia/README.md`
- Create: `plugins/magistratura-enam-br/evals/pedagogia/schema/evals.schema.json`
- Test: `plugins/magistratura-enam-br/tests/test_evals_pedagogicos.py`

**Interfaces:**

- Consumes: as skills da versão `0.3.3` sem alterações.
- Produces: casos versionados com `id`, `skill`, `prompt`, `fixtures`, `assertions`, `human_rubric` e `risk_tags`.

- [ ] Escrever teste que rejeite avaliação sem skill, resultado esperado ou rubrica.
- [ ] Executar `uv run python -m pytest tests/test_evals_pedagogicos.py -v` e confirmar falha pela ausência do catálogo.
- [ ] Criar schema e doze casos sintéticos: quatro de estudo/questões, três de curadoria, três de planejamento e dois de comparação.
- [ ] Incluir casos negativos de acionamento: pedido de agenda dirigido à skill de estudo, julgado isolado dirigido à curadoria e material não publicado dirigido ao comparador.
- [ ] Executar o teste focado e confirmar aprovação.

### Task 0.2: criar avaliador determinístico de estrutura

**Files:**

- Create: `plugins/magistratura-enam-br/scripts/avaliar_saida_pedagogica.py`
- Test: `plugins/magistratura-enam-br/tests/test_avaliar_saida_pedagogica.py`

**Interfaces:**

- Consumes: `avaliar_saida(caso: dict, texto: str) -> dict`.
- Produces: `{status, assertions, human_review_required}` sem declarar correção jurídica automaticamente.

- [ ] Escrever testes para separação de tentativa/gabarito, presença das cinco alternativas, encerramento após alternativa E e campos obrigatórios de comentário jurisprudencial.
- [ ] Confirmar que os testes falham porque o avaliador não existe.
- [ ] Implementar somente verificações estruturais objetivas; marcar correção jurídica, unicidade material e qualidade do distrator para revisão humana.
- [ ] Executar testes focados e Ruff no arquivo.

### Task 0.3: registrar baseline 0.3.3

**Files:**

- Create: `plugins/magistratura-enam-br/evals/pedagogia/baseline-0.3.3.md`
- Modify: `plugins/magistratura-enam-br/CONTINUACAO.md`

**Interfaces:**

- Consumes: três execuções novas por caso, sem reaproveitar contexto entre execuções.
- Produces: taxas estruturais, julgamento humano, duração, tokens quando disponíveis e variância por caso.

- [ ] Executar os doze casos três vezes com a versão `0.3.3`.
- [ ] Aplicar a rubrica somente após capturar as saídas.
- [ ] Registrar resultados agregados, falhas recorrentes e limitações; não versionar respostas do candidato nem material protegido.
- [ ] Commit phase: `test(pedagogy): establish behavioral baseline`.

### Gate da fase 0

- 36 execuções registradas ou justificativa explícita para qualquer execução indisponível.
- Rubrica humana separada das verificações automáticas.
- Nenhuma mudança no comportamento das skills.

---

## Fase 1: criar contratos pedagógicos compartilhados

### Objetivo

Definir linguagem comum para atividades, resultados, erros, evidências e referências de conteúdo sem introduzir persistência ou adaptação.

### Task 1.1: documentar contrato e taxonomia

**Files:**

- Create: `plugins/magistratura-enam-br/references/contrato-pedagogico.md`
- Modify: `plugins/magistratura-enam-br/AGENTS.md`
- Test: `plugins/magistratura-enam-br/tests/test_contrato_pedagogico.py`

**Interfaces:**

- Produces: vocabulários exatos da spec para modalidades, resultados, erros e evidências de domínio.

- [ ] Escrever testes que rejeitem categorias ausentes, duplicadas ou divergentes da taxonomia v1.
- [ ] Confirmar falha antes da criação da referência.
- [ ] Criar a referência explicando quando cada categoria pode ser registrada e proibindo inferência de erro sem tentativa observável.
- [ ] Vincular o contrato em `AGENTS.md` sem duplicar toda a taxonomia.
- [ ] Executar o teste focado.

### Task 1.2: criar schemas versionados

**Files:**

- Create: `plugins/magistratura-enam-br/modelos/pedagogia/learning-event.schema.json`
- Create: `plugins/magistratura-enam-br/modelos/pedagogia/candidate-profile.schema.json`
- Create: `plugins/magistratura-enam-br/modelos/pedagogia/review-recommendation.schema.json`
- Test: `plugins/magistratura-enam-br/tests/test_schemas_pedagogicos.py`

**Interfaces:**

- `learning-event`: `schema_version`, `event_id`, `occurred_at`, `skill`, `content_ref`, `activity`, `performance`, `routing`.
- `candidate-profile`: `schema_version`, `updated_at`, `objectives`, `preferences`, `competencies`, `open_remediations`.
- `review-recommendation`: `policy`, `base_interval_days`, `suggested_interval_days`, `reason_codes`, `shadow_mode`.

- [ ] Criar fixtures válidas e inválidas antes dos schemas.
- [ ] Confirmar falha por arquivo ausente.
- [ ] Implementar schemas com `additionalProperties: false`, IDs estáveis e campos pessoais opcionais ou ausentes.
- [ ] Validar que comparação de material não pode registrar domínio ou erro do candidato.
- [ ] Validar que evento não exige resposta integral.
- [ ] Executar testes focados.

### Task 1.3: integrar contratos ao verificador

**Files:**

- Modify: `plugins/magistratura-enam-br/scripts/verificar_integracao.py`
- Modify: `plugins/magistratura-enam-br/tests/test_verificar_integracao.py`
- Modify: `plugins/magistratura-enam-br/README.md`

- [ ] Escrever teste que reprove ausência ou JSON inválido dos três schemas.
- [ ] Confirmar falha esperada.
- [ ] Acrescentar os artefatos ao conjunto essencial e validar sintaxe sem criar cache.
- [ ] Executar integração completa.
- [ ] Commit phase: `feat(pedagogy): define shared learning contracts`.

### Gate da fase 1

- Schemas aceitam fixtures válidas e rejeitam inferência indevida, categoria inválida e campo pessoal inesperado.
- Todas as quatro skills continuam produzindo exatamente os formatos anteriores.

---

## Fase 2: implementar log local e perfil reconstruível

### Objetivo

Permitir continuidade entre sessões sem memória fictícia, backend ou gravação silenciosa.

### Task 2.1: implementar log append-only

**Files:**

- Create: `plugins/magistratura-enam-br/scripts/eventos_aprendizagem.py`
- Test: `plugins/magistratura-enam-br/tests/test_eventos_aprendizagem.py`

**Interfaces:**

```python
def validar_evento(evento: dict) -> list[str]: ...
def acrescentar_evento(caminho: Path, evento: dict) -> None: ...
def ler_eventos(caminho: Path) -> list[dict]: ...
```

- [ ] Escrever testes para evento válido, schema inválido, linha JSON corrompida, `event_id` duplicado e caminho inexistente.
- [ ] Confirmar falhas antes da implementação.
- [ ] Implementar validação antes da escrita, UTF-8, uma linha por evento e `flush`/`fsync`.
- [ ] Recusar duplicidade sem alterar o arquivo.
- [ ] Não criar diretório pai sem opção explícita `--criar-diretorio`.
- [ ] Executar testes focados.

### Task 2.2: implementar projeção do perfil

**Files:**

- Create: `plugins/magistratura-enam-br/scripts/perfil_candidato.py`
- Test: `plugins/magistratura-enam-br/tests/test_perfil_candidato.py`

**Interfaces:**

```python
def reconstruir_perfil(eventos: Iterable[dict]) -> dict: ...
def salvar_perfil_atomico(caminho: Path, perfil: dict) -> None: ...
```

- [ ] Escrever testes para reconstrução determinística, ordenação fora de sequência, evento duplicado, competência independente por modalidade e remediação aberta/fechada.
- [ ] Confirmar falhas antes da implementação.
- [ ] Agregar evidências sem produzir nota global de domínio.
- [ ] Preservar histórico contraditório; a evidência mais recente não apaga a anterior.
- [ ] Gravar projeção por arquivo temporário no mesmo diretório e substituição atômica.
- [ ] Demonstrar que apagar o perfil e reconstruí-lo do log produz JSON semanticamente idêntico.

### Task 2.3: expor CLI explícita

**Files:**

- Modify: `plugins/magistratura-enam-br/scripts/eventos_aprendizagem.py`
- Modify: `plugins/magistratura-enam-br/scripts/perfil_candidato.py`
- Create: `plugins/magistratura-enam-br/references/persistencia-pedagogica-local.md`
- Test: `plugins/magistratura-enam-br/tests/test_cli_persistencia_pedagogica.py`

- [ ] Testar `validate`, `append`, `rebuild`, `export` e erros de caminho.
- [ ] Exigir `--log` e `--perfil`; não adotar caminho oculto padrão.
- [ ] Documentar exclusão separada de perfil e log e explicar que o perfil é reconstruível.
- [ ] Executar testes e validar que nenhum dado é enviado pela rede.
- [ ] Commit phase: `feat(pedagogy): add local learning history`.

### Gate da fase 2

- Nenhuma gravação ocorre sem comando e caminho explícitos.
- Log resiste a evento inválido ou duplicado sem corrupção.
- Perfil é reproduzível a partir do log.
- Nenhum dado pessoal é obrigatório.

---

## Fase 3: adaptar estudo, feedback e retenção

### Objetivo

Usar evidências disponibilizadas pelo candidato para ajustar a intervenção, mantendo o comportamento atual quando perfil ou opção adaptativa não existirem.

### Task 3.1: introduzir protocolo de ambientação

**Files:**

- Create: `plugins/magistratura-enam-br/skills/estudar-direito-magistratura/references/ambientacao-e-calibracao.md`
- Modify: `plugins/magistratura-enam-br/skills/estudar-direito-magistratura/SKILL.md`
- Test: `plugins/magistratura-enam-br/tests/test_ambientacao_estudo.py`

- [ ] Criar cenários para usuário novo com tema claro, usuário com perfil, perfil desatualizado e usuário que recusa persistência.
- [ ] Confirmar que o teste comportamental atual não distingue esses casos.
- [ ] Definir abertura sem interrogatório: usar pedido e material primeiro; fazer no máximo uma pergunta quando objetivo, modalidade ou profundidade forem realmente ambíguos.
- [ ] Permitir que o candidato informe resposta como letra simples ou como `resposta + confiança + fundamento`.
- [ ] Proibir inferir confiança, histórico ou domínio quando não fornecidos.

### Task 3.2: implementar feedback adaptativo opt-in

**Files:**

- Modify: `plugins/magistratura-enam-br/skills/estudar-direito-magistratura/references/questoes-fgv-enam.md`
- Modify: `plugins/magistratura-enam-br/skills/estudar-direito-magistratura/references/revisao.md`
- Modify: `plugins/magistratura-enam-br/skills/estudar-direito-magistratura/references/cenarios-avaliacao.md`
- Modify: `plugins/magistratura-enam-br/tests/test_contrato_questoes_fgv.py`

- [ ] Adicionar cenários equivalentes com feedback completo e adaptativo.
- [ ] Manter correção completa para erro, parcial, baixa confiança, ausência de justificativa, auditoria ou pedido expresso.
- [ ] Permitir correção compacta somente com opção expressa, alta confiança e fundamento correto.
- [ ] Preservar reconhecimento de questão inválida antes de avaliar desempenho.
- [ ] Comparar três execuções por cenário com o baseline 0.3.3 e rejeitar perda de precisão jurídica.

### Task 3.3: criar contrato de flashcards

**Files:**

- Create: `plugins/magistratura-enam-br/skills/estudar-direito-magistratura/references/flashcards-de-alto-rendimento.md`
- Modify: `plugins/magistratura-enam-br/skills/estudar-direito-magistratura/SKILL.md`
- Test: `plugins/magistratura-enam-br/tests/test_contrato_flashcards.py`

- [ ] Testar atomicidade, pergunta discriminativa, resposta independente, fonte identificável e ausência de cartão meramente opinativo.
- [ ] Exigir que cada cartão avalie uma decisão recuperável, não um resumo amplo.
- [ ] Limitar geração automática a três cartões e permitir omissão quando não houver ganho de retenção.
- [ ] Registrar evento somente se o cartão for efetivamente usado em tentativa posterior.
- [ ] Commit phase: `feat(study): add opt-in adaptive learning modes`.

### Gate da fase 3

- Sem perfil ou opt-in, saídas continuam compatíveis com `0.3.3`.
- Feedback adaptativo reduz extensão sem reduzir fundamento ou esconder erro.
- Flashcards são avaliáveis e não aumentam acervo por ritual.

---

## Fase 4: revisão adaptativa de jurisprudência em modo sombra

### Objetivo

Acrescentar recomendação baseada em resultado e confiança sem substituir imediatamente os ciclos fixos nem ampliar a skill para cronograma geral.

### Task 4.1: implementar política de recomendação

**Files:**

- Create: `plugins/magistratura-enam-br/skills/planejar-jurisprudencia/references/politica-adaptativa-v1.md`
- Create: `plugins/magistratura-enam-br/skills/planejar-jurisprudencia/scripts/recomendar_revisao.py`
- Test: `plugins/magistratura-enam-br/skills/planejar-jurisprudencia/tests/test_recomendar_revisao.py`

**Interfaces:**

```python
def recomendar_revisao(evento: dict, intervalo_fixo: int, modo_sombra: bool = True) -> dict: ...
```

- [ ] Criar testes tabelados para todas as linhas da política adaptativa v1 da spec.
- [ ] Confirmar falha antes da implementação.
- [ ] Implementar arredondamento para baixo, limite de 90 dias e `reason_codes` estáveis.
- [ ] Em modo sombra, retornar data sugerida sem alterar `proxima_revisao`.
- [ ] Rejeitar recomendação quando resultado, confiança ou evidência exigida estiverem ausentes.

### Task 4.2: migrar planilha de forma compatível

**Files:**

- Modify: `plugins/magistratura-enam-br/skills/planejar-jurisprudencia/scripts/atualizar_esteira.py`
- Modify: `plugins/magistratura-enam-br/skills/planejar-jurisprudencia/references/fluxo-da-esteira.md`
- Modify: `plugins/magistratura-enam-br/skills/planejar-jurisprudencia/tests/test_atualizar_esteira.py`

- [ ] Adicionar testes de abertura de planilha antiga sem novas colunas.
- [ ] Acrescentar ao final, sem renomear colunas existentes: `politica_revisao`, `confianca`, `transferencia`, `intervalo_sugerido`, `motivo_sugestao`.
- [ ] Usar `fixa` e campos vazios como migração padrão.
- [ ] Garantir que `status` permaneça somente leitura.
- [ ] Preservar sanitização de fórmulas e fechamento de workbook em todos os fluxos.

### Task 4.3: comparar política fixa e sombra

**Files:**

- Create: `plugins/magistratura-enam-br/evals/pedagogia/politica-revisao-v1.md`
- Modify: `plugins/magistratura-enam-br/CONTINUACAO.md`

- [ ] Executar fixtures sintéticas com acerto, parcial, erro, reincidência e transferência.
- [ ] Comparar datas, carga semanal e quantidade de remediações entre política fixa e sombra.
- [ ] Manter modo sombra se qualquer regra ampliar intervalo após evidência insuficiente.
- [ ] Commit phase: `feat(planner): add shadow adaptive review policy`.

### Gate da fase 4

- Planilhas antigas abrem e preservam dados.
- A política adaptativa não altera datas no modo sombra.
- Nenhuma atividade não jurisprudencial ingressa na esteira.

---

## Fase 5: fechar o ciclo entre as quatro skills

### Objetivo

Permitir transporte explícito e verificável de referências e resultados sem transformar uma skill em autoridade sobre outra.

### Task 5.1: padronizar referências de conteúdo

**Files:**

- Modify: `plugins/magistratura-enam-br/modelos/pedagogia/learning-event.schema.json`
- Modify: `plugins/magistratura-enam-br/skills/curar-informativos-stf-stj/modelos/precedentes.schema.json`
- Modify: `plugins/magistratura-enam-br/skills/comparar-materiais-enam/modelos/comparativo.schema.json`
- Test: `plugins/magistratura-enam-br/tests/test_integracao_referencias_pedagogicas.py`

- [ ] Definir `content_ref` com `kind`, `id`, `disciplina`, `tema`, `subtema`, `source_refs` e `source_state`.
- [ ] Testar conversão de precedente e delta documental sem perda de identificador ou fonte.
- [ ] Proibir que delta documental produza automaticamente erro ou nível de domínio.
- [ ] Manter compatibilidade com artefatos sem `content_ref` durante uma versão de migração.

### Task 5.2: consumir e concluir remediações

**Files:**

- Modify: `plugins/magistratura-enam-br/skills/estudar-direito-magistratura/SKILL.md`
- Modify: `plugins/magistratura-enam-br/skills/planejar-jurisprudencia/scripts/atualizar_esteira.py`
- Modify: `plugins/magistratura-enam-br/skills/planejar-jurisprudencia/tests/test_atualizar_esteira.py`
- Test: `plugins/magistratura-enam-br/tests/test_ciclo_remediacao.py`

- [ ] Criar fixture `revisao_julgado → erro → questao_objetiva → correto → remediacao_concluida`.
- [ ] Confirmar que o fluxo atual não fecha automaticamente a remediação.
- [ ] Fazer a skill de estudo produzir evento proposto com o mesmo `content_ref` e `remediation_id`.
- [ ] Fazer o planejador fechar remediação somente ao importar evento válido e explicitamente confirmado.
- [ ] Preservar remediação aberta diante de evento parcial, inválido ou referente a outro conteúdo.

### Task 5.3: integrar atualização de material

**Files:**

- Modify: `plugins/magistratura-enam-br/skills/comparar-materiais-enam/SKILL.md`
- Modify: `plugins/magistratura-enam-br/skills/comparar-materiais-enam/references/formato-entrega-comparativo.md`
- Test: `plugins/magistratura-enam-br/tests/test_delta_para_estudo.py`

- [ ] Permitir exportar evento `material_atualizado` apenas quando solicitado.
- [ ] Vincular ação `INCLUIR`, `SUBSTITUIR` ou `REVISAR` ao conteúdo, sem definir data ou prioridade automática.
- [ ] Encaminhar explicação da mudança à skill de estudo e agenda jurisprudencial somente quando o delta envolver julgado já presente na esteira.
- [ ] Commit phase: `feat(pedagogy): integrate learning and remediation flow`.

### Gate da fase 5

- O ciclo completo usa IDs e fontes preservados.
- Nenhuma remediação é fechada por inferência textual solta.
- Comparação documental não se converte em avaliação do candidato.

---

## Fase 6: orquestração fina, observabilidade e release

### Objetivo

Adicionar ambientação unificada apenas depois de os contratos estarem comprovados, medir a evolução contra o baseline e preparar instalação sem migração implícita.

### Task 6.1: criar skill de acompanhamento

**Files:**

- Create: `plugins/magistratura-enam-br/skills/acompanhar-percurso-magistratura/SKILL.md`
- Create: `plugins/magistratura-enam-br/skills/acompanhar-percurso-magistratura/agents/openai.yaml`
- Create: `plugins/magistratura-enam-br/skills/acompanhar-percurso-magistratura/references/roteamento.md`
- Test: `plugins/magistratura-enam-br/tests/test_roteamento_percurso.py`

**Interfaces:**

- Consumes: objetivo expresso, perfil opcional, remediações e referências de conteúdo.
- Produces: uma recomendação de skill, motivo, dados necessários e ação que depende de confirmação.

- [ ] Criar testes de acionamento positivo e near-miss para as cinco skills.
- [ ] Confirmar falha antes da nova skill.
- [ ] Implementar roteador sem conteúdo jurídico substantivo e sem escrita automática.
- [ ] Encaminhar agenda exclusivamente ao planejador e atualização documental exclusivamente ao comparador.
- [ ] Omitir qualquer alegação de histórico quando perfil/log não forem fornecidos.

### Task 6.2: acrescentar relatório local de aprendizagem

**Files:**

- Create: `plugins/magistratura-enam-br/scripts/relatorio_aprendizagem.py`
- Test: `plugins/magistratura-enam-br/tests/test_relatorio_aprendizagem.py`

**Interfaces:**

```python
def gerar_relatorio(eventos: Iterable[dict], periodo: tuple[date, date]) -> dict: ...
```

- [ ] Testar contagem de tentativas, precisão por modalidade, reincidência de erros, retenção observada e calibração de confiança.
- [ ] Não calcular ranking, pontuação global ou previsão de aprovação.
- [ ] Separar ausência de evidência de desempenho insuficiente.
- [ ] Produzir JSON e Markdown somente por pedido explícito.

### Task 6.3: executar avaliação comparativa final

**Files:**

- Create: `plugins/magistratura-enam-br/evals/pedagogia/relatorio-final.md`
- Modify: `plugins/magistratura-enam-br/evals/pedagogia/evals.json`

- [ ] Reexecutar os doze casos da fase 0 três vezes com a versão candidata.
- [ ] Acrescentar casos de persistência recusada, perfil contraditório, remediação cruzada e roteamento ambíguo.
- [ ] Comparar precisão, aderência às fronteiras, extensão, tokens, variância e notas humanas contra `0.3.3`.
- [ ] Bloquear release se houver regressão jurídica, vazamento de gabarito, inferência de memória ou fechamento indevido de remediação.

### Task 6.4: documentação, migração e release

**Files:**

- Modify: `plugins/magistratura-enam-br/.codex-plugin/plugin.json`
- Modify: `plugins/magistratura-enam-br/README.md`
- Modify: `plugins/magistratura-enam-br/AGENTS.md`
- Modify: `plugins/magistratura-enam-br/CHANGELOG.md`
- Modify: `plugins/magistratura-enam-br/CONTINUACAO.md`
- Modify: `plugins/magistratura-enam-br/scripts/verificar_integracao.py`
- Modify: `.github/workflows/validar.yml`

- [ ] Documentar instalação sem perfil e ativação opcional de persistência.
- [ ] Documentar migração de planilha com política `fixa` padrão e modo sombra.
- [ ] Atualizar capacidades e prompts iniciais sem prometer memória automática.
- [ ] Incluir todos os novos testes no workflow.
- [ ] Sincronizar versão no manifesto, `pyproject.toml` e `uv.lock`.
- [ ] Executar os gates finais abaixo.
- [ ] Commit phase: `feat(plugin): release integrated pedagogical environment`.

### Gates finais

```powershell
uv sync --all-groups
uv lock --check
uv run python -m pytest tests skills/planejar-jurisprudencia/tests skills/comparar-materiais-enam/tests skills/curar-informativos-stf-stj/tests
uv run ruff check .
uv run python scripts/verificar_integracao.py
uv run python "C:\Users\Boni Jr\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" .
```

Além dos comandos:

- executar avaliações comportamentais em sessões novas;
- aplicar rubrica jurídica sem revelar critérios ao agente antes da saída;
- comparar com o baseline `0.3.3`;
- inspecionar instalação limpa do plugin;
- confirmar que nenhum perfil ou log é criado sem comando explícito.

### Gate da fase 6

- Ciclo completo rastreável e local.
- Nenhuma regressão nas quatro skills originais.
- Roteamento correto nos casos positivos e near-miss.
- Relatório distingue falta de evidência de desempenho insuficiente.
- Release somente após aprovação técnica e revisão humana dos evals.

---

## Ordem de execução e dependências

1. Fase 0 não depende de mudança estrutural e deve congelar o baseline antes de qualquer edição de prompt.
2. Fase 1 define contratos consumidos por todas as fases posteriores.
3. Fase 2 implementa persistência, mas nenhuma skill passa a exigi-la.
4. Fase 3 pode consumir perfil; sem ele, preserva o comportamento atual.
5. Fase 4 depende dos eventos da fase 2 e opera primeiro em sombra.
6. Fase 5 depende dos schemas e IDs estabilizados nas fases 1 a 4.
7. Fase 6 somente começa depois de o ciclo da fase 5 passar por avaliação comportamental.

Cada fase deve permanecer em commit próprio e pode ser publicada separadamente. Falha em uma fase não autoriza antecipar a seguinte nem contornar seu gate.
