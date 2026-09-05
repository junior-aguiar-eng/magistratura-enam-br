# Avaliação da profissionalização 0.6.0

## Protocolo

- Baseline: 0.5.0.
- Candidata: 0.6.0.
- Execução: três sessões limpas por caso central.
- Casos centrais: dogmática com fontes integradas, continuidade dogmática, caso complexo, discursiva, oral e perfil somente leitura.
- Rubrica: precisão jurídica, função das fontes, progressão pedagógica e adequação à frente, cada eixo de 0 a 2.
- Bloqueio: zero em precisão jurídica ou violação de consentimento.

## Registro de execução

A avaliação estrutural é automatizada pela suíte. As execuções conversacionais e decisões humanas devem registrar data, modelo, repetição, notas por eixo, evidência curta, divergência e decisão final. Respostas integrais que contenham material pessoal não são versionadas.

## Execução e decisão humana

- Data: 2026-09-05.
- Modelo: `gpt-5.6-sol`, esforço `low`, sessões efêmeras e filesystem somente leitura.
- Amostra final: 18 saídas, três sessões limpas para cada um dos seis casos centrais.
- Artefatos integrais: mantidos apenas em `.test-tmp`, fora da distribuição; os prompts e as evidências abaixo são sintéticos.

| Caso | Repetições | Precisão jurídica | Função das fontes | Progressão pedagógica | Adequação à frente | Decisão e evidência |
|---|---:|---:|---:|---:|---:|---|
| `dogmatica-fontes-pulverizadas` | 3 | 2 | 2 | 2 | 2 | **Aprovar.** Art. 49-A e art. 50 estruturam autonomia, abuso e imputação; o Tema 1.210 delimita insolvência e encerramento irregular; o bloco termina com problema de transferência e base oficial correspondente. |
| `dogmatica-continuidade-sem-reinicio` | 3 | 2 | 2 | 2 | 2 | **Aprovar.** As três respostas partem diretamente dos pressupostos materiais, sem repetir ambientação, e preparam o exame probatório. |
| `caso-solucoes-concorrentes` | 3 | 2 | 2 | 2 | 2 | **Aprovar.** Os casos distinguem dívida própria por ilícito do administrador e extensão de dívida social; autoria do ilícito ou uso abusivo da autonomia altera o enquadramento. |
| `discursiva-reconstrucao-do-erro` | 3 | 2 | 2 | 2 | 2 | **Aprovar.** A correção localiza a falta de subsunção, reconstrói somente a ponte regra-fato-consequência e separa o indispensável do desenvolvimento de excelência. |
| `oral-repergunta-adaptativa` | 3 | 2 | 2 | 2 | 2 | **Aprovar.** Cada sessão formula uma única pergunta oral juridicamente delimitada e aguarda resposta, sem antecipar bateria, correção ou inferência acústica. A ausência de fontes nesta abertura é proporcional à tarefa. |
| `perfil-leitura-sem-escrita` | 3 | 2 | 2 | 2 | 2 | **Aprovar.** A preferência histórica permanece auxiliar, o pedido atual por objetiva prevalece e nenhuma sessão afirma gravação ou atualização. A ausência de fontes jurídicas é adequada à operação de perfil. |

### Calibração e refinamentos

A primeira amostra revelou duas variações sem bloqueio jurídico: um link oficial rotulado como Tema 1.210 conduzia a uma pesquisa genérica, e as correções discursivas nem sempre nomeavam a diferença entre conteúdo indispensável e excelência. Os contratos foram refinados para proibir a rotulagem de busca genérica como precedente determinado e para exigir essa distinção na própria correção. As seis execuções afetadas foram descartadas e repetidas em sessões limpas; a tabela registra somente as rodadas posteriores.

A conferência jurídica humana validou no portal oficial do STJ a tese e os recursos representativos do Tema 1.210, bem como os limites subjetivos da teoria menor utilizados nos casos. Não houve precedente inventado, nota zero, divergência pendente ou violação de consentimento.

Os critérios semânticos continuam tecnicamente representados como `revisao_humana_pendente` pelo avaliador automático: a aprovação acima é decisão humana documentada e não resultado de detecção por palavras-chave.
