# Profissionalização Pedagógica Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Entregar a versão 0.6.0 do plugin como ambiente jurídico despersonificado, fluido e especializado, com frentes didáticas próprias, estudo dogmático integrado e perfil individual local consentido.

**Architecture:** Manter as cinco skills públicas e a infraestrutura local da versão 0.5.0. Concentrar invariantes em contratos compartilhados, mover regras especializadas para referências próprias de cada frente e evoluir eventos/perfis de modo retrocompatível. Validar primeiro os contratos observáveis, depois os artefatos determinísticos e, por fim, cenários jurídicos com rubrica humana.

**Tech Stack:** Markdown de skills, JSON Schema Draft 2020-12, Python 3.14, `uv`, `pytest`, `jsonschema`, Ruff, MkDocs/Zensical.

**Spec:** `docs/superpowers/specs/2026-09-05-profissionalizacao-pedagogica-design.md`

## Global Constraints

- Público pressuposto: bacharéis em Direito em preparação de alta complexidade para Magistratura e ENAM.
- Higiene significa preservar, aprofundar, realocar, generalizar ou remover com cobertura comprovada; contagem de linhas não é métrica de qualidade.
- A conversa começa pelo pedido disponível e formula no máximo uma pergunta realmente discriminante antes de agir.
- Não adicionar MCP, conta, nuvem, telemetria ou caminho oculto.
- Perfil individual: opcional, local, reconstruível e dependente de autorização explícita para cada escrita.
- Carregar perfil não autoriza gravação.
- Fontes jurídicas temporalmente sensíveis devem ser oficiais e rastreáveis.
- Não versionar material pessoal, respostas reais ou dados de candidatos.
- Manter compatibilidade de leitura com eventos `1.0.0` e `1.1.0`.
- Python `>=3.14,<3.15`; usar `uv`, nunca `pip`.
- Usar `--basetemp .test-tmp/<gate>` nos testes para evitar o diretório temporário global bloqueado no Windows.
- Cada commit previsto abaixo é um gate local; push, PR, merge e release permanecem ações separadas.

---

### Task 1: Inventário de regras e baseline de despersonificação

**Files:**
- Create: `docs/superpowers/audits/2026-09-05-inventario-regras-pedagogicas.md`
- Create: `plugins/magistratura-enam-br/tests/test_despersonificacao_plugin.py`
- Modify: `plugins/magistratura-enam-br/evals/pedagogia/README.md`

**Interfaces:**
- Consumes: estrutura e testes da versão 0.5.0.
- Produces: matriz `regra | origem | finalidade | operação | destino | cobertura` e gate automatizado contra defaults pessoais conhecidos.

- [ ] **Step 1: Registrar o baseline técnico antes de editar**

Run:

```powershell
Set-Location plugins/magistratura-enam-br
uv sync --all-groups
uv run python -m pytest tests skills/planejar-jurisprudencia/tests skills/comparar-materiais-enam/tests skills/curar-informativos-stf-stj/tests --basetemp .test-tmp/profissionalizacao-task-1
uv run ruff check .
uv run python scripts/verificar_integracao.py
```

Expected: 207 testes aprovados, Ruff sem erro e integração aprovada. Se a contagem mudar por coleta do pytest, registrar a nova contagem e exigir zero falhas.

- [ ] **Step 2: Escrever o teste de despersonificação**

Create `tests/test_despersonificacao_plugin.py`:

```python
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARQUIVOS_DISTRIBUIDOS = (
    ROOT / "AGENTS.md",
    ROOT / ".codex-plugin" / "plugin.json",
    ROOT / "README.md",
    *sorted((ROOT / "skills").glob("*/SKILL.md")),
    *sorted((ROOT / "skills").glob("*/references/*.md")),
)

DEFAULTS_PESSOAIS_PROIBIDOS = (
    "50% ciclo geral",
    "25% recuperação",
    "empresarial/humanística/direitos humanos",
    "na última vez em que fizemos essa escolha",
    "seu estágio atual",
)


def test_distribuicao_nao_embute_percurso_pessoal_do_autor():
    corpus = "\n".join(path.read_text(encoding="utf-8").casefold() for path in ARQUIVOS_DISTRIBUIDOS)
    for trecho in DEFAULTS_PESSOAIS_PROIBIDOS:
        assert trecho.casefold() not in corpus


def test_plugin_continua_especializado_em_bachareis_e_magistratura():
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8").casefold()
    assert "bachar" in agents
    assert "magistratura" in agents
    assert "não simplifique" in agents
```

- [ ] **Step 3: Executar o novo teste e confirmar a falha útil**

Run:

```powershell
uv run python -m pytest tests/test_despersonificacao_plugin.py -v --basetemp .test-tmp/profissionalizacao-task-1-red
```

Expected: o teste de especialização falha porque `AGENTS.md` ainda não declara o público e a vedação com o contrato novo; o teste de defaults pessoais pode passar e funciona como regressão.

- [ ] **Step 4: Produzir o inventário sem excluir regras**

Create `docs/superpowers/audits/2026-09-05-inventario-regras-pedagogicas.md` com estas seções e classificações:

```markdown
# Inventário de regras pedagógicas da versão 0.5.0

| Regra | Origem | Finalidade | Operação | Destino canônico | Cobertura |
|---|---|---|---|---|---|
| Precisão e atualização jurídica | `AGENTS.md` | Segurança jurídica transversal | preservar | `AGENTS.md` | `test_fontes_por_skill.py` |
| Fluidez e uma pergunta discriminante | ambientações | Evitar interrogatório | realocar | `contrato-fluxos-conversacionais.md` | `test_ambientacao_estudo.py` |
| Progressão do estudo dogmático | `SKILL.md` e `explicacao-e-integracao.md` | Formação conceitual | aprofundar | `explicacao-e-integracao.md` | novo gate dogmático |
| Cinco alternativas e chave única | estudo e questões | Validade objetiva | preservar | `questoes-fgv-enam.md` | `test_contrato_questoes_fgv.py` |
| Discursiva e oral no mesmo arquivo | `discursivas-e-prova-oral.md` | Orientação das duas modalidades | realocar | referências separadas | novos gates por modalidade |
| Eventos append-only | scripts e contrato | Reconstrução local | preservar | scripts/schemas | testes de eventos |
| Preferência `completo` criada por default | `perfil_candidato.py` | Completar schema | generalizar | configuração explícita ou ausência | testes de perfil v2 |
```

