# MCP de Questões Interativas — Plano de Implementação

> **Para execução agentic:** implementar uma tarefa por vez, usando TDD, verificando o diff e criando apenas o commit previsto para a tarefa. Push, PR, merge, publicação e release não estão autorizados por este plano.

**Objetivo:** Acrescentar ao plugin 0.6.0 um MCP local com indexação Markdown, geração dinâmica de questões pelo modelo, widget moderno, gabarito protegido e histórico local, funcionando no Codex e no ChatGPT.

**Arquitetura:** Manter a skill como autoridade pedagógica e introduzir um núcleo Python determinístico para caminhos, busca, sessões e persistência. Separar ferramentas de dados da ferramenta de renderização. Distribuir o servidor local ao Codex por `.mcp.json` e conectá-lo ao ChatGPT por Secure MCP Tunnel e registro em modo desenvolvedor.

**Stack:** Python 3.14, `uv`, SDK MCP/FastMCP compatível, Pydantic ou JSON Schema conforme dependências confirmadas, `pytest`, React, TypeScript, Vite, Vitest, Testing Library e axe.

**Especificação:** `docs/superpowers/specs/2026-09-05-mcp-questoes-interativas-design.md`

## Restrições globais

- Trabalhar no plugin canônico `plugins/magistratura-enam-br`.
- Não alterar nem criar conteúdo dentro da biblioteca real durante testes; usar diretórios temporários.
- Não introduzir `pip`; dependências Python entram por `uv`.
- Não persistir tokens, credenciais ou identidade privada do túnel.
- Não expor `correct_option`, fundamentos ou análise de distratores antes da tentativa.
- Não usar `localStorage` nem `widgetState` como fonte durável.
- Não substituir os eventos/perfis existentes sem migração ou integração explícita.
- Não afirmar compatibilidade com ChatGPT ou Codex sem teste real em cada superfície.
- Tratar instalação do serviço, registro do MCP, início automático, build, commit, push, PR, merge e release como gates separados.

## Tarefa 1: Linha de base, dependências e contratos públicos

**Arquivos:**

- Modificar: `plugins/magistratura-enam-br/pyproject.toml`
- Modificar: `plugins/magistratura-enam-br/uv.lock`
- Criar: `plugins/magistratura-enam-br/mcp_server/__init__.py`
- Criar: `plugins/magistratura-enam-br/mcp_server/schemas/library-config.schema.json`
- Criar: `plugins/magistratura-enam-br/mcp_server/schemas/indexed-document.schema.json`
- Criar: `plugins/magistratura-enam-br/mcp_server/schemas/question-session.schema.json`
- Criar: `plugins/magistratura-enam-br/mcp_server/schemas/question-attempt.schema.json`
- Criar: `plugins/magistratura-enam-br/tests/test_mcp_schemas.py`

- [ ] Registrar o estado inicial com `git status --short --branch`, `git rev-parse HEAD` e a suíte vigente.
- [ ] Escrever testes que carreguem os quatro schemas e validem exemplos mínimos.
- [ ] Exigir exatamente cinco alternativas `A`–`E`, chave única, correção completa, referências versionadas e `source_status` entre `verified`, `partial` e `caution`.
- [ ] Separar no schema as projeções privada, pública e corrigida; a pública não deve admitir a chave.
- [ ] Confirmar os testes vermelhos antes de criar os schemas.
- [ ] Adicionar somente as dependências MCP necessárias com `uv add`; atualizar o lock.
- [ ] Executar:

```powershell
Set-Location plugins/magistratura-enam-br
uv run python -m pytest tests/test_mcp_schemas.py -v --basetemp .test-tmp/mcp-task-1
uv lock --check
```

- [ ] Commit: `feat(mcp): define interactive question contracts`.

## Tarefa 2: Raiz autorizada e contenção segura

**Arquivos:**

