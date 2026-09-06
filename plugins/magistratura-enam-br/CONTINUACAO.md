# Continuação de manutenção

## Fonte canônica

Trabalhe exclusivamente em `plugins/magistratura-enam-br` no repositório `junior-aguiar-eng/magistratura-enam-br`. O manifesto válido é `.codex-plugin/plugin.json`; não mantenha cópias aninhadas ou versões paralelas. Leia `AGENTS.md` antes de qualquer alteração.

## Estado confirmado em 2026-09-05

- Versão sincronizada no manifesto, em `pyproject.toml` e no `uv.lock`: `0.7.0`.
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
- Integração contínua: o workflow de raiz `.github/workflows/validar.yml` executa a suíte canônica, no diretório do plugin, em `push` e pull request.
- Árvore versionada: limpa após a auditoria; ambientes e caches locais permanecem ignorados pelo Git.

## Questões interativas — 0.7.0

- Servidor MCP, widget, persistência local e indexação recursiva integrados na versão `0.7.0`.
- Codex usa o servidor empacotado por `stdio`; ChatGPT usa conexão privada previamente registrada, sem credenciais versionadas.
- O modelo gera a questão; a skill governa o conteúdo jurídico; o MCP executa persistência, isolamento do gabarito, renderização e correção.
- Inicialização automática do túnel é opt-in, limitada a `HKCU` e removível sem apagar biblioteca ou histórico.
- O runner é um supervisor persistente: valida executável, perfil e diretório, usa mutex para evitar duplicidade, acompanha a instância efetiva e reinicia o túnel cinco segundos após uma queda. PIDs e logs operacionais ficam em `%LOCALAPPDATA%`.
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

Não crie ambiente virtual manualmente, não use `pip install` nos scripts internos e não versione `.venv`, caches, bytecode ou saídas temporárias.
## Fase 6 — candidata 0.4.0

Implementados: skill de acompanhamento, relatório local, contratos de roteamento, fechamento rastreável de remediação, avaliação final com 48 execuções e documentação de migração. Gates automatizados e revisões independentes automatizadas aprovados após correções.

Revisão humana de `evals/pedagogia/relatorio-final.md` e das amostras em `evals/pedagogia/fase-6/runs/` aprovada pelo responsável pelo repositório em 4 de setembro de 2026.

Instalação limpa isolada aprovada para a candidata `0.4.0`: quinta skill e relatório presentes, sem criação implícita de perfil ou log. Gates técnicos finais: 161 testes, Ruff, lock, integração e validador do plugin aprovados.
