# Plano de implementação — organização e qualidade do plugin

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tornar previsíveis o roteamento entre plugin e treinador FGV, a qualidade jurídico-pedagógica avaliada e o estado do acervo MCP, sem duplicar sistemas nem introduzir infraestrutura sem necessidade.

**Architecture:** Preservar as cinco skills, o índice Markdown local e o fluxo MCP atual como núcleo canônico. Evoluir primeiro evidências e contratos: registrar a fronteira entre clientes, ampliar os evals existentes com um benchmark jurídico humano-validado e oferecer diagnóstico local somente de leitura. A integração de bases multimodais ou migração do formato do plugin fica condicionada a uma lacuna demonstrada.

**Tech Stack:** Markdown, JSON Schema Draft 2020-12, Python 3.14, `uv`, `pytest`, `jsonschema`, MCP e documentação MkDocs/Zensical já existentes.

**Spec:** Proposta de organização e qualidade apresentada na conversa de 2026-09-22; decisões e limites consolidados neste plano.

**Estado em 2026-09-24:** Tasks 1, 3, 4 e 5 executadas tecnicamente na branch `codex/organizacao-qualidade-plugin`. A Task 2 tem schema, fontes e oito casos implementados; revisão jurídica independente e três execuções limpas por caso permanecem pendentes como validação formal, não como condição do piloto em uso real solicitado pelo usuário. O smoke Codex com fixture passou; o ChatGPT remoto não foi homologado porque o túnel não estava operacional. Gate integrado anterior à candidata de instalação: 323 testes aprovados, Ruff, lock, verificador de integração, build MkDocs estrito e `git diff --check` aprovados. A versão de branch é `0.7.3`; a tag estável permanece `v0.7.2`.

## Global Constraints

- `plugins/magistratura-enam-br` permanece a única fonte canônica do plugin.
- Não alterar nem copiar automaticamente a skill global `$treinador-fgv-magistratura`; ela é um pacote externo ao repositório.
- Não presumir que habilidades do Codex estejam carregadas no ChatGPT ou em outro cliente MCP.
- O estado do acervo, a busca e a indexação permanecem distintos; diagnóstico não indexa nem grava.
- Nenhuma resposta jurídica é aprovada por teste lexical ou por modelo-juiz sem revisão humana.
- Fontes jurídicas do benchmark devem ser oficiais, localizáveis e associadas a uma data de verificação; não armazenar provas protegidas, respostas reais ou dados pessoais.
- Não adicionar dependência, telemetria, nuvem, Open Notebook ou serviço externo nesta execução.
- Usar Python `>=3.14,<3.15` com `uv`; não introduzir `pip`.
- Commit, push, PR, merge, tag, publicação e instalação são gates distintos; este plano não os autoriza.

## Review Focus

- O cliente não oferece o treinador FGV externo: a orientação não pode afirmar que ele foi acionado; cobrir em `evals/pedagogia/evals.json` com caso positivo e near-miss de roteamento.
- Índice ausente ou corrompido: o diagnóstico deve informar estado limitado sem criar, reparar ou sobrescrever arquivos; cobrir em `tests/test_mcp_tools.py`.
- Fonte jurídica sem apoio para a afirmação ou com atualização não confirmada: resultado deve permanecer pendente/reprovado para análise humana; cobrir em `tests/test_evals_pedagogicos.py` e no benchmark.
- Questão com distrator defensável ou gabarito ambíguo: precisão jurídica impede aprovação mesmo que formato e rubrica somem pontos; cobrir por caso jurídico revisado e rubrica.
- Dúvida pontual submetida a regras extensas: avaliar extensão por modalidade e finalidade, sem impor limite global de palavras; cobrir por pares de casos breve/profundo.

---

### Task 1: Fixar o mapa de ambientes e o contrato de roteamento

**Files:**
- Create: `docs/superpowers/audits/2026-09-22-matriz-ambientes-e-roteamento.md`
- Modify: `plugins/magistratura-enam-br/evals/pedagogia/evals.json`
- Modify: `plugins/magistratura-enam-br/evals/pedagogia/fase-6/routing/README.md`
- Modify: `plugins/magistratura-enam-br/skills/acompanhar-percurso-magistratura/references/roteamento.md`
- Test: `plugins/magistratura-enam-br/tests/test_evals_pedagogicos.py`

