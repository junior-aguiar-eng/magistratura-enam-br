# Continuação de manutenção

## Incrementos MCP — task 5, 2026-10-03

Executada na branch `codex/incrementos-mcp-calibracao`, a partir de `d00540c`, por autorização específica. Revisão ancorada reutiliza o protocolo de acervo e conserva recuperação, consolidação e véspera; material anterior inacessível exige apenas recorte/checkpoint, sem memória fabricada. Notícia sem fundamentos não permite reconstruir ratio, modulação ou trânsito. Mudança de base é expressa e não suspende a política de fontes.

Os formatos direto, numerado, V/F e associação e os desenhos soluções, matriz e fundamento preservam núcleo funcional, cinco alternativas, chave única, paridade e correção integral. Combinações exigem ordem/reutilização claras, sem duplicação; correção explica componentes e erros das quatro alternativas após tentativa, inclusive no acerto. `initialize.instructions` transmite o mínimo desses contratos; prompt/alternativas/correção existentes acomodam os formatos, sem migração ou campo novo.

Validação: RED contratual com 11 falhas novas e oito testes anteriores aprovados, seguido de 19/19; suíte completa com 388 testes Python aprovados (68,72 s), Ruff, lockfile e 42 verificações de integração aprovados. Avaliação comportamental usa cinco sessões limpas anteriores e cinco candidatas para associação/matriz, correção após tentativa, revisão de trecho, material anterior inacessível e V/F. [Registros e rubrica posterior](evals/pedagogia/task5/README.md) preservam origem, instruções, hashes e pendência humana. O controle já gerava associações; a amostra não comprova superioridade geral nem representa homologação do modelo no ChatGPT.

AGENTS permanece sem novas diretrizes porque a aprovação humana não foi obtida, como permite o plano. Manifesto continua 0.7.5; tasks 6–8, push, reinstalação e publicação não integram esta autorização.


## Incrementos MCP — task 4, 2026-10-03

Executada na branch `codex/incrementos-mcp-calibracao`, a partir de `9d65d2e`, por autorização específica. O snapshot visual versionado aceita somente sessão, escolha pendente A–E e abertura dos painéis; campos extras/inválidos e outra sessão são rejeitados. A escolha só é restaurada em ready; answered segue a resposta do servidor, e invalidated limpa o estado visual. Armazenamento OpenAI é opcional, inclusive com SDK para ferramentas; indisponibilidade conserva a interação React, sem localStorage ou memória entre sessões.

O SDK anuncia inline/fullscreen e usa `requestDisplayMode`; o bridge legado detecta seu método antes de oferecer controle. Clique solicita expansão ou retorno, com trava enquanto pendente e falha acessível. Resposta com outro modo mantém esse modo; notificação externa mais recente vence ACK atrasado. Não há Fullscreen API do navegador, expansão automática ou chamada de ferramenta por troca de apresentação. Tema/variáveis são aplicados pelos helpers do SDK, com fallback CSS e restauração no fechamento; altura e safeAreaInsets reservam espaço para o host. Os recursos v2/v1 anunciam os modos também em `openai/ui`.

Validação local: 377 testes Python e 94 web aprovados, TypeScript/build, Ruff/lockfile, 42 verificações de integração e auditoria npm sem vulnerabilidades. QA no navegador com host sintético: questões/correções longas, painéis expandidos até fontes, roundtrip ready/answered/invalidated, teclado/foco, claro/escuro, viewport 360 px e zoom 200% (separadamente), movimento reduzido sem transição e composer simulado acessível. Esse ensaio não comprova operação no ChatGPT real; a task 8 continua responsável pela homologação. Bundle regenerado; manifesto permanece 0.7.5, sem push/reinstalação/publicação nesta task. Nenhuma evidência de cache de host foi obtida: URIs preservadas e eventual revisão de URI depende da homologação.


Revisão independente de `9d65d2e..b366a2c`: dois achados importantes, nenhum crítico ou menor. O retorno desaparecia quando o host permitia somente inline durante fullscreen; nova dimensão sem limite de altura preservava o limite anterior. Ambos foram reproduzidos em três testes RED e corrigidos em uma única passagem: o controle considera o destino permitido, e dimensão explicitamente recebida sem altura remove a variável, enquanto notificação sem dimensões preserva o valor. A suíte web completa passou com 94 testes; TypeScript/build foram repetidos e o bundle regenerado. Não houve segunda revisão independente após as correções.

