# Estudos Jurídicos de Alto Nível

Plugin para apoio ao estudo de Direito brasileiro voltado à Magistratura e ao Exame Nacional da Magistratura (ENAM). Ele reúne curadoria de informativos, estudo ativo, comparação de materiais do ENAM e planejamento de revisão de jurisprudência.

## Skills disponíveis

| Skill | Finalidade |
| --- | --- |
| `comparar-materiais-enam` | Compara versões de materiais do ENAM por tema e subtema, com quadro de deltas rastreáveis. |
| `curar-informativos-stf-stj` | Seleciona e comenta julgados de informativos do STF e do STJ. |
| `estudar-direito-magistratura` | Explica, revisa e treina Direito brasileiro em nível compatível com a Magistratura. |
| `planejar-jurisprudencia` | Organiza a revisão espaçada de julgados já selecionados. |

Cada skill lê `AGENTS.md` antes de atuar. As diretrizes preservam rigor jurídico, uso proporcional de fontes oficiais, estudo ativo e fronteiras claras entre curadoria, estudo, comparação e planejamento.

## Ambiente de desenvolvimento

O projeto usa `uv` e Python 3.14. Instale as dependências de desenvolvimento com:

```powershell
uv sync --all-groups
```

Não crie ambiente virtual manualmente nem use `pip install` para os scripts internos. O ambiente, caches e arquivos temporários não fazem parte da distribuição.

## Validação

Execute, a partir desta pasta:

```powershell
uv lock --check
uv run python -m pytest tests skills/planejar-jurisprudencia/tests skills/comparar-materiais-enam/tests skills/curar-informativos-stf-stj/tests
uvx ruff check .
uv run python scripts/verificar_integracao.py
```

O verificador interno é somente leitura: ele valida arquivos distribuíveis, contrato do manifesto e das skills, JSON, sintaxe Python, coerência de versão e o lockfile, sem criar artefatos no código-fonte.

O workflow de raiz `.github/workflows/validar.yml` executa essa mesma sequência, no diretório do plugin, em cada `push` e pull request.

## Estrutura relevante

- `.codex-plugin/plugin.json`: manifesto canônico do plugin.
- `AGENTS.md`: diretrizes obrigatórias para manutenção e execução das skills.
- `CHANGELOG.md`: histórico de alterações publicáveis.
- `CONTINUACAO.md`: estado técnico e roteiro de manutenção.
- `skills/`: instruções, referências, modelos, scripts e testes de cada skill.

Consulte o [changelog](CHANGELOG.md) antes de atualizar ou publicar o plugin.