**Interfaces:**
- Consumes: cinco skills do plugin, ferramenta MCP local e habilidade global instalada fora do repositório.
- Produces: matriz que distingue habilidade, ferramenta, armazenamento, disponibilidade e superfície; convenção de acionamento explícito do treinador externo.

- [ ] **Step 1: Registrar o baseline técnico**

Run from repository root:

```powershell
git status --short --branch
git log -10 --oneline
Set-Location plugins/magistratura-enam-br
uv sync --all-groups
uv run python -m pytest tests/test_evals_pedagogicos.py tests/test_mcp_tools.py -v --basetemp .pytest-organizacao-baseline
```

Expected: estado Git registrado; os testes focados passam. Se o checkout ou os testes divergirem, atualizar o plano de trabalho antes de qualquer edição de comportamento.

- [ ] **Step 2: Construir a matriz factual dos clientes**

Registrar no artefato os campos `superficie`, `como carrega skills`, `como conecta MCP`, `onde persiste`, `estado observado` e `limite`. Distinguir pelo menos: Codex com plugin instalado, Codex com skill global explícita e ChatGPT com MCP via túnel. Marcar Claude/Cursor/outros como não testados neste checkout, sem inferir compatibilidade universal. Registrar separadamente que o índice é configurado fora da pasta do plugin e que o servidor aponta seu estado local para `.estudo-juridico` dentro da raiz da biblioteca.

- [ ] **Step 3: Definir a regra de precedência sem alterar a skill global**

Documentar que o treinador externo só é invocado por seu identificador explícito quando estiver disponível no cliente. Um pedido genérico de questão continua na skill do plugin; em cliente sem a skill externa, não alegar calibração exclusiva de 480 questões. Não sincronizar histórico nem duplicar gravações entre os dois ambientes.

- [ ] **Step 4: Adicionar cenários de roteamento e testar o catálogo**

Adicionar ao catálogo um caso de acionamento explícito do treinador externo, um pedido genérico de questão difícil e um cliente sem aquela skill. Cada caso terá `expected_route`, `expected_transition`, uma asserção humana e `risk_tags` específicos; o teste automatizado verificará schema, IDs únicos e presença dos três cenários, não a qualidade da resposta.

Run:

```powershell
Set-Location plugins/magistratura-enam-br
uv run python -m pytest tests/test_evals_pedagogicos.py -v --basetemp .pytest-organizacao-routing
```

Expected: PASS estrutural. Cenários sem execução em cliente real ficam identificados como não homologados.

### Task 2: Criar o benchmark jurídico-pedagógico piloto

**Files:**
- Modify: `plugins/magistratura-enam-br/evals/pedagogia/schema/evals.schema.json`
- Modify: `plugins/magistratura-enam-br/evals/pedagogia/evals.json`
- Modify: `plugins/magistratura-enam-br/evals/pedagogia/rubrica.md`
- Modify: `plugins/magistratura-enam-br/evals/pedagogia/README.md`
- Create: `plugins/magistratura-enam-br/evals/pedagogia/benchmark-juridico/README.md`
- Create: `plugins/magistratura-enam-br/evals/pedagogia/benchmark-juridico/fontes.json`
- Modify: `plugins/magistratura-enam-br/tests/test_evals_pedagogicos.py`
- Modify: `plugins/magistratura-enam-br/scripts/avaliar_saida_pedagogica.py` somente se necessário para validar a nova estrutura; manter revisão semântica humana.

**Interfaces:**
- Consumes: schema atual 1.1.0, 44 casos pedagógicos, rubrica humana e avaliador estrutural.
- Produces: piloto de ao menos oito casos sintéticos em uma matéria já representada no catálogo, cobrindo questão objetiva, correção, transferência, caso complexo, dúvida pontual e resposta que exige desenvolvimento; cada conclusão jurídica material terá fonte oficial e critério humano de aceitação.