## Incrementos MCP — task 3, 2026-10-03

Executada na branch `codex/incrementos-mcp-calibracao`, a partir de `1934373`, por autorização específica. `obter_questao` anuncia saída de sessão e acesso modelo/app sem template de UI; reutiliza a projeção atual do repositório, preservando arquivos e logs. O card consulta essa ferramenta antes de preparar a continuidade e a instrução canônica determina nova consulta pelo modelo antes de atender.

Após tentativa, estão disponíveis explicação do erro (somente em erro), aprofundamento da distinção e pedido de outra questão. Invalidação mantém apenas o último pedido, com aviso. O SDK usa mensagens/contexto negociados; OpenAI usa `sendFollowUpMessage`. Ausência de mensagens oferece texto selecionável. O contexto contém apenas versão, sessão, ação, disciplina, tema e estado; cada atualização substitui a anterior. Nenhuma ação gera questão, registra tentativa ou modifica perfil automaticamente.

Trava por sessão/instância impede cliques duplicados; mudança de sessão durante consulta/contexto interrompe o pedido antigo. Falha de contexto não impede a mensagem autossuficiente, e falha de envio permite nova tentativa explícita. A leitura não refocaliza a correção já lida. CSS mínimo organiza botões responsivos e textarea sem nova biblioteca.

Validação local: 377 testes Python e 57 web (16 do adaptador, 32 do widget, oito de followup e um build real), TypeScript, build, Ruff, lockfile, 42 checks de integração e MkDocs estrito aprovados; auditoria npm sem vulnerabilidades. A asserção anterior de visibilidade foi atualizada para a nova consulta sem expor template. Bundle regenerado da fonte canônica. Homologação visual e comportamento do modelo no ChatGPT real permanecem na task 8; fullscreen na task 4. Manifesto continua em 0.7.5; este ciclo não publica nem reinstala o plugin.

Revisão independente de `1934373..d79bd59`: um achado importante, nenhum crítico ou menor. Entrada de outra sessão durante confirmação do contexto, sem resultado novo ainda, permitia enviar pedido antigo porque a UI aguardava o resultado para trocar seu estado. O caso foi reproduzido RED e corrigido: `sendMessage(text, sessionId)` verifica a sessão vinculada no adaptador imediatamente antes do despacho e após a confirmação. A suíte web completa passou com 57 testes e o bundle foi regenerado. Não houve segunda revisão independente após a correção.

## Incrementos MCP — task 2, 2026-10-02

Executada na branch `codex/incrementos-mcp-calibracao`, a partir de `04c1be8`, por pedido específico do usuário. `QuestionHost` concentra conexão, chamadas e fechamento; `bindSession` ancora a questão inicial e a entrada completa do host. O widget usa um único transporte, trava submissão e incerteza por sessão e reconcilia falhas por `renderizar_questao`, sem nova mutação automática. A entrada do host não é conteúdo renderizável, e projeção pública não aceita campos de tentativa.

Vitest inclui agora testes `.ts` previstos no plano. Validação: 37 testes web (14 do adaptador, 22 do widget e um build real), 374 testes Python, TypeScript, build, Ruff, lockfile, 42 verificações de integração e MkDocs estrito aprovados. O bundle `web/dist/index.html` foi regenerado da fonte canônica. Os avisos de comentários PURE da dependência Zod permanecem não impeditivos.

O gate de auditoria npm identificou `braces` vulnerável sem versão corrigida na cadeia de `vite-plugin-singlefile`. Esse empacotador foi substituído por um plugin Vite restrito ao único HTML do widget, sem seleção por glob; o teste compila JS/CSS/SVG e valida incorporação e escape de delimitadores HTML. `npm audit --audit-level=moderate` passou sem vulnerabilidades após a remoção. `@types/jsdom` serve somente à tipagem do teste de build.

As capacidades de mensagens/contexto são expostas para a task 3; seus métodos e ações ainda não foram implementados. Fullscreen permanece na task 4. Nenhum acervo pessoal ou log foi alterado; release/reinstalação e homologação no ChatGPT não integram esta task.

