# Changelog

## [0.4.0] - 2026-09-04

### Adicionado

- Acompanhamento unificado com roteamento entre cinco skills.
- Relatório local de tentativas, precisão, reincidência, retenção e confiança.
- Transporte rastreável de referências e fechamento confirmado de remediação.
- Avaliação pedagógica final com 48 execuções da versão candidata.

### Alterado

- Política fixa preservada como padrão, com adaptação somente em modo sombra e opt-in.
- Persistência documentada como local, opcional e sem memória automática.
- Casos pedagógicos subespecificados receberam fixtures sintéticas explícitas.

Todas as alterações relevantes deste plugin são registradas neste arquivo.

## 0.3.3 — 2026-09-04

- Eleva o requisito mínimo de `pypdf` para `6.16.1` e resolve o ambiente com `6.17.0`, corrigindo seis alertas moderados do Dependabot relacionados ao processamento de PDFs malformados ou adversariais.

## 0.3.2 — 2026-08-08

- Sincroniza a versão `0.3.2` entre manifesto, `pyproject.toml` e `uv.lock`, declara as capacidades efetivas do plugin e torna essas invariantes obrigatórias no verificador de integração.
- Substitui a instalação global com `pip --user` por `uv sync --no-dev` no ambiente isolado do plugin.
- Torna obrigatória a correção completa de questões objetivas mesmo após acerto, com resultado direto, fundamento determinante, aplicação às pistas do enunciado, exame individual dos distratores e distinção final útil para prova.
- Passa a tratar prova, caderno e correção-modelo aprovados pelo candidato como corpus de calibração do comportamento da skill, sem copiar redação nem conservar imprecisões jurídicas ou alegações empíricas sem fonte.
- Adiciona cenário e testes de contrato específicos para impedir correções telegráficas, omissão dos distratores e confusão entre Constituição jurídico-positiva e norma fundamental hipotética.
- Garante o fechamento dos workbooks da esteira em fluxos normais, erros e retornos antecipados, reduzindo o risco de bloqueio de planilhas no Windows.
- Centraliza em `conftest.py` a leitura de arquivos usada pelos testes de contrato e amplia os casos de sanitização contra fórmulas ocultas por whitespace.

## 0.3.1 — 2026-08-05

- Fixa a versão do Ruff como dependência de desenvolvimento (`uv add --dev ruff`) e troca `uvx ruff check .` por `uv run ruff check .` no workflow, eliminando a resolução flutuante da versão mais recente do Ruff a cada execução do CI — comportamento que já havia se mostrado não determinístico entre execuções.
- Corrige os apontamentos reais de lint expostos por essa fixação: variável ambígua `l` em `atualizar_esteira.py` e declarações múltiplas separadas por `;` em `test_schemas.py`.
- Marca como executáveis (`chmod +x`) os scripts com shebang que não tinham essa permissão no Git, resolvendo os alertas `EXE001` reportados pelo Ruff a partir da versão 0.16.

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