- [ ] **Step 1: Escolher um recorte sem ampliar artificialmente o escopo**

Selecionar, após inventariar os casos já existentes, um tema com regra, exceção ou precedente verificável em fonte oficial e que permita ao menos uma hipótese nova de transferência. Registrar no `README.md` do benchmark por que o recorte é testável e quais modalidades ele cobre. Não usar prova protegida ou transcrição substancial de questão comercial.

- [ ] **Step 2: Especificar metadados de sustentação jurídica**

Acrescentar ao caso, como campo opcional retrocompatível `legal_grounding`, o objeto com `checked_at` (data ISO), `cutoff_date` (data ISO), `claims` e `human_review`. Cada claim contém `id`, `expected_conclusion`, `official_source`, `locator` e `supports`; não armazenar texto integral da fonte. `human_review` contém `review_status` (`pending`, `approved` ou `rejected`) e `review_note`. `approved` exige nota não vazia, fonte oficial e ao menos um claim.

- [ ] **Step 3: Escrever primeiro os testes do schema e das travas**

Em `test_evals_pedagogicos.py`, validar: catálogo antigo continua válido; caso novo com fonte, localizador e datas válidos é aceito; data inválida, claim sem fonte oficial, aprovação sem nota e gabarito aprovado sem claim são rejeitados. Confirmar que resultado automático continua `revisao_humana_pendente` enquanto houver claim sem decisão humana.

Run:

```powershell
Set-Location plugins/magistratura-enam-br
uv run python -m pytest tests/test_evals_pedagogicos.py tests/test_avaliar_saida_pedagogica.py -v --basetemp .pytest-benchmark-schema-red
```

Expected: os novos testes falham antes da implementação por campo/schema ausente; os casos antigos permanecem compatíveis.

- [ ] **Step 4: Implementar o schema aditivo e validação estrita**

Adicionar a definição de `legal_grounding` ao schema sem mudar a versão do schema para os campos antigos nem afrouxar `additionalProperties: false`. Se o schema exigir incremento de versão após a análise de compatibilidade, manter validação explícita dos catálogos 1.1.0 existentes e documentar a migração. O avaliador nunca converte presença de URL, palavra ou resultado de modelo em validação jurídica.

- [ ] **Step 5: Criar os oito casos sintéticos e a referência de fontes**

Os casos devem incluir: pergunta pontual com resposta proporcional; explicação dogmática; caso complexo com soluções concorrentes; questão objetiva com cinco alternativas plausíveis e chave única; correção das alternativas; discursiva com critério de suficiência e excelência; oral em pergunta unitária; e hipótese de transferência com alteração material dos fatos. Em cada caso, indicar a fonte oficial, localização normativa/jurisprudencial, data de conferência, conclusão esperada, limites e erro impeditivo. Não prometer atualização contínua: fonte com estado posterior incerto requer revisão humana.

- [ ] **Step 6: Aplicar rubrica humana e preservar variação**

Pontuar de 0 a 2 precisão jurídica, suporte das fontes, operação cognitiva, feedback/transferência, adequação da modalidade e proporcionalidade. Nota zero em precisão jurídica, ambiguidade material do gabarito ou fonte que não sustente a conclusão reprova o caso. Executar três sessões limpas por caso; preservar divergência entre avaliadores e variação entre rodadas, sem reduzir respostas a média ou ao número de palavras.

- [ ] **Step 7: Rodar gates focados do benchmark**

Run:

```powershell
Set-Location plugins/magistratura-enam-br
uv run python -m pytest tests/test_evals_pedagogicos.py tests/test_avaliar_saida_pedagogica.py -v --basetemp .pytest-benchmark-schema
uv run python scripts/avaliar_saida_pedagogica.py --help
```

Expected: schema e estrutura passam; aprovação semântica continua marcada apenas após revisão humana documentada.

### Task 3: Expor diagnóstico somente de leitura do acervo MCP