Revisão independente de `04c1be8..cce81f5` identificou dois achados importantes: resultado malformado e cancelamento pelo host mantinham carregamento indefinido. Em 2026-10-03, ambos foram reproduzidos com testes RED e corrigidos: o adaptador comunica falha sem propagar payload privado, descarta resultados identificáveis de sessão antiga antes de validá-los e trata `ontoolcancelled`. Os 37 testes passaram após a correção, com novo build do bundle. Nenhum achado crítico ou menor foi confirmado; não houve segunda revisão independente após a correção.

## Incrementos MCP — task 1, 2026-10-02

Plano/spec aprovados e versionados na branch `codex/incrementos-mcp-calibracao`, a partir de `main` em `8b245f1`. O pedido vigente executa somente a task 1; tasks 2–8 permanecem pendentes, incluindo fullscreen na task 4. Manifesto e pacote continuam em 0.7.5; esta alteração ainda não constitui release ou reinstalação.

`mcp_server/instructions.py` extrai um bloco único de `references/questoes-interativas-mcp.md`; o SDK o anuncia em `initialize.instructions`. `mcp_server/outputs.py` deriva o schema público/corrigido da sessão canônica, expande referências locais para o registro Pydantic e valida a projeção na saída. Demais saídas usam TypedDict. Não houve atualização de dependências, alteração de logs ou regeneração de widget. Visibilidade de renderização/resposta inclui modelo e app; ferramentas de gestão ficam para o modelo.

Validação: 374 testes Python aprovados (62,56 s), Ruff, lockfile e 42 verificações de integração aprovadas. Discovery e chamadas reais por cliente MCP, `stdio` e HTTP local usam apenas biblioteca sintética. A saída pública também rejeita campos de tentativa para evitar revelação indireta da chave. A inicialização foi verificada no protocolo; aplicação dessas instruções pelo modelo e homologação visual no ChatGPT são limites distintos.

Revisão independente do intervalo `8b245f1..b062ce0` aprovada, sem achados críticos, importantes ou menores. O revisor verificou adicionalmente, com cliente MCP real, que retorno privado inválido gera erro sem conteúdo privado no envelope e que sessões corrigidas históricas continuam legíveis. As tasks posteriores e a homologação no ChatGPT permanecem pendentes conforme o plano.

## Release 0.7.5 — 2026-10-02

Versão 0.7.5 sincronizada no manifesto e no ambiente Python. O usuário autorizou commit, push, reinstalação e publicação em 2026-10-02. As correções foram integradas com os três commits novos de main; a publicação exige os gates desta árvore final. O repositório remoto foi confirmado público. Nenhuma tarefa agendada ou indexação pessoal é ativada pela release.

Gates locais repetidos após integrar main: 364 testes Python aprovados (70,44 s), 15 testes do widget, TypeScript, build, Ruff, lockfile e 42 verificações de integração; npm audit sem vulnerabilidades e builds Zensical/MkDocs estrito aprovados. CI remoto, tag e reinstalação devem ser conferidos nos respectivos registros operacionais.

Os alertas de dependências identificados no push motivaram atualização pontual do lockfile: PyJWT 2.15.1, pypdf 6.19.0 e urllib3 2.8.0, mantendo as restrições existentes. Após essa atualização, os 364 testes Python passaram novamente (66,64 s), assim como Ruff, lockfile e integração. pip-audit sobre o export completo do lockfile, incluindo grupos de desenvolvimento e documentação, não encontrou vulnerabilidades conhecidas.

## Correções locais da auditoria — etapa anterior à release

Na etapa de correção, as sete frentes da auditoria receberam correções locais, antes da autorização para instalação e publicação. O plano está em `docs/superpowers/plans/2026-10-02-correcoes-auditoria-plugin.md` na raiz do repositório. Eventos novos usam 2.1; logs 1.x/2.0 permanecem legíveis e retries antigos não os reescrevem. Invalidações pós-tentativa são append-only e retiram a atividade das projeções reconstruídas com o log completo. Nenhum acervo pessoal foi migrado.