- Criar: `plugins/magistratura-enam-br/mcp_server/config.py`
- Criar: `plugins/magistratura-enam-br/mcp_server/paths.py`
- Criar: `plugins/magistratura-enam-br/tests/test_mcp_paths.py`
- Criar: `plugins/magistratura-enam-br/tests/test_mcp_config.py`

- [ ] Testar configuração ausente, raiz inexistente, caminho relativo, arquivo no lugar de diretório e consentimento não confirmado.
- [ ] Testar contenção de arquivo regular dentro da raiz e rejeição de `..`, caminho absoluto externo, UNC externo, symlink/junction e ponto de nova análise que escape da raiz.
- [ ] Testar que escritas só podem atingir `<raiz>/.estudo-juridico/`.
- [ ] Implementar `LibraryConfig` versionada, com raiz absoluta, exclusões e limites, sem criar diretórios implicitamente durante leitura.
- [ ] Implementar helpers de resolução canônica e contenção com semântica correta no Windows.
- [ ] Executar:

```powershell
uv run python -m pytest tests/test_mcp_paths.py tests/test_mcp_config.py -v --basetemp .test-tmp/mcp-task-2
```

- [ ] Commit: `feat(mcp): authorize one local markdown library`.

## Tarefa 3: Indexador Markdown recursivo

**Arquivos:**

- Criar: `plugins/magistratura-enam-br/mcp_server/indexer.py`
- Criar: `plugins/magistratura-enam-br/mcp_server/retrieval.py`
- Criar: `plugins/magistratura-enam-br/tests/test_mcp_indexer.py`
- Criar: `plugins/magistratura-enam-br/tests/test_mcp_retrieval.py`

- [ ] Criar fixtures temporárias com Markdown na raiz e em subpastas, headings, Unicode, arquivo grande, ocultos e exclusões.
- [ ] Testar que `.git`, `.estudo-juridico`, `node_modules`, ocultos e caminhos inseguros são ignorados.
- [ ] Testar manifesto incremental por hash e remoção de entrada quando o original desaparece.
- [ ] Implementar segmentação por headings e parágrafos, preservando caminho relativo e posição.
- [ ] Implementar busca lexical determinística, filtros e limites de retorno.
- [ ] Garantir que indexação e busca nunca alteram os Markdown.
- [ ] Executar:

```powershell
uv run python -m pytest tests/test_mcp_indexer.py tests/test_mcp_retrieval.py tests/test_contrato_acervo_markdown.py -v --basetemp .test-tmp/mcp-task-3
```

- [ ] Commit: `feat(mcp): index local markdown recursively`.

## Tarefa 4: Persistência append-only e máquina de estados

**Arquivos:**

- Criar: `plugins/magistratura-enam-br/mcp_server/persistence.py`
- Criar: `plugins/magistratura-enam-br/mcp_server/questions.py`
- Criar: `plugins/magistratura-enam-br/tests/test_mcp_persistence.py`
- Criar: `plugins/magistratura-enam-br/tests/test_mcp_question_sessions.py`
- Modificar, se necessário: `plugins/magistratura-enam-br/scripts/eventos_aprendizagem.py`
- Modificar, se necessário: `plugins/magistratura-enam-br/scripts/perfil_candidato.py`

- [ ] Testar append UTF-8, flush, lock, IDs estáveis, timestamps UTC e rejeição de JSONL previamente corrompido.
- [ ] Testar `draft -> ready -> answered`, invalidação explícita e proibição de transições regressivas.
- [ ] Testar que a criação retorna somente a projeção pública.
- [ ] Testar primeira resposta, repetição idempotente e conflito quando uma segunda alternativa diverge.
- [ ] Testar reconstrução do perfil e do histórico após reinício do processo.
- [ ] Integrar tentativas ao contrato pedagógico existente sem criar perfil paralelo.
- [ ] Executar:

```powershell
uv run python -m pytest tests/test_mcp_persistence.py tests/test_mcp_question_sessions.py tests/test_eventos_aprendizagem.py tests/test_perfil_candidato.py -v --basetemp .test-tmp/mcp-task-4
```

