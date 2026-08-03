# Continuação de manutenção

## Fonte canônica

Trabalhe exclusivamente em `plugins/magistratura-enam-br` no repositório `junior-aguiar-eng/magistratura-enam-br`. O manifesto válido é `.codex-plugin/plugin.json`; não mantenha cópias aninhadas ou versões paralelas. Leia `AGENTS.md` antes de qualquer alteração.

## Estado confirmado em 2026-08-03

- Versão declarada no manifesto: `0.3.0`.
- Ambiente canônico: `uv` com Python 3.14, fixado em `.python-version` e resolvido em `uv.lock`.
- Suíte de testes: 82 testes aprovados.
- Qualidade estática: `ruff check .` aprovado.
- Integridade: verificador interno de contrato do plugin e `uv lock --check` aprovados.
- Integração contínua: o workflow de raiz `.github/workflows/validar.yml` executa a suíte canônica, no diretório do plugin, em `push` e pull request.
- Árvore versionada: limpa após a auditoria; ambientes e caches locais permanecem ignorados pelo Git.

## Contratos que exigem preservação

1. Todas as `SKILL.md` leem e cumprem `AGENTS.md`.
2. O comparador usa `id_execucao` e `id_item` como vínculos canônicos e valida JSON Schema antes das regras semânticas.
3. A curadoria preserva a rastreabilidade de precedentes, a sanitização de fórmulas em planilhas e a validação de PDF e boletim.
4. A esteira mantém as abas `Entrada`, `Revisao`, `Remediacao`, `Semana` e `Config`; o CSV de entrada é estrito, a remediação integra o ciclo de revisão, e todo valor gravado em planilha ou CSV passa por sanitização de fórmula antes da escrita.
5. O verificador de integração é estritamente de leitura e não cria artefatos na árvore distribuível.
6. Questões objetivas seguem a trava canônica FGV/ENAM: matriz de núcleo, fatos e alternativas; gabarito aplicado à regra determinante; enunciado funcionalmente denso; distratores com paridade; e invalidação do rascunho diante de ambiguidade ou assimetria.

## Validação obrigatória

```powershell
uv sync --all-groups
uv lock --check
uv run python -m pytest tests skills/planejar-jurisprudencia/tests skills/comparar-materiais-enam/tests skills/curar-informativos-stf-stj/tests
uvx ruff check .
uv run python scripts/verificar_integracao.py
```

Não crie ambiente virtual manualmente, não use `pip install` nos scripts internos e não versione `.venv`, caches, bytecode ou saídas temporárias.