Completar a tabela com todas as regras substantivas de `AGENTS.md`, dos cinco `SKILL.md` e de suas referências. Toda linha classificada como `remover` deve indicar a regra canônica que conserva sua capacidade; sem esse vínculo, reclassificar como `preservar`.

- [ ] **Step 5: Documentar o regime de avaliação**

Append to `evals/pedagogia/README.md`:

```markdown
## Profissionalização 0.6.0

Testes literais protegem somente contratos textuais e proibições objetivamente enumeráveis. Profundidade dogmática, função das fontes, plausibilidade de soluções e qualidade de correção exigem rubrica semântica e revisão jurídica humana. Nenhum caso versionado contém material ou desempenho pessoal de candidato.
```

- [ ] **Step 6: Commit do inventário e do gate inicial**

```powershell
git add docs/superpowers/audits/2026-09-05-inventario-regras-pedagogicas.md plugins/magistratura-enam-br/tests/test_despersonificacao_plugin.py plugins/magistratura-enam-br/evals/pedagogia/README.md
git commit -m "test(pedagogy): inventory professionalization invariants"
```

### Task 2: Contratos transversais e orquestração neutra

**Files:**
- Modify: `plugins/magistratura-enam-br/AGENTS.md`
- Modify: `plugins/magistratura-enam-br/references/contrato-fluxos-conversacionais.md`
- Modify: `plugins/magistratura-enam-br/references/contrato-pedagogico.md`
- Modify: `plugins/magistratura-enam-br/skills/acompanhar-percurso-magistratura/SKILL.md`
- Modify: `plugins/magistratura-enam-br/skills/acompanhar-percurso-magistratura/references/ambientacao-conversacional.md`
- Modify: `plugins/magistratura-enam-br/skills/acompanhar-percurso-magistratura/references/roteamento.md`
- Modify: `plugins/magistratura-enam-br/tests/test_ambientacao_plugin.py`
- Modify: `plugins/magistratura-enam-br/tests/test_roteamento_percurso.py`
- Modify: `plugins/magistratura-enam-br/tests/test_contrato_fluxos_conversacionais.py`

**Interfaces:**
- Consumes: inventário da Task 1.
- Produces: invariantes canônicas `publico_juridico`, `fluidez`, `perfil_opcional` e roteamento para as cinco skills existentes.

- [ ] **Step 1: Escrever testes para o contrato transversal**

Adicionar aos testes correspondentes:

```python
def test_contrato_preserva_estrutura_interna_e_fluidez_externa(texto):
    contrato = texto("references/contrato-fluxos-conversacionais.md").casefold()
    assert "estrutura interna" in contrato
    assert "fluidez externa" in contrato
    assert "no máximo uma pergunta" in contrato
    assert "menu obrigatório" in contrato


def test_orquestrador_nao_presume_banca_disciplina_ou_percurso(texto):
    skill = texto("skills/acompanhar-percurso-magistratura/SKILL.md").casefold()
    for conceito in ("não presuma banca", "não presuma disciplina", "não presuma percurso"):
        assert conceito in skill


def test_orquestrador_usa_perfil_como_evidencia_auxiliar(texto):
    skill = texto("skills/acompanhar-percurso-magistratura/SKILL.md").casefold()
    assert "evidência auxiliar" in skill
    assert "instrução atual prevalece" in skill
```

- [ ] **Step 2: Confirmar que os novos contratos ainda não estão completos**

Run:

```powershell
uv run python -m pytest tests/test_ambientacao_plugin.py tests/test_roteamento_percurso.py tests/test_contrato_fluxos_conversacionais.py tests/test_despersonificacao_plugin.py -v --basetemp .test-tmp/profissionalizacao-task-2-red
```

Expected: falhas nos novos testes de público, fluidez ou neutralidade.

- [ ] **Step 3: Consolidar invariantes em `AGENTS.md`**

Inserir uma seção inicial `## Identidade e público` com o texto normativo:

```markdown
O plugin é especializado em estudo jurídico brasileiro de alta complexidade para bacharéis em Direito, especialmente candidatos à Magistratura e ao ENAM. Presuma formação jurídica básica, salvo lacuna demonstrada. Não simplifique institutos a ponto de perder requisitos, exceções, controvérsias ou precisão terminológica.

Nenhum exemplo, recomendação ou default distribuído pode pressupor banca, disciplina vulnerável, percentual de ciclo, percurso anterior ou preferência do autor. Dados individuais só orientam a resposta quando estiverem presentes na sessão ou em perfil local que o usuário tenha escolhido utilizar.
```

Realocar as repetições sobre perguntas, transições e perfil para os contratos compartilhados, mantendo em `AGENTS.md` uma única regra de remissão. Conferir cada remoção contra o inventário.

- [ ] **Step 4: Formalizar fluidez e neutralidade nos contratos**

Adicionar a `contrato-fluxos-conversacionais.md`:

```markdown
## Estrutura interna e fluidez externa

As skills podem manter estado e critérios internos rigorosos, mas respondem em linguagem natural. Use primeiro pedido, contexto, material e perfil autorizado. Se um dado indispensável continuar ambíguo, faça no máximo uma pergunta discriminante; não abra menu, formulário, diagnóstico ou entrevista compulsórios.
```

Adicionar a `contrato-pedagogico.md`:

```markdown
## Personalização opcional

O uso sem perfil é completo. Perfil local é evidência auxiliar: a instrução atual prevalece, evidência antiga não cristaliza fraqueza e leitura não autoriza escrita. Preferências declaradas e inferências de desempenho são categorias distintas.
```

- [ ] **Step 5: Ajustar orquestração e ambientação**

Manter exatamente as cinco skills públicas. Alterar a ambientação para mencionar as frentes de forma natural apenas em pedido realmente genérico. Incluir no `SKILL.md`:

```markdown
Não presuma banca, não presuma disciplina e não presuma percurso anterior. Quando houver perfil local fornecido e escolhido para a sessão, trate-o como evidência auxiliar; a instrução atual prevalece sobre preferência ou inferência histórica.
```