A ferramenta `invalidar_questao` aceita motivo explícito; repetir com o mesmo motivo conclui gravação parcial. O widget usa o SDK MCP Apps, mantém `window.openai` e apresenta a correção completa após a tentativa. A reconstrução explícita do índice tolera conteúdo anterior inválido; a sincronização automática preserva a política de não reparo.

O benchmark deixa de exigir revisão eternamente pendente. Aprovação ou rejeição da fixture exige revisor, data e nota; o registrador de execuções preserva versão/modelo/cliente, sessão, rodada, saída, hash e revisão por critério. Revisões jurídicas reais e homologação visual no Codex/ChatGPT não foram realizadas por esta alteração.

Validação final deste ciclo: 364 testes Python, 15 testes do widget com SDK real e host simulado, TypeScript, build Vite, Ruff e 42 verificações de integração aprovados. A revisão independente identificou regressões por notificações atrasadas, payloads malformados e reaproveitamento de revisão após mudar o caso; os três achados foram reproduzidos e corrigidos. O build contém avisos não impeditivos de comentários da dependência Zod. O bundle distribuído foi regenerado. Esse registro de validação antecede os commits, a instalação, o push e a publicação da release.

## Fonte canônica

Trabalhe exclusivamente em `plugins/magistratura-enam-br` no repositório `junior-aguiar-eng/magistratura-enam-br`. O manifesto válido é `.codex-plugin/plugin.json`; não mantenha cópias aninhadas ou versões paralelas. Leia `AGENTS.md` antes de qualquer alteração.

## Candidata 0.7.4 — verificação pontual do índice

- Manifesto, `pyproject.toml` e `uv.lock` identificam a candidata `0.7.4`; a tag estável permanece `v0.7.2` até publicação específica. A instalação do autor deve ser verificada pelo cache efetivo do Codex, não apenas pela versão do manifesto.
- `mcp_server.index_sync` executa uma checagem de hashes e termina; `StudyService.sync_if_changed` não regrava o índice inalterado e não repara estados `missing` ou `invalid`. O conteúdo de cada Markdown elegível é verificado, sem processo residente adicional.
- `SINCRONIZAR_ACERVO.bat` executa a mesma checagem sob demanda, por duplo clique, usando por padrão `.runtime/library-config.json`; não registra tarefa agendada.
- `scripts/install_index_sync.ps1` registra tarefa separada do túnel no login e a cada dez minutos; `scripts/uninstall_index_sync.ps1` remove apenas essa tarefa. O status mais recente fica em `.runtime/index-sync/last-run.json`, ignorado pelo Git.
- O runner registra saída e código mesmo quando o processo emite `stderr`; o verificador de integração exclui `.runtime` por não integrar a árvore distribuível.
- A primeira indexação continua explícita por `indexar_acervo(confirmar_gravacao_local=true)`. Não confundir instalação da tarefa no computador do autor com distribuição da candidata ou homologação em outros ambientes.

## Candidata 0.7.3 em 2026-09-24

- Na etapa anterior desta branch, manifesto, `pyproject.toml` e lock identificavam a candidata `0.7.3`; a versão estável por tag permanecia `v0.7.2`. Push da branch, build e instalação são gates operacionais distintos; não presumir tag, PR ou merge.
- O MCP novo expõe `diagnosticar_acervo` somente para leitura: distingue índice ausente, estruturalmente válido e inválido, sem afirmar atualização perante os arquivos da biblioteca. A validação do índice foi alinhada ao indexador para cabeçalhos longos, extensão `.MD` e H1 sem texto útil. Busca e questões foram exercitadas com fixture sintética e transporte `stdio`; não houve acesso ao acervo pessoal.
- O benchmark jurídico piloto contém oito casos sintéticos e referências oficiais, mas sua revisão jurídica independente e as três execuções limpas por caso permanecem pendentes. Por decisão do usuário, a candidata será experimentada em uso real: os casos formais não são pré-requisito desse piloto e não devem ser apresentados como aprovados. Os testes de schema não comprovam qualidade semântica nem aprovam o gabarito.
- ChatGPT com túnel não foi homologado neste ciclo: não havia túnel operacional e a consulta local a `/readyz` retornou HTTP 404. A documentação distingue esse limite do fluxo Codex local.
- Gates executados nesta candidata: `uv sync --all-groups`; `uv run python -m pytest tests skills/planejar-jurisprudencia/tests skills/comparar-materiais-enam/tests skills/curar-informativos-stf-stj/tests -q --basetemp .pytest-install-073` (323 aprovados); Ruff; `uv lock --check`; verificador de integração (42 checks, zero erros); `npm ci`, quatro testes do widget, lint, auditoria sem vulnerabilidades e build; builds MkDocs estrito e Zensical. O teste estrutural do plugin não substitui revisão jurídica humana ou smoke na interface do ChatGPT.
- Open Notebook e ingestão de PDFs/OCR não foram incluídos: a avaliação de multimodalidade exigiria amostra não sensível, citação localizável por página e comparação de qualidade e privacidade com o índice Markdown.

