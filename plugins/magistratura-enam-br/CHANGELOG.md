# Changelog

Todas as alterações relevantes deste plugin são registradas neste arquivo.

## Não publicado

- Torna canônico e obrigatório o padrão FGV/ENAM para questões objetivas, com trava de pré-emissão, matriz de construção e auditoria contra gabarito genérico, enunciado artificial, alternativas assimétricas e regra específica ignorada.

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