- [ ] Commit: `feat(mcp): persist question sessions and attempts`.

## Tarefa 5: Servidor MCP e ferramentas de dados

**Arquivos:**

- Criar: `plugins/magistratura-enam-br/mcp_server/server.py`
- Criar: `plugins/magistratura-enam-br/mcp_server/tools.py`
- Criar: `plugins/magistratura-enam-br/tests/test_mcp_tools.py`
- Criar: `plugins/magistratura-enam-br/tests/test_mcp_transport.py`

- [ ] Testar contratos de `indexar_acervo`, `buscar_acervo`, `criar_sessao_questao`, `responder_questao` e `consultar_historico_questoes` por cliente MCP real.
- [ ] Confirmar que ferramentas de dados não carregam `_meta.ui.resourceUri`.
- [ ] Confirmar por busca recursiva serializada que a criação não devolve chave, correção nem distratores.
- [ ] Implementar composição explícita das dependências para permitir biblioteca temporária nos testes.
- [ ] Oferecer `stdio` para Codex e transporte HTTP compatível para o túnel sem duplicar regras de domínio.
- [ ] Aplicar limites de entrada e mensagens de erro sem divulgar caminhos além do necessário.
- [ ] Executar:

```powershell
uv run python -m pytest tests/test_mcp_tools.py tests/test_mcp_transport.py -v --basetemp .test-tmp/mcp-task-5
```

- [ ] Commit: `feat(mcp): expose legal study tools`.

## Tarefa 6: Recurso MCP Apps e widget moderno

**Arquivos:**

- Criar: `plugins/magistratura-enam-br/mcp_server/resources.py`
- Criar: `plugins/magistratura-enam-br/web/package.json`
- Criar: `plugins/magistratura-enam-br/web/package-lock.json`
- Criar: `plugins/magistratura-enam-br/web/tsconfig.json`
- Criar: `plugins/magistratura-enam-br/web/vite.config.ts`
- Criar: `plugins/magistratura-enam-br/web/src/contracts.ts`
- Criar: `plugins/magistratura-enam-br/web/src/main.tsx`
- Criar: `plugins/magistratura-enam-br/web/src/QuestionWidget.tsx`
- Criar: `plugins/magistratura-enam-br/web/src/styles.css`
- Criar: `plugins/magistratura-enam-br/web/src/QuestionWidget.test.tsx`
- Criar: `plugins/magistratura-enam-br/tests/test_mcp_ui_resource.py`

- [ ] Criar primeiro testes dos estados visualmente observáveis: pronta, selecionada, enviando, correta, incorreta, cautela e erro.
- [ ] Testar teclado, radio group, foco, `aria-live`, contraste e ausência do gabarito no DOM antes da resposta.
- [ ] Implementar identidade visual derivada do plugin, layout responsivo e preferência de movimento reduzido.
- [ ] Fazer o widget chamar `responder_questao` pelo bridge MCP Apps e renderizar exclusivamente a resposta liberada.
- [ ] Registrar `ui://estudo-juridico/questao/v1.html` com MIME exigido pela especificação vigente.
- [ ] Implementar `renderizar_questao` como única ferramenta inicial contendo `_meta.ui.resourceUri`.
- [ ] Executar:

```powershell
Set-Location web
npm ci
npm test -- --run
npm run build
Set-Location ..
uv run python -m pytest tests/test_mcp_ui_resource.py tests/test_mcp_tools.py -v --basetemp .test-tmp/mcp-task-6
```

- [ ] Fazer inspeção visual do widget em largura estreita e larga; teste estrutural não substitui esse gate.
- [ ] Commit: `feat(ui): add interactive legal question widget`.

## Tarefa 7: Integração pedagógica e fallback textual

**Arquivos:**