## Estado em 2026-09-22

- Versão sincronizada no manifesto, em `pyproject.toml` e no `uv.lock`: `0.7.2`, publicada na tag `v0.7.2`.
- A versão `0.7.2` distribui as correções documentais de instalação, MCP, supervisor Windows e catálogo de skills feitas após a tag `v0.7.1`; não altera o comportamento do plugin.
- Ambiente canônico: `uv` com Python 3.14, fixado em `.python-version` e resolvido em `uv.lock`.
- Linha de base: 207 testes aprovados na arquitetura conversacional e de fontes `0.5.0`; candidata `0.6.0`: 238 testes aprovados no gate integrado.

## Profissionalização 0.6.0

- **Preservadas:** precisão jurídica, política de fontes, acervo, cinco rotas públicas, transições, trava objetiva, campos de curadoria, ciclos fixos, rastreabilidade documental e log append-only.
- **Aprofundadas:** identidade para bacharéis, dogmática integrada, casos complexos, discursiva, oral, revisão, evidência por assistência e avaliação semântica.
- **Realocadas:** fluidez para o contrato conversacional; dogmática e casos para referências próprias; discursiva e oral para arquivos especializados.
- **Generalizadas:** defaults pessoais foram substituídos por perfil declarado opcional; extensão da curadoria tornou-se proporcional à função do campo.
- **Removidas:** somente a referência combinada de discursiva e oral, depois da preservação integral de suas capacidades nos dois destinos e nos respectivos testes.
- Qualidade estática: `ruff check .` aprovado.
- Integridade: verificador interno de contrato do plugin e `uv lock --check` aprovados.
- Ambientes e caches locais permanecem ignorados pelo Git.

## Questões interativas — 0.7.0

- Servidor MCP, widget, persistência local e indexação recursiva integrados na versão `0.7.0`.
- A versão `0.7.1` corrige o manifesto MCP, reconcilia evento pedagógico após falha parcial e restringe o transporte HTTP ao loopback.
- O workflow de raiz `.github/workflows/validar.yml` executa a suíte canônica, a instalação pelo CLI do Codex e os gates do widget em `push` e pull request.
- Validação local da versão: suíte Python, Ruff, verificador de integração, validador do plugin, lockfile, quatro testes do widget, auditoria npm sem alertas e builds Zensical/MkDocs aprovados.
- Codex usa o servidor empacotado por `stdio`; ChatGPT usa conexão privada previamente registrada, sem credenciais versionadas.
- O modelo gera a questão; a skill governa o conteúdo jurídico; o MCP executa persistência, isolamento do gabarito, renderização e correção.
- Inicialização automática do túnel é opt-in, registrada no Agendador de Tarefas para o usuário atual e removível sem apagar biblioteca ou histórico; a chave legada de `HKCU\...\Run` é retirada na migração.
- O runner é um supervisor persistente lançado pelo Agendador de Tarefas, não pelo shell instalador: valida executável, perfil e diretório, usa mutex para evitar duplicidade, acompanha a instância efetiva e reinicia o túnel cinco segundos após uma queda. O próprio supervisor recebe política de reinício do Windows. Perfil copiado, PIDs e logs operacionais ficam em `.runtime/startup`, ignorado pelo Git e compartilhado com o contexto do Agendador.
- O widget lê `ui/notifications/tool-result` em `params.structuredContent`, mantém compatibilidade legada e usa `ui://estudo-juridico/questao/v2.html` para evitar recurso visual obsoleto em cache; `v1.html` continua registrado como alias durante a atualização de catálogos existentes.
- Os metadados de `criar_sessao_questao` e `renderizar_questao` tornam obrigatório o card interativo para pedidos de questão quando o MCP estiver disponível; fallback textual exige falha explícita da chamada.