- [ ] **Step 6: Executar o gate de orquestração**

Run:

```powershell
uv run python -m pytest tests/test_ambientacao_plugin.py tests/test_roteamento_percurso.py tests/test_contrato_fluxos_conversacionais.py tests/test_transicoes_rota.py tests/test_despersonificacao_plugin.py -v --basetemp .test-tmp/profissionalizacao-task-2
```

Expected: PASS.

- [ ] **Step 7: Commit dos contratos transversais**

```powershell
git add plugins/magistratura-enam-br/AGENTS.md plugins/magistratura-enam-br/references plugins/magistratura-enam-br/skills/acompanhar-percurso-magistratura plugins/magistratura-enam-br/tests
git commit -m "refactor(plugin): neutralize shared pedagogical contracts"
```

### Task 3: Estudo dogmático integrado e casos complexos

**Files:**
- Modify: `plugins/magistratura-enam-br/skills/estudar-direito-magistratura/SKILL.md`
- Modify: `plugins/magistratura-enam-br/skills/estudar-direito-magistratura/references/explicacao-e-integracao.md`
- Create: `plugins/magistratura-enam-br/skills/estudar-direito-magistratura/references/casos-complexos.md`
- Create: `plugins/magistratura-enam-br/tests/test_estudo_dogmatico_integrado.py`
- Create: `plugins/magistratura-enam-br/tests/test_casos_complexos.py`
- Modify: `plugins/magistratura-enam-br/tests/test_ambientacao_estudo.py`

**Interfaces:**
- Consumes: contrato de fontes, protocolo do acervo e fluidez da Task 2.
- Produces: quatro contextos (`resposta_pontual`, `sessao_aprofundada`, `revisao`, `sintese`) e protocolo de caso complexo.

- [ ] **Step 1: Escrever gates estruturais do estudo dogmático**

Create `tests/test_estudo_dogmatico_integrado.py`:

```python
def test_estudo_distingue_contextos_sem_impor_template(texto):
    referencia = texto("skills/estudar-direito-magistratura/references/explicacao-e-integracao.md").casefold()
    for contexto in ("resposta pontual", "sessão aprofundada", "revisão", "síntese"):
        assert contexto in referencia
    assert "não são seções obrigatórias" in referencia


def test_norma_e_jurisprudencia_entram_na_construcao_dogmatica(texto):
    referencia = texto("skills/estudar-direito-magistratura/references/explicacao-e-integracao.md").casefold()
    for funcao in ("institui", "delimita", "excepciona", "define", "restringe", "atualiza", "aplica"):
        assert funcao in referencia
    assert "fontes jurisprudenciais oficiais" in referencia
    assert "ao final de cada resposta" in referencia
    assert "desfile de artigos" in referencia


def test_sessao_e_cumulativa_sem_despejo_editorial(texto):
    referencia = texto("skills/estudar-direito-magistratura/references/explicacao-e-integracao.md").casefold()
    assert "unidade intelectualmente completa" in referencia
    assert "prepara o núcleo seguinte" in referencia
    assert "não reinicie" in referencia
    assert "glossário" in referencia
```

- [ ] **Step 2: Escrever gates do caso complexo**

Create `tests/test_casos_complexos.py`:

```python
def test_caso_complexo_exige_fatos_funcionais_e_solucoes_concorrentes(texto):
    referencia = texto("skills/estudar-direito-magistratura/references/casos-complexos.md").casefold()
    for requisito in ("fatos funcionalmente relevantes", "questões jurídicas", "soluções concorrentes", "pressuposto decisivo", "entendimento prevalente"):
        assert requisito in referencia


def test_correcao_classifica_a_origem_do_erro(texto):
    referencia = texto("skills/estudar-direito-magistratura/references/casos-complexos.md").casefold()
    for erro in ("identificação", "enquadramento", "fonte", "inferência", "conclusão"):
        assert erro in referencia
```

- [ ] **Step 3: Confirmar a falha dos novos contratos**

Run:

```powershell
uv run python -m pytest tests/test_estudo_dogmatico_integrado.py tests/test_casos_complexos.py -v --basetemp .test-tmp/profissionalizacao-task-3-red
```

Expected: FAIL porque os contratos ainda não contêm todos os contextos e `casos-complexos.md` não existe.

- [ ] **Step 4: Reescrever a referência dogmática em torno do problema jurídico**

Estruturar `explicacao-e-integracao.md` com estes títulos:

```markdown
# Estudo dogmático integrado
## Escolha do contexto
## Mapa conceitual interno
## Unidade de desenvolvimento
## Integração funcional das fontes
## Ritmo e continuidade
## Fechamento e base consultada
## Antipadrões
```

Na `Unidade de desenvolvimento`, fixar a sequência interna problema/distinção → categoria dogmática → dispositivo pertinente → precedente funcional → consequência/limite → conexão. Declarar que esses elementos não são seções obrigatórias da resposta. Em `Antipadrões`, vedar sinopse substitutiva, glossário, texto editorial exaustivo, bloco jurisprudencial isolado e desfile de artigos ou julgados.

- [ ] **Step 5: Criar o protocolo de casos complexos**

`casos-complexos.md` deve conter:

```markdown
# Casos jurídicos complexos

Construa o caso com fatos funcionalmente relevantes. A dificuldade decorre da concorrência entre qualificações, regimes ou consequências, não de ruído narrativo.

## Construção
1. Defina a questão jurídica central e as questões subordinadas.
2. Vincule cada fato a uma função na solução.
3. Identifique fontes capazes de sustentar as soluções concorrentes.
4. Determine o pressuposto decisivo que muda o resultado.

## Resolução e correção
Exponha regra, aplicação e consequência. Quando houver pluralidade defensável, identifique o entendimento prevalente ou mais atual e o pressuposto de cada alternativa. Classifique o erro do candidato como identificação, enquadramento, fonte, inferência ou conclusão antes de remediá-lo.
```

- [ ] **Step 6: Atualizar o roteamento interno da skill de estudo**

Substituir a orientação genérica de `sessão aprofundada` por seleção explícita entre os quatro contextos. Acrescentar `casos-complexos.md` para pedidos de resolução, construção ou treino por caso; conservar julgados já selecionados em `explicacao-e-integracao.md`.

