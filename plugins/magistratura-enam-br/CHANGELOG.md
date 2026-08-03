# Changelog

Todas as alterações relevantes deste plugin são registradas neste arquivo.

## 0.3.0 — 2026-08-03

- Torna canônico e obrigatório o padrão FGV/ENAM para questões objetivas, com trava de pré-emissão, matriz de construção e auditoria contra gabarito genérico, enunciado artificial, alternativas assimétricas e regra específica ignorada.
- Estende a sanitização de fórmulas de planilha (já aplicada na curadoria de precedentes) aos scripts da esteira de jurisprudência: `atualizar_esteira.py` (abas Entrada/Revisao/Remediacao/Semana/Config) e `preparar_itens_esteira.py` (CSV de itens) agora neutralizam valores iniciados em `=`, `+`, `-` ou `@` antes de gravá-los, fechando um vetor de injeção de fórmula ao abrir os artefatos no Excel.
- Padroniza a execução dos testes por `uv run python -m pytest`, evitando a falha do trampoline do `uv` em instalações Windows cujo caminho contém espaços.
- Move o workflow de validação para a raiz do repositório e fixa o diretório de trabalho no plugin, para que o GitHub Actions o descubra e execute a suíte correta.

## 0.2.4 — 2026-08-01

- Remove manifesto aninhado e obsoleto que mantinha a versão `0.2.2` em paralelo ao manifesto canônico.
- Cria documentação de entrada (`README.md`) e consolida o roteiro de manutenção em `CONTINUACAO.md`.
- Atualiza a documentação da esteira para incluir a aba `Remediacao` na interface estável.
- Passa a ignorar explicitamente o cache do Ruff.
- Corrige mensagem com codificação inválida no auditor de rastreabilidade e torna a validação documentada independente de caminho local.
- Adiciona validação contínua, contrato local do manifesto e cenários versionados de avaliação para curadoria e questões.

## 0.2.3 — 2026-08-01

- Fixa o ambiente canônico em Python 3.14 e sincroniza `pyproject.toml`, `.python-version` e `uv.lock`.
- Fortalece a validação do ciclo da esteira e elimina leitura duplicada do CSV inicial.
- Atualiza o verificador de integração e seus testes para a configuração atual.

## 0.2.2 — 2026-07-27

- Publica a identidade visual do plugin e aperfeiçoa os contratos de curadoria, comparação e planejamento.
