# Continuação — Magistratura ENAM BR

## Fonte canônica

Trabalhe exclusivamente em `plugins/magistratura-enam-br` dentro deste repositório marketplace. A árvore antiga em `outputs/magistratura-enam-br` não é fonte de verdade. Leia `AGENTS.md` integralmente antes de qualquer alteração.

## Estado validado

- Versão do plugin: `0.2.3`.
- Ambiente canônico: `uv`, Python 3.14, `pyproject.toml`, `.python-version` e `uv.lock`.
- Execução: não criar `venv` manual, não usar `pip install` e não usar PEP 723 nos scripts internos deste projeto.
- Testes aprovados: 45.
- Integridade, plugin e lockfile validados com êxito.

## Alterações estruturais já concluídas

1. Estudo para Magistratura: sessão aprofundada integrada; julgado identificado incorporado ao estudo; revisão ativa separada por recuperação, consolidação e véspera.
2. Todas as skills exigem a leitura de `AGENTS.md`.
3. Verificador de integração: somente leitura, sem bytecode; valida a árvore distribuível e `uv lock --check`.
4. Comparador ENAM: `id_item` é o vínculo canônico; o auditor rejeita tipos inválidos, itens duplicados ou órfãos, divergência de tipo e ausência de delta. Os JSON Schemas agora são executados pelo auditor.
5. Planejador: cobertura do ciclo completo, remediação, consolidação, deduplicação e contrato curadoria → esteira.
6. Entrada do planejador: CSV estrito; rejeita coluna ausente, campo vazio, ID duplicado e vocabulário inválido.
7. Dependências do plugin: declaradas no `pyproject.toml`, travadas em `uv.lock`; `requirements*.txt` permanecem como compatibilidade de instalação.

## Comandos obrigatórios de validação

```powershell
uv sync --all-groups
uv run pytest tests skills/planejar-jurisprudencia/tests skills/comparar-materiais-enam/tests skills/curar-informativos-stf-stj/tests --basetemp .test-tmp
uv run python scripts/verificar_integracao.py
python C:\Users\Boni Jr\.codex\skills\.system\plugin-creator\scripts\update_plugin_cachebuster.py .
python C:\Users\Boni Jr\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py .
```

Remova somente `.test-tmp` após a execução. Preserve `.venv`, que é gerenciada por `uv` e ignorada pelo Git.

## Próximo passo sugerido

Prosseguir a auditoria estrutural de forma cadenciada. Os eixos já corrigidos são integração, comparador, planejador, ambiente `uv` e execução dos schemas. Antes de novo redesenho funcional, inspecione o próximo contrato ainda sem cobertura equivalente — prioritariamente os limites entre curadoria, geração de PDF e planilha de precedentes.

## Cuidado com o repositório

O worktree já contém alterações anteriores do usuário e desta revisão. Não use `git reset`, `git checkout` destrutivo ou remoção ampla. Preserve alterações não relacionadas e atualize o cachebuster somente depois de uma alteração validada.