**Files:**
- Modify: `plugins/magistratura-enam-br/mcp_server/tools.py`
- Modify: `plugins/magistratura-enam-br/mcp_server/server.py`
- Modify: `plugins/magistratura-enam-br/tests/test_mcp_tools.py`
- Modify: `plugins/magistratura-enam-br/tests/test_mcp_transport.py`
- Modify: `plugins/magistratura-enam-br/README.md`
- Modify: `docs/site/privacidade-e-persistencia.md`

**Interfaces:**
- Consumes: `StudyService.config`, `index_path` e manifesto `index.json` existente.
- Produces: ferramenta MCP `diagnosticar_acervo()` sem parâmetros, estruturada e anotada como somente leitura; informa raiz configurada, caminho de estado, existência do índice, data de geração e número de documentos indexados, sem conteúdo dos documentos.

- [ ] **Step 1: Escrever testes de leitura e ausência de efeitos colaterais**

Adicionar em `test_mcp_tools.py` testes de índice ausente, índice válido e JSON inválido. Verificar que a ferramenta retorna estado explícito (`missing`, `available` ou `invalid`), contagem/data apenas quando válidas e não cria `index.json`, diretório, reparo ou escrita em nenhum caso.

- [ ] **Step 2: Verificar a falha antes de implementar**

Run:

```powershell
Set-Location plugins/magistratura-enam-br
uv run python -m pytest tests/test_mcp_tools.py -k diagnostico -v --basetemp .pytest-diagnostico-red
```

Expected: FAIL por ausência do método/tool.

- [ ] **Step 3: Implementar método e ferramenta MCP**

Adicionar a `StudyService` um método que apenas lê a configuração já carregada e, se existente, o JSON do índice. Capturar apenas erro de leitura/JSON inválido para retornar estado diagnóstico; não normalizar nem regravar dados. Expor `diagnosticar_acervo` com `readOnlyHint=True`, sem parâmetro de confirmação e sem divulgar trechos ou nomes de documentos.

- [ ] **Step 4: Validar descoberta MCP e proteção contra gravação**

Atualizar teste de descoberta para exigir `diagnosticar_acervo`; verificar anotação `readOnlyHint`, invocação sem argumentos e comparação de conteúdo do diretório antes/depois.

Run:

```powershell
Set-Location plugins/magistratura-enam-br
uv run python -m pytest tests/test_mcp_tools.py tests/test_mcp_transport.py -v --basetemp .pytest-diagnostico
```

Expected: PASS; diagnóstico não cria nem modifica o acervo ou seu índice.

- [ ] **Step 5: Documentar o que o diagnóstico prova e não prova**

Explicar que conexão MCP não prova existência/atualidade do índice, que diagnóstico não indexa, e que busca requer índice existente. Não afirmar que o índice está atualizado com os arquivos atuais sem implementar e testar uma comparação explícita de hashes.

### Task 4: Homologar limites entre superfícies e atualizar documentação

**Files:**
- Modify: `plugins/magistratura-enam-br/README.md`
- Modify: `plugins/magistratura-enam-br/docs/chatgpt-local.md`
- Modify: `docs/site/primeiros-passos.md`
- Modify: `docs/site/instalacao.md`
- Modify: `docs/site/skills/index.md`
- Modify: `docs/site/privacidade-e-persistencia.md`
- Modify: `plugins/magistratura-enam-br/tests/test_app_mapping.py` somente se metadados ou mapeamento mudarem.

**Interfaces:**
- Consumes: matriz da Task 1 e operação `diagnosticar_acervo` da Task 3.
- Produces: instruções versionadas por superfície e protocolo de smoke sem alegar cliente que não foi testado.

- [ ] **Step 1: Verificar o fluxo Codex local**

Usar o servidor `stdio` já declarado em `.mcp.json`, confirmar descoberta de ferramentas MCP, executar diagnóstico, buscar somente depois de confirmar índice e testar uma questão completa até a tentativa/correção em fixture. Registrar ferramenta e resultado, sem escrever no acervo pessoal.

- [ ] **Step 2: Verificar o fluxo ChatGPT com túnel**

Somente se o túnel e a conexão MCP estiverem disponíveis: confirmar que o ChatGPT descobre as ferramentas, obter estado diagnóstico e exercitar a UI da questão. Se indisponível, registrar como pendência ambiental, sem mudar política de binding, tarefa agendada ou acesso de rede neste escopo.