- [ ] **Step 7: Executar gates da frente central**

Run:

```powershell
uv run python -m pytest tests/test_estudo_dogmatico_integrado.py tests/test_casos_complexos.py tests/test_ambientacao_estudo.py tests/test_fontes_por_skill.py tests/test_contrato_flashcards.py -v --basetemp .test-tmp/profissionalizacao-task-3
```

Expected: PASS.

- [ ] **Step 8: Commit do eixo dogmático**

```powershell
git add plugins/magistratura-enam-br/skills/estudar-direito-magistratura plugins/magistratura-enam-br/tests
git commit -m "feat(study): integrate dogmatics statutes and precedents"
```

### Task 4: Objetiva, discursiva, oral, revisão e remediação

**Files:**
- Modify: `plugins/magistratura-enam-br/skills/estudar-direito-magistratura/references/questoes-fgv-enam.md`
- Delete: `plugins/magistratura-enam-br/skills/estudar-direito-magistratura/references/discursivas-e-prova-oral.md`
- Create: `plugins/magistratura-enam-br/skills/estudar-direito-magistratura/references/discursivas.md`
- Create: `plugins/magistratura-enam-br/skills/estudar-direito-magistratura/references/prova-oral.md`
- Modify: `plugins/magistratura-enam-br/skills/estudar-direito-magistratura/references/revisao.md`
- Modify: `plugins/magistratura-enam-br/skills/estudar-direito-magistratura/SKILL.md`
- Create: `plugins/magistratura-enam-br/tests/test_frentes_aplicadas.py`
- Modify: `plugins/magistratura-enam-br/tests/test_contrato_questoes_fgv.py`
- Modify: `plugins/magistratura-enam-br/tests/test_ciclo_remediacao.py`

**Interfaces:**
- Consumes: taxonomia pedagógica v1 e estudo/casos da Task 3.
- Produces: contratos independentes para objetiva, discursiva, oral e revisão, sem criar novas skills públicas.

- [ ] **Step 1: Escrever os testes das modalidades especializadas**

Create `tests/test_frentes_aplicadas.py`:

```python
def test_objetiva_distingue_treino_simulado_e_remediacao(texto):
    referencia = texto("skills/estudar-direito-magistratura/references/questoes-fgv-enam.md").casefold()
    for modo in ("treino", "simulado", "remediação"):
        assert modo in referencia
    assert "hipótese independente" in referencia


def test_discursiva_distingue_indispensavel_excelencia_e_acessorio(texto):
    referencia = texto("skills/estudar-direito-magistratura/references/discursivas.md").casefold()
    for criterio in ("atendimento ao comando", "aplicação aos fatos", "objeções", "economia argumentativa"):
        assert criterio in referencia
    for faixa in ("indispensável", "excelência", "acessório"):
        assert faixa in referencia


def test_oral_usa_repregunta_adaptativa_sem_simular_avaliacao_acustica(texto):
    referencia = texto("skills/estudar-direito-magistratura/references/prova-oral.md").casefold()
    assert "uma pergunta por vez" in referencia
    assert "repregunta" in referencia
    assert "ao final do ciclo" in referencia
    assert "não avalie voz" in referencia


def test_revisao_separa_assistencia_transferencia_e_retencao(texto):
    referencia = texto("skills/estudar-direito-magistratura/references/revisao.md").casefold()
    for estado in ("com assistência", "transferência independente", "retenção posterior"):
        assert estado in referencia
```

- [ ] **Step 2: Confirmar a falha seletiva**

Run:

```powershell
uv run python -m pytest tests/test_frentes_aplicadas.py -v --basetemp .test-tmp/profissionalizacao-task-4-red
```

Expected: FAIL nos contratos ainda ausentes, preservando os testes antigos de questões.

- [ ] **Step 3: Especializar os quatro contratos**

Em `questoes-fgv-enam.md`, conservar integralmente a trava de cinco alternativas, chave única, paralelismo, auditoria e correção completa do simulado. Acrescentar definições operacionais:

```markdown
- Treino: focaliza uma estrutura jurídica e admite intervenção pedagógica depois da tentativa.
- Simulado: preserva condições de prova e entrega correção completa somente depois da resposta.
- Remediação: transfere a estrutura do erro para hipótese independente; não parafraseia o item anterior.
```

Em `discursivas.md`, definir comando, problemas, fundamento, aplicação, objeções, conclusão e economia; o espelho separa indispensável, excelência e acessório. Em `prova-oral.md`, definir uma pergunta por vez, repregunta adaptativa e correção principal ao final do ciclo; em texto, incluir literalmente `não avalie voz, ritmo acústico ou linguagem corporal`. Em `revisao.md`, distinguir assistência, transferência independente e retenção posterior.

- [ ] **Step 4: Atualizar referências e remover o arquivo combinado**

No `SKILL.md`, trocar a leitura de `discursivas-e-prova-oral.md` pelas duas novas referências. Executar:

```powershell
rg -n "discursivas-e-prova-oral" plugins/magistratura-enam-br
```

Expected: nenhuma ocorrência depois da migração.

- [ ] **Step 5: Executar gates das modalidades**

Run:

```powershell
uv run python -m pytest tests/test_frentes_aplicadas.py tests/test_contrato_questoes_fgv.py tests/test_ciclo_remediacao.py tests/test_correcao_proporcional.py -v --basetemp .test-tmp/profissionalizacao-task-4
```

Expected: PASS.

- [ ] **Step 6: Commit das modalidades**

```powershell
git add -A plugins/magistratura-enam-br/skills/estudar-direito-magistratura plugins/magistratura-enam-br/tests
git commit -m "refactor(study): specialize applied learning modes"
```

### Task 5: Refinamento conservador das skills maduras