## Contratos que exigem preservação

1. Todas as `SKILL.md` leem e cumprem `AGENTS.md`.
2. O comparador usa `id_execucao` e `id_item` como vínculos canônicos e valida JSON Schema antes das regras semânticas.
3. A curadoria preserva a rastreabilidade de precedentes, a sanitização de fórmulas em planilhas e a validação de PDF e boletim.
4. A esteira mantém as abas `Entrada`, `Revisao`, `Remediacao`, `Semana` e `Config`; o CSV de entrada é estrito, a remediação integra o ciclo de revisão, todo valor gravado em planilha ou CSV passa por sanitização de fórmula antes da escrita e todo workbook é fechado inclusive em erros ou retornos antecipados.
5. O verificador de integração é estritamente de leitura e não cria artefatos na árvore distribuível.
6. Questões objetivas seguem a trava canônica FGV/ENAM: matriz de núcleo, fatos e alternativas; gabarito aplicado à regra determinante; enunciado funcionalmente denso; distratores com paridade; e invalidação do rascunho diante de ambiguidade ou assimetria.
7. A correção objetiva é completa mesmo após acerto: resultado direto, fundamento desenvolvido, aplicação ao enunciado, análise individual dos distratores e chave de prova; exemplos aprovados e cadernos da FGV funcionam como corpus de calibração, sem substituir o rigor jurídico.
8. Manifesto, `pyproject.toml` e `uv.lock` mantêm a mesma versão; `interface.capabilities` declara ao menos uma capacidade efetivamente implementada.
9. O processamento de PDFs exige `pypdf>=6.16.1`; versões anteriores permanecem vedadas por vulnerabilidades de negação de serviço em entradas adversariais.
10. A política adaptativa de jurisprudência permanece em modo sombra: registra intervalo e motivo sugeridos, mas `proxima_revisao` continua governada pelo ciclo fixo. Planilhas antigas recebem cinco colunas ao final sem perda dos dados existentes.
11. Pedido genérico recebe ambientação breve; pedido específico segue diretamente à skill competente sem menu redundante.
12. Mudança de tema preserva modalidade, mudança de modalidade preserva tema e menção incidental não cria rota, pendência ou suspensão.
13. A política de fontes distingue acervo exclusivo, validação oficial e pesquisa completa; fontes editoriais não substituem STF, STJ, Planalto ou órgão oficial competente.
14. A interface principal expõe no máximo três prompts, conforme o contrato do Codex; informativos, comparação e revisão usam os gatilhos próprios das skills.

## Validação obrigatória

```powershell
uv sync --all-groups
uv lock --check
uv run python -m pytest tests skills/planejar-jurisprudencia/tests skills/comparar-materiais-enam/tests skills/curar-informativos-stf-stj/tests
uv run ruff check .
uv run python scripts/verificar_integracao.py
```

No widget, execute a partir de `web/`: `npm ci`, `npm audit --audit-level=moderate`, `npm test -- --run`, `npm run lint` e `npm run build`. O CI instala o bundle com o CLI do Codex para verificar o contrato externo do plugin.

Não crie ambiente virtual manualmente, não use `pip install` nos scripts internos e não versione `.venv`, caches, bytecode ou saídas temporárias.
## Fase 6 — candidata 0.4.0

Implementados: skill de acompanhamento, relatório local, contratos de roteamento, fechamento rastreável de remediação, avaliação final com 48 execuções e documentação de migração. Gates automatizados e revisões independentes automatizadas aprovados após correções.

Revisão humana de `evals/pedagogia/relatorio-final.md` e das amostras em `evals/pedagogia/fase-6/runs/` aprovada pelo responsável pelo repositório em 4 de setembro de 2026.

Instalação limpa isolada aprovada para a candidata `0.4.0`: quinta skill e relatório presentes, sem criação implícita de perfil ou log. Gates técnicos finais: 161 testes, Ruff, lock, integração e validador do plugin aprovados.