- Modificar: `plugins/magistratura-enam-br/skills/estudar-direito-magistratura/SKILL.md`
- Modificar: `plugins/magistratura-enam-br/references/contrato-pedagogico.md`
- Modificar: `plugins/magistratura-enam-br/references/politica-fontes-juridicas.md`
- Criar: `plugins/magistratura-enam-br/references/questoes-interativas-mcp.md`
- Modificar: `plugins/magistratura-enam-br/tests/test_contrato_questoes_fgv.py`
- Criar: `plugins/magistratura-enam-br/tests/test_integracao_questoes_mcp.py`

- [ ] Testar o fluxo: busca local opcional, fontes atuais, geração privada, criação, renderização, tentativa e correção.
- [ ] Testar que a skill continua exigindo cinco alternativas, gabarito único e análise integral dos distratores.
- [ ] Testar fonte canônica em ordem Planalto, STF/STJ, acervo e fonte jurídica subsidiária.
- [ ] Testar `source_status: caution` e aviso obrigatório quando não houver verificação atual.
- [ ] Testar fallback textual sem antecipação do gabarito quando MCP Apps não estiver disponível.
- [ ] Remover duplicações apenas depois de apontar a nova fonte canônica.
- [ ] Executar:

```powershell
uv run python -m pytest tests/test_contrato_questoes_fgv.py tests/test_integracao_questoes_mcp.py tests/test_politica_fontes.py tests/test_governanca_fontes.py -v --basetemp .test-tmp/mcp-task-7
```

- [ ] Commit: `feat(skill): route objective questions through mcp`.

## Tarefa 8: Empacotamento para Codex

**Arquivos:**

- Criar: `plugins/magistratura-enam-br/.mcp.json`
- Modificar: `plugins/magistratura-enam-br/.codex-plugin/plugin.json`
- Modificar: `plugins/magistratura-enam-br/scripts/verificar_integracao.py`
- Modificar: `plugins/magistratura-enam-br/tests/test_manifest_interface.py`
- Modificar: `plugins/magistratura-enam-br/tests/test_verificar_integracao.py`

- [ ] Criar teste de manifesto exigindo `mcpServers: "./.mcp.json"` e comando portável relativo ao plugin.
- [ ] Configurar o servidor bundled para iniciar por `stdio` sem caminho absoluto da máquina do autor.
- [ ] Verificar como `PLUGIN_ROOT` é disponibilizado ao processo e evitar comandos dependentes do shell quando houver alternativa.
- [ ] Instalar o plugin em fonte local e iniciar uma sessão limpa do Codex.
- [ ] Executar cenário real com biblioteca temporária: indexar, buscar, criar, renderizar ou aplicar fallback, responder e reiniciar.
- [ ] Registrar evidências e limitações específicas da superfície.
- [ ] Commit: `feat(plugin): bundle local mcp server`.

## Tarefa 9: Conexão privada com ChatGPT

**Arquivos:**

- Criar localmente: `plugins/magistratura-enam-br/.app.json` após registro
- Modificar: `plugins/magistratura-enam-br/.codex-plugin/plugin.json`
- Modificar: `plugins/magistratura-enam-br/.gitignore` ou raiz `.gitignore`, conforme política adotada
- Criar: `plugins/magistratura-enam-br/docs/chatgpt-local.md`
- Criar: `plugins/magistratura-enam-br/tests/test_app_mapping.py`

- [ ] Confirmar o transporte HTTP local com cliente MCP antes de configurar o túnel.
- [ ] Criar endpoint no Secure MCP Tunnel e executar `tunnel-client` no Windows com conexão somente de saída.
- [ ] Registrar o endpoint no modo desenvolvedor do ChatGPT e obter o identificador `plugin_asdk_app...`.
- [ ] Determinar documentalmente se o identificador técnico pode ser versionado. Credenciais e identidade do túnel nunca serão versionadas.
- [ ] Criar `.app.json`, apontar `apps: "./.app.json"` no manifesto e validar os caminhos relativos.
- [ ] Instalar o plugin a partir da fonte local e testar em chat novo.
- [ ] Executar o fluxo ponta a ponta com o widget real e confirmar que os dados foram gravados somente na biblioteca local.
- [ ] Desligar o túnel e confirmar falha segura no ChatGPT e funcionamento preservado no Codex.
- [ ] Commit apenas de arquivos não sensíveis: `feat(plugin): map private chatgpt mcp connection`.