**Files:**
- Modify: `plugins/magistratura-enam-br/skills/curar-informativos-stf-stj/SKILL.md`
- Modify: `plugins/magistratura-enam-br/skills/curar-informativos-stf-stj/references/comentario-jurisprudencial.md`
- Modify: `plugins/magistratura-enam-br/skills/planejar-jurisprudencia/SKILL.md`
- Modify: `plugins/magistratura-enam-br/skills/planejar-jurisprudencia/references/politica-adaptativa-v1.md`
- Modify: `plugins/magistratura-enam-br/skills/comparar-materiais-enam/SKILL.md`
- Modify: `plugins/magistratura-enam-br/skills/comparar-materiais-enam/references/formato-entrega-comparativo.md`
- Create: `plugins/magistratura-enam-br/tests/test_especializacao_frentes_maduras.py`

**Interfaces:**
- Consumes: contratos compartilhados da Task 2; não altera schemas de boletim, planilha ou comparação.
- Produces: proporcionalidade de curadoria, prioridade pedagógica não cristalizada e comparação orientada à decisão.

- [ ] **Step 1: Escrever testes de preservação e ganho**

Create `tests/test_especializacao_frentes_maduras.py`:

```python
def test_curadoria_preserva_campos_e_evitar_burocracia(texto):
    referencia = texto("skills/curar-informativos-stf-stj/references/comentario-jurisprudencial.md").casefold()
    for campo in ("tese", "contexto", "fundamento determinante", "alcance", "limites", "distinções", "situação processual"):
        assert campo in referencia
    assert "proporcional" in referencia
    assert "inferência" in referencia


def test_planejamento_nao_cristaliza_evidencia_historica(texto):
    politica = texto("skills/planejar-jurisprudencia/references/politica-adaptativa-v1.md").casefold()
    assert "assistência" in politica
    assert "transferência" in politica
    assert "retenção" in politica
    assert "não cristal" in politica


def test_comparacao_distingue_tres_classes_de_mudanca(texto):
    formato = texto("skills/comparar-materiais-enam/references/formato-entrega-comparativo.md").casefold()
    for classe in ("ausência aparente", "mudança editorial", "alteração jurídica"):
        assert classe in formato
    assert "ação de estudo" in formato
```

- [ ] **Step 2: Confirmar que os refinamentos ainda faltam**

Run:

```powershell
uv run python -m pytest tests/test_especializacao_frentes_maduras.py -v --basetemp .test-tmp/profissionalizacao-task-5-red
```

Expected: ao menos um teste falha por ausência dos novos critérios.

- [ ] **Step 3: Refinar sem mudar formatos determinísticos**

Curadoria: preservar todos os campos existentes e declarar que a extensão de cada campo é proporcional à sua função; separar conteúdo expresso, síntese do curador e inferência. Planejamento: preservar ciclos fixos e modo sombra; usar assistência, transferência e retenção apenas para sugestão, sem cristalizar evidência antiga. Comparação: manter originais, IDs e ações existentes; distinguir ausência aparente, mudança editorial e alteração jurídica antes da ação de estudo.

- [ ] **Step 4: Executar testes das três skills**

Run:

```powershell
uv run python -m pytest tests/test_especializacao_frentes_maduras.py tests/test_curadoria_estrutura.py tests/test_contrato_comparador_entrega.py skills/planejar-jurisprudencia/tests skills/comparar-materiais-enam/tests skills/curar-informativos-stf-stj/tests -v --basetemp .test-tmp/profissionalizacao-task-5
```

Expected: PASS, sem mudança nos schemas públicos das três skills.

- [ ] **Step 5: Commit dos refinamentos conservadores**

```powershell
git add plugins/magistratura-enam-br/skills plugins/magistratura-enam-br/tests/test_especializacao_frentes_maduras.py
git commit -m "refactor(pedagogy): specialize mature study fronts"
```

### Task 6: Eventos v2 e perfil derivado sem defaults pessoais

**Files:**
- Modify: `plugins/magistratura-enam-br/modelos/pedagogia/learning-event.schema.json`
- Modify: `plugins/magistratura-enam-br/modelos/pedagogia/candidate-profile.schema.json`
- Create: `plugins/magistratura-enam-br/modelos/pedagogia/profile-settings.schema.json`
- Modify: `plugins/magistratura-enam-br/scripts/perfil_candidato.py`
- Modify: `plugins/magistratura-enam-br/scripts/verificar_integracao.py`
- Modify: `plugins/magistratura-enam-br/tests/test_schemas_pedagogicos.py`
- Modify: `plugins/magistratura-enam-br/tests/test_perfil_candidato.py`
- Modify: `plugins/magistratura-enam-br/tests/test_verificar_integracao.py`

**Interfaces:**
- Consumes: eventos v1.0.0/v1.1.0 e `reconstruir_perfil(eventos)` existentes.
- Produces: eventos `2.0.0`, configuração explícita v1, perfil `2.0.0` e assinatura retrocompatível `reconstruir_perfil(eventos, configuracao=None)`.

- [ ] **Step 1: Escrever fixtures v2 e testes de compatibilidade**

Adicionar a `test_schemas_pedagogicos.py` uma fixture com:

```python
EVENTO_V2 = {
    "schema_version": "2.0.0",
    "event_id": "evt_21a06d61-62eb-71f1-b7c0-5e19a67c47dc",
    "occurred_at": "2026-09-05T12:00:00Z",
    "skill": "estudar-direito-magistratura",
    "content_ref": {
        "kind": "questao",
        "id": "civil-prescricao-001",
        "disciplina": "Direito Civil",
        "tema": "Prescrição e decadência",
        "subtema": "Termo inicial",
        "source_refs": ["CC-art-189"],
        "source_state": "verificada",
        "source_version": "2026-09-05",
    },
    "activity": {
        "activity_id": "atividade-civil-prescricao-001",
        "modality": "questao_objetiva",
        "attempt_observed": True,
        "assistance_level": "nenhuma",
    },
    "performance": {
        "result": "correto",
        "error_types": [],
        "domain_evidence": ["aplicacao_fatos_novos"],
        "confidence": None,
    },
    "routing": {"target_skill": None, "reason_codes": []},
}
```

Testar que v1.0.0, v1.1.0 e v2.0.0 validam; v2 sem `activity_id`, `source_version` ou `assistance_level` falha.

- [ ] **Step 2: Escrever testes da projeção v2**

Adicionar a `test_perfil_candidato.py`:

```python
def test_perfil_v2_separa_preferencias_explicitas_de_inferencias():
    configuracao = {
        "schema_version": "1.0.0",
        "objectives": ["Magistratura estadual"],
        "preferences": {"feedback_mode": "adaptativo", "preferred_modalities": ["questao_objetiva"]},
    }
    reconstruido = perfil.reconstruir_perfil([], configuracao)
    assert reconstruido["schema_version"] == "2.0.0"
    assert reconstruido["declared"] == configuracao
    assert reconstruido["competencies"] == []


def test_acerto_assistido_nao_demonstra_transferencia_autonoma():
    item = copy.deepcopy(EVENTO_V2)
    item["activity"]["assistance_level"] = "conducao_completa"
    item["performance"]["domain_evidence"] = ["aplicacao_fatos_novos"]
    competencia = perfil.reconstruir_perfil([item])["competencies"][0]
    assert competencia["evidence"]["aplicacao_fatos_novos"] == "em_desenvolvimento"


def test_chave_de_competencia_aceita_content_ref_novo_e_legado():
    assert perfil.reconstruir_perfil([evento(), copy.deepcopy(EVENTO_V2)])["competencies"]
```

Adicionar `import copy` ao arquivo de teste. A função `evento()` já existente fornece o evento legado.

- [ ] **Step 3: Executar os testes para obter falhas v2**

Run:

```powershell
uv run python -m pytest tests/test_schemas_pedagogicos.py tests/test_perfil_candidato.py tests/test_verificar_integracao.py -v --basetemp .test-tmp/profissionalizacao-task-6-red
```

Expected: FAIL nas versões, campos e assinatura ainda não implementados.

- [ ] **Step 4: Evoluir os schemas com condicionais por versão**

No evento, adicionar `2.0.0` ao enum. Para `schema_version == 2.0.0`, exigir:

```json
{
  "content_ref.source_version": "string não vazia",
  "activity.activity_id": "^[a-z0-9][a-z0-9-]{2,127}$",
  "activity.assistance_level": ["nenhuma", "pista", "orientacao_parcial", "conducao_completa"]
}
```

No perfil, aceitar somente `2.0.0` na nova projeção e adicionar `declared`, contendo exatamente um objeto válido pelo novo `profile-settings.schema.json`. O schema de settings terá `schema_version`, `objectives` e `preferences`; não admitirá nome, CPF, matrícula, e-mail ou propriedades adicionais.

- [ ] **Step 5: Implementar reconstrução retrocompatível**

Adicionar helpers a `perfil_candidato.py`:

```python
def _identificador_conteudo(evento: dict) -> str:
    referencia = evento["content_ref"]
    return referencia.get("id") or referencia["content_id"]


def _nivel_evidencia(evento: dict) -> str:
    assistencia = evento["activity"].get("assistance_level", "nao_registrada")
    if evento["performance"]["result"] != "correto":
        return "em_desenvolvimento"
    if assistencia in {"nenhuma", "pista"}:
        return "demonstrado"
    return "em_desenvolvimento"
```

Alterar para `reconstruir_perfil(eventos: Iterable[dict], configuracao: dict | None = None) -> dict`. Ausência de configuração produz `declared` com listas vazias e sem preferência inventada. Preservar ordenação determinística, rejeição de duplicatas, remediações e gravação atômica.

- [ ] **Step 6: Registrar o novo schema no verificador de integração**

Adicionar `modelos/pedagogia/profile-settings.schema.json` à lista `ARQUIVOS_ESSENCIAIS` e atualizar o respectivo teste.

- [ ] **Step 7: Executar gates de schema e projeção**

Run:

```powershell
uv run python -m pytest tests/test_schemas_pedagogicos.py tests/test_eventos_aprendizagem.py tests/test_perfil_candidato.py tests/test_verificar_integracao.py -v --basetemp .test-tmp/profissionalizacao-task-6
```

Expected: PASS para eventos legados e v2; perfil derivado em v2 sem preferência pessoal criada por default.

- [ ] **Step 8: Commit dos contratos de perfil v2**

```powershell
git add plugins/magistratura-enam-br/modelos/pedagogia plugins/magistratura-enam-br/scripts/perfil_candidato.py plugins/magistratura-enam-br/scripts/verificar_integracao.py plugins/magistratura-enam-br/tests
git commit -m "feat(profile): add assistance-aware local profile v2"
```

### Task 7: Operações locais consentidas do perfil

**Files:**
- Modify: `plugins/magistratura-enam-br/scripts/eventos_aprendizagem.py`
- Modify: `plugins/magistratura-enam-br/scripts/perfil_candidato.py`
- Modify: `plugins/magistratura-enam-br/references/persistencia-pedagogica-local.md`
- Modify: `plugins/magistratura-enam-br/references/contrato-pedagogico.md`
- Modify: `plugins/magistratura-enam-br/tests/test_cli_persistencia_pedagogica.py`
- Modify: `plugins/magistratura-enam-br/tests/test_governanca_persistencia.py`

**Interfaces:**
- Consumes: profile settings e projeção v2 da Task 6.
- Produces: CLI com `inspect`, `rebuild`, `export` e `delete`; todas as escritas exigem `--confirmar-gravacao-local` e caminhos explícitos.

- [ ] **Step 1: Escrever testes de separação entre leitura e escrita**

Adicionar a `test_cli_persistencia_pedagogica.py`:

```python
def test_inspect_le_sem_autorizar_nova_escrita(tmp_path, capsys):
    perfil_path = tmp_path / "perfil.json"
    perfil.salvar_perfil_atomico(perfil_path, perfil.reconstruir_perfil([]))
    assert perfil.main(["inspect", "--perfil", str(perfil_path)]) == 0
    assert json.loads(capsys.readouterr().out)["schema_version"] == "2.0.0"


def test_rebuild_exige_confirmacao_de_gravacao_local(tmp_path):
    log = tmp_path / "eventos.jsonl"
    log.write_text("", encoding="utf-8")
    destino = tmp_path / "perfil.json"
    with pytest.raises(SystemExit):
        perfil.main(["rebuild", "--log", str(log), "--perfil", str(destino)])
    assert not destino.exists()


def test_delete_exige_confirmacao_e_remove_somente_o_alvo(tmp_path):
    perfil_path = tmp_path / "perfil.json"
    log = tmp_path / "eventos.jsonl"
    perfil_path.write_text("{}", encoding="utf-8")
    log.write_text("preservar", encoding="utf-8")
    assert perfil.main(["delete", "--perfil", str(perfil_path), "--confirmar-exclusao-local"]) == 0
    assert not perfil_path.exists()
    assert log.read_text(encoding="utf-8") == "preservar"
```