- [ ] **Step 3: Atualizar matriz de suporte**

Indicar capacidades compartilhadas e específicas (skills, ferramentas MCP, UI, persistência e requisito do túnel). Marcar cada célula como validada, declarada pelo pacote ou não testada. Não migrar automaticamente `.codex-plugin/plugin.json` para outro formato de distribuição e não declarar suporte a cliente terceiro sem smoke correspondente.

- [ ] **Step 4: Executar validação documental**

Run from repository root:

```powershell
uv run --project plugins/magistratura-enam-br mkdocs build --strict
git diff --check
```

Expected: build estrito e diff aprovados; todos os caminhos de instrução apontam para arquivos existentes.

### Task 5: Gate integrado e decisão sobre extensão multimodal

**Files:**
- Modify: `plugins/magistratura-enam-br/CHANGELOG.md` se houver alteração comportamental publicável.
- Modify: `plugins/magistratura-enam-br/CONTINUACAO.md` com estado e limitações validados.
- Modify: versão em `.codex-plugin/plugin.json`, `pyproject.toml` e `uv.lock` somente se a natureza/dimensão da mudança exigir nova versão.
- Test: suíte e verificador de integração já existentes.

**Interfaces:**
- Consumes: entregáveis das Tasks 1–4.
- Produces: evidência integrada, estado da release e decisão documentada de manter o acervo Markdown ou abrir avaliação separada de PDFs/OCR.

- [ ] **Step 1: Executar os gates completos do plugin**

Run from repository root:

```powershell
Set-Location plugins/magistratura-enam-br
uv run python -m pytest tests skills/planejar-jurisprudencia/tests skills/comparar-materiais-enam/tests skills/curar-informativos-stf-stj/tests --basetemp .pytest-organizacao-final
uv run ruff check .
uv lock --check
uv run python scripts/verificar_integracao.py
Set-Location ../..
uv run --project plugins/magistratura-enam-br mkdocs build --strict
git diff --check
```

Expected: zero falhas; teste de verificação mantém a regra de não criar bytecode, cache ou artefato na árvore fonte.

- [ ] **Step 2: Registrar resultados sem extrapolar**

Em `CONTINUACAO.md`, registrar checkout/commit validado, comandos realmente executados, resultados, versão efetiva, superfícies testadas e não testadas, benchmark aprovado ou pendente de revisão jurídica e eventual bloqueio do túnel. Não declarar homologação ChatGPT quando apenas o fluxo `stdio` tiver sido testado.

- [ ] **Step 3: Decidir se Open Notebook merece projeto separado**

Manter fora do escopo salvo demonstração de que PDFs digitalizados ou formatos multimodais recorrentes não podem ser atendidos pelo fluxo atual. Para abrir avaliação posterior, exigir amostra pequena de documentos não sensíveis, citações localizáveis por página, privacidade e permissões verificadas e comparação de qualidade com o índice Markdown. Não instalar, importar acervo real ou adicionar novo backend nesta fase.

- [ ] **Step 4: Revisar diff e determinar a próxima fronteira de release**

Verificar que nenhuma escrita externa, alteração de skill global, instalação, publicação, push, PR, merge ou tag ocorreu. Separar os dois componentes independentes — benchmark e diagnóstico MCP — em commits próprios quando implementados; decidir a versão depois do diff final, não antes.

## Critério de conclusão desta execução

Para a candidata em uso real, o plano estará implementado quando (1) clientes e roteamento estiverem descritos sem promessas cruzadas; (2) o benchmark piloto tiver fontes oficiais rastreáveis, estado de revisão pendente explícito e critérios de proporcionalidade/transferência, sem alegação de qualidade jurídica aprovada; (3) o diagnóstico MCP for somente de leitura e estiver testado; e (4) os gates integrados e limites de homologação estiverem documentados. A revisão humana formal e as três execuções por caso permanecem uma avaliação separada, não condição para instalar a candidata. Open Notebook, migração de formato universal, tag, PR e merge não são pré-requisitos.