## Tarefa 10: Inicialização com Windows

**Arquivos:**

- Criar: `plugins/magistratura-enam-br/scripts/install_local_service.ps1`
- Criar: `plugins/magistratura-enam-br/scripts/uninstall_local_service.ps1`
- Criar: `plugins/magistratura-enam-br/tests/test_windows_service_scripts.py`
- Modificar: `plugins/magistratura-enam-br/docs/chatgpt-local.md`

- [ ] Escolher mecanismo no escopo do usuário, sem privilégio administrativo, somente depois do fluxo manual funcionar.
- [ ] Testar geração da definição, quoting de caminhos com espaços, diretório de trabalho e variáveis específicas do plugin.
- [ ] Exigir confirmação explícita para instalar e remover a inicialização automática.
- [ ] Implementar desinstalação simétrica sem apagar biblioteca, índice, questões ou tentativas.
- [ ] Reiniciar uma sessão do Windows ou simular o gatilho de forma proporcional e comprovar servidor e túnel ativos.
- [ ] Commit: `feat(windows): add opt-in local mcp startup`.

## Tarefa 11: Gate integrado e documentação

**Arquivos:**

- Modificar: `plugins/magistratura-enam-br/README.md`
- Modificar: `plugins/magistratura-enam-br/CHANGELOG.md`
- Modificar: `plugins/magistratura-enam-br/CONTINUACAO.md`
- Modificar: `docs/site/arquitetura-pedagogica.md`
- Modificar: `docs/site/privacidade-e-persistencia.md`
- Criar: `docs/site/questoes-interativas.md`
- Modificar: `mkdocs.yml`

- [ ] Documentar configuração da biblioteca, arquivos locais, consentimentos, funcionamento nas duas superfícies e aviso de cautela.
- [ ] Documentar claramente que a questão é gerada pelo modelo e que a skill, não o MCP, define sua substância jurídica.
- [ ] Executar a suíte Python integral no diretório temporário do workspace.
- [ ] Executar lint, lock check, testes e build do widget.
- [ ] Executar `mkdocs build --strict`, `git diff --check` e verificador de integração.
- [ ] Fazer auditoria de vazamento pesquisando chaves, correções e credenciais nos payloads públicos e arquivos versionados.
- [ ] Fazer E2E real no Codex e no ChatGPT, com captura de evidência visual e inspeção dos JSONL.
- [ ] Confirmar que nenhum Markdown original mudou.
- [ ] Atualizar versão somente no gate de release expressamente autorizado; não presumir `0.7.0` publicado.
- [ ] Commit: `docs(mcp): document interactive question workflow`.

## Comandos do gate final

```powershell
Set-Location plugins/magistratura-enam-br
uv run python -m pytest tests skills/planejar-jurisprudencia/tests skills/comparar-materiais-enam/tests skills/curar-informativos-stf-stj/tests --basetemp .test-tmp/mcp-final
uv run ruff check .
uv lock --check
uv run python scripts/verificar_integracao.py
Set-Location web
npm ci
npm test -- --run
npm run build
Set-Location ../../..
uv run --project plugins/magistratura-enam-br mkdocs build --strict
git diff --check
git status --short
```

**Resultado esperado:** suíte existente preservada; contratos MCP e UI aprovados; widget funcional nas duas superfícies; gabarito ausente antes da tentativa; Markdown original intacto; questão e tentativa reconstruíveis a partir dos JSONL; nenhuma credencial versionada.

## Gates posteriores

Este plano não autoriza automaticamente:

- implementação funcional;
- instalação persistente no Windows;
- registro definitivo no ChatGPT;
- commit além daquele explicitamente autorizado durante cada tarefa;
- push;
- abertura de PR;
- merge;
- tag, release ou publicação pública.