Adicionar teste equivalente para `eventos_aprendizagem.py append`: sem `--confirmar-gravacao-local`, nenhum log é criado.

- [ ] **Step 2: Confirmar que a CLI atual não separa consentimentos**

Run:

```powershell
uv run python -m pytest tests/test_cli_persistencia_pedagogica.py tests/test_governanca_persistencia.py -v --basetemp .test-tmp/profissionalizacao-task-7-red
```

Expected: FAIL por ausência dos comandos/flags.

- [ ] **Step 3: Implementar os comandos e flags explícitos**

Em ambos os CLIs, tornar `--confirmar-gravacao-local` obrigatório nos subcomandos que escrevem. Em `perfil_candidato.py`, implementar:

```python
if args.comando == "inspect":
    print(args.perfil.read_text(encoding="utf-8"), end="")
    return 0
if args.comando == "delete":
    args.perfil.unlink(missing_ok=True)
    print(json.dumps({"status": "removido", "perfil": str(args.perfil)}, ensure_ascii=False))
    return 0
```

`rebuild` aceitará `--config` opcional, validará settings e passará o objeto a `reconstruir_perfil`. `export` continuará exigindo caminhos explícitos e confirmação porque cria arquivo. Não criar diretório, perfil, log ou configuração automaticamente.

- [ ] **Step 4: Atualizar o contrato de persistência**

Documentar comandos completos, incluindo:

```powershell
uv run python scripts/perfil_candidato.py inspect --perfil C:\dados\perfil.json
uv run python scripts/perfil_candidato.py rebuild --log C:\dados\eventos.jsonl --perfil C:\dados\perfil.json --config C:\dados\preferencias.json --confirmar-gravacao-local
uv run python scripts/perfil_candidato.py export --log C:\dados\eventos.jsonl --perfil C:\dados\perfil.json --saida C:\dados\exportacao.json --confirmar-gravacao-local
uv run python scripts/perfil_candidato.py delete --perfil C:\dados\perfil.json --confirmar-exclusao-local
```

Explicar que leitura, uso na sessão, atualização e exclusão são autorizações distintas.

- [ ] **Step 5: Executar gates de governança e CLI**

Run:

```powershell
uv run python -m pytest tests/test_cli_persistencia_pedagogica.py tests/test_governanca_persistencia.py tests/test_eventos_aprendizagem.py tests/test_perfil_candidato.py -v --basetemp .test-tmp/profissionalizacao-task-7
```

Expected: PASS; operações não autorizadas não alteram o filesystem.

- [ ] **Step 6: Commit da experiência local de perfil**

```powershell
git add plugins/magistratura-enam-br/scripts plugins/magistratura-enam-br/references plugins/magistratura-enam-br/tests
git commit -m "feat(profile): require explicit local write consent"
```

### Task 8: Avaliações comportamentais e jurídicas da 0.6.0

**Files:**
- Modify: `plugins/magistratura-enam-br/evals/pedagogia/schema/evals.schema.json`
- Modify: `plugins/magistratura-enam-br/evals/pedagogia/evals.json`
- Modify: `plugins/magistratura-enam-br/evals/pedagogia/rubrica.md`
- Modify: `plugins/magistratura-enam-br/scripts/avaliar_saida_pedagogica.py`
- Modify: `plugins/magistratura-enam-br/tests/test_evals_pedagogicos.py`
- Modify: `plugins/magistratura-enam-br/tests/test_avaliar_saida_pedagogica.py`
- Create: `plugins/magistratura-enam-br/evals/pedagogia/profissionalizacao-0.6.0.md`

**Interfaces:**
- Consumes: contratos finais das Tasks 2–7.
- Produces: catálogo 0.6.0 com `front`, critérios semânticos explícitos e relatório humano reproduzível.

- [ ] **Step 1: Evoluir primeiro os testes do catálogo**

Alterar `test_evals_pedagogicos.py` para exigir `baseline == "0.5.0"`, `target == "0.6.0"` e pelo menos um caso para cada frente:

```python
FRENTES = {
    "orquestracao",
    "dogmatica",
    "caso_complexo",
    "objetiva",
    "discursiva",
    "oral",
    "revisao",
    "curadoria",
    "planejamento",
    "comparacao",
    "perfil_local",
}


def test_catalogo_cobre_todas_as_frentes_profissionalizadas():
    catalogo = carregar_json(CATALOGO)
    assert catalogo["baseline"] == "0.5.0"
    assert catalogo["target"] == "0.6.0"
    assert {caso["front"] for caso in catalogo["evals"]} >= FRENTES
```

- [ ] **Step 2: Ampliar o schema sem criar verificador semântico falso**

Adicionar `target` ao catálogo e `front` a cada caso. Manter checks automáticos apenas para estrutura literal. Adicionar `semantic_claims` como lista de objetos `{id, description, evidence_required}`, sempre dirigida à revisão humana.

- [ ] **Step 3: Confirmar a falha do catálogo antigo**

Run:

```powershell
uv run python -m pytest tests/test_evals_pedagogicos.py tests/test_avaliar_saida_pedagogica.py -v --basetemp .test-tmp/profissionalizacao-task-8-red
```

Expected: FAIL por ausência de `target`, `front` e novas frentes.

- [ ] **Step 4: Adicionar casos reservados por frente**

Adicionar ao catálogo, no mínimo:

```json
[
  {"id": "dogmatica-fontes-pulverizadas", "front": "dogmatica"},
  {"id": "dogmatica-pedido-pontual", "front": "dogmatica"},
  {"id": "dogmatica-continuidade-sem-reinicio", "front": "dogmatica"},
  {"id": "caso-solucoes-concorrentes", "front": "caso_complexo"},
  {"id": "objetiva-distratores-plausiveis", "front": "objetiva"},
  {"id": "discursiva-reconstrucao-do-erro", "front": "discursiva"},
  {"id": "oral-repergunta-adaptativa", "front": "oral"},
  {"id": "revisao-transferencia-independente", "front": "revisao"},
  {"id": "perfil-leitura-sem-escrita", "front": "perfil_local"},
  {"id": "perfil-ausente-sem-degradacao", "front": "perfil_local"}
]
```

