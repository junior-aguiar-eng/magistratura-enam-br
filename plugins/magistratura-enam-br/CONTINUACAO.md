# Continuação de manutenção

## Fonte canônica

Trabalhe exclusivamente em `plugins/magistratura-enam-br` no repositório `junior-aguiar-eng/magistratura-enam-br`. O manifesto válido é `.codex-plugin/plugin.json`; não mantenha cópias aninhadas ou versões paralelas. Leia `AGENTS.md` antes de qualquer alteração.

## Candidata 0.7.4 — verificação pontual do índice

- Manifesto, `pyproject.toml` e `uv.lock` identificam a candidata `0.7.4`; a tag estável permanece `v0.7.2` até publicação específica. A instalação do autor deve ser verificada pelo cache efetivo do Codex, não apenas pela versão do manifesto.
- `mcp_server.index_sync` executa uma checagem de hashes e termina; `StudyService.sync_if_changed` não regrava o índice inalterado e não repara estados `missing` ou `invalid`. O conteúdo de cada Markdown elegível é verificado, sem processo residente adicional.
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