Cada objeto completo deve usar fixture sintética, `expected_output`, ao menos uma asserção humana e riscos próprios. O caso dogmático deve exigir artigos cirúrgicos no desenvolvimento, precedentes com função identificável e fontes oficiais ao final; não exigir uma quantidade fixa de citações.

- [ ] **Step 5: Atualizar avaliador e rubrica**

`avaliar_saida_pedagogica.py` continuará marcando critérios semânticos como `revisao_humana_pendente`; não inferirá aprovação por presença de palavras. A rubrica humana terá quatro eixos de 0–2: precisão jurídica, função das fontes, progressão pedagógica e adequação à frente. Zero em precisão jurídica reprova o caso independentemente da soma.

- [ ] **Step 6: Executar gates do catálogo**

Run:

```powershell
uv run python -m pytest tests/test_evals_pedagogicos.py tests/test_avaliar_saida_pedagogica.py -v --basetemp .test-tmp/profissionalizacao-task-8
```

Expected: PASS estrutural; critérios semânticos permanecem explicitamente pendentes de revisão humana.

- [ ] **Step 7: Executar amostra comportamental e registrar evidência**

Executar em sessões limpas três rodadas dos casos centrais: `dogmatica-fontes-pulverizadas`, `dogmatica-continuidade-sem-reinicio`, `caso-solucoes-concorrentes`, `discursiva-reconstrucao-do-erro`, `oral-repergunta-adaptativa` e `perfil-leitura-sem-escrita`. Aplicar a rubrica somente depois das respostas. Registrar em `profissionalizacao-0.6.0.md` modelo, data, casos, decisões por eixo, divergências e bloqueios; não versionar respostas que contenham dados pessoais.

- [ ] **Step 8: Commit dos evals**

```powershell
git add plugins/magistratura-enam-br/evals plugins/magistratura-enam-br/scripts/avaliar_saida_pedagogica.py plugins/magistratura-enam-br/tests
git commit -m "test(evals): cover professionalized legal study fronts"
```

### Task 9: Documentação, versão e gate integrado

**Files:**
- Modify: `plugins/magistratura-enam-br/README.md`
- Modify: `plugins/magistratura-enam-br/CHANGELOG.md`
- Modify: `plugins/magistratura-enam-br/CONTINUACAO.md`
- Modify: `plugins/magistratura-enam-br/.codex-plugin/plugin.json`
- Modify: `plugins/magistratura-enam-br/pyproject.toml`
- Modify: `plugins/magistratura-enam-br/uv.lock`
- Modify: `docs/site/index.md`
- Modify: `docs/site/arquitetura-pedagogica.md`
- Modify: `docs/site/privacidade-e-persistencia.md`
- Modify: `docs/site/skills/index.md`

**Interfaces:**
- Consumes: implementação e evidências das Tasks 1–8.
- Produces: release candidate 0.6.0 instalável, documentada e sem alteração de infraestrutura.

- [ ] **Step 1: Atualizar documentação pública**

Descrever as cinco skills públicas e, dentro do estudo, as frentes dogmática, casos, objetiva, discursiva, oral e revisão. Explicar em texto corrido que legislação e jurisprudência são integradas no ponto conceitual relevante e que as fontes oficiais aparecem ao final. Documentar uso completo sem perfil e operações locais consentidas com caminhos explícitos.

- [ ] **Step 2: Atualizar versão e changelog**

Alterar `plugin.json` e `pyproject.toml` para `0.6.0`. Inserir no topo do changelog:

```markdown
## 0.6.0 — 2026-09-05

- Despersonifica defaults e mantém especialização para bacharéis, Magistratura e ENAM.
- Integra dogmática, legislação e jurisprudência em sessões cumulativas.
- Especializa casos, objetiva, discursiva, oral, revisão, curadoria, planejamento e comparação.
- Evolui o perfil local para distinguir assistência, transferência, retenção e preferências declaradas.
- Separa leitura, gravação e exclusão do perfil por autorizações explícitas.
```

Run:

```powershell
Set-Location plugins/magistratura-enam-br
uv lock
```

- [ ] **Step 3: Executar a suíte integral**

Run:

```powershell
uv run python -m pytest tests skills/planejar-jurisprudencia/tests skills/comparar-materiais-enam/tests skills/curar-informativos-stf-stj/tests --basetemp .test-tmp/profissionalizacao-final
uv run ruff check .
uv lock --check
uv run python scripts/verificar_integracao.py
```

Expected: zero falhas, zero erros de Ruff, lock sincronizado e integração aprovada.

- [ ] **Step 4: Validar documentação e pacote**

Run from repository root:

```powershell
uv run --project plugins/magistratura-enam-br mkdocs build --strict
git diff --check
rg -n "TBD|TODO|50% ciclo geral|25% recuperação|na última vez em que fizemos essa escolha|seu estágio atual" plugins/magistratura-enam-br docs/site
```

Expected: build aprovado, diff sem whitespace inválido e busca sem placeholders ou defaults pessoais. Ocorrências explicativas em testes de regressão são admissíveis e devem estar restritas aos valores proibidos do próprio teste.

- [ ] **Step 5: Inspecionar o diff por classe de operação**

Comparar o diff com o inventário e registrar em `CONTINUACAO.md` as contagens de regras preservadas, aprofundadas, realocadas, generalizadas e removidas. Toda remoção deve apontar seu destino canônico e teste; qualquer remoção sem cobertura bloqueia o commit final.

- [ ] **Step 6: Commit da candidata 0.6.0**

```powershell
git add plugins/magistratura-enam-br docs/site
git commit -m "feat(plugin): release professionalized study architecture 0.6.0"
```

- [ ] **Step 7: Verificação final do estado local**

Run:

```powershell
git status --short
git log --oneline --decorate -9
```

Expected: árvore limpa e nove commits locais correspondentes às Tasks 1–9. Push, PR, merge e publicação somente nos gates expressamente autorizados depois desta verificação.
