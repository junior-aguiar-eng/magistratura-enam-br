# Avaliações pedagógicas

Este diretório mede o comportamento das skills com casos sintéticos e versionados. Os testes automatizados validam estrutura e riscos observáveis; a rubrica humana decide precisão jurídica, qualidade pedagógica e defensabilidade.

## Piloto em uso real da candidata 0.7.3

Use o plugin em atividades normais, sem roteiro de 24 execuções. Quando houver resposta suspeita, registre apenas cliente, versão, data, pergunta e trecho necessário da saída, após retirar dados pessoais e material protegido. Confira o ponto contestado na fonte apropriada e converta defeitos confirmados em casos sintéticos de regressão. Ausência de relatos não comprova qualidade; este piloto não altera o estado `pending` do benchmark formal.

## Execução do baseline

1. Use uma sessão nova para cada execução, sem histórico de outro caso.
2. Execute cada caso três vezes com a versão indicada em `baseline`.
3. Capture texto, duração e tokens quando disponíveis.
4. Rode `scripts/avaliar_saida_pedagogica.py` para asserções automáticas.
5. Aplique `rubrica.md` somente depois da saída.
6. Registre apenas resultados agregados e evidências sintéticas no relatório versionado.

Não use material pessoal, prova protegida ou resposta real do candidato como fixture versionada.

O piloto jurídico em `benchmark-juridico/` acrescenta fonte oficial, data de corte, proposições verificáveis e estado de revisão humana aos casos sintéticos. Fonte localizada não torna a saída correta: a análise da aplicação da norma ao caso, da unicidade do gabarito e da proporcionalidade permanece humana. Casos com fixture `pending` não são referência jurídica aprovada.

## Profissionalização 0.6.0

Testes literais protegem somente contratos textuais e proibições objetivamente enumeráveis. Profundidade dogmática, função das fontes, plausibilidade de soluções e qualidade de correção exigem rubrica semântica e revisão jurídica humana. Nenhum caso versionado contém material ou desempenho pessoal de candidato.

## Auditor quantitativo de blocos — task 6

`scripts/auditar_questoes.py` lê arquivos UTF-8 (com ou sem BOM), imprime relatório JSON e não altera questões, gabarito, perfil ou biblioteca. Não cria arquivo de saída, não reordena alternativas e não registra tentativas. O [schema do relatório](../../modelos/pedagogia/question-block-audit.schema.json) separa `errors`, `warnings`, `not_checked` e `metrics`.

```powershell
uv run python scripts/auditar_questoes.py --questoes bloco.md --formato markdown
uv run python scripts/auditar_questoes.py --questoes sessoes.json --formato json --gabarito chaves.json
```

Markdown de várias questões usa cabeçalhos `## Questão ID — Tema`; uma questão sem cabeçalho recebe ID `1`. O enunciado vem antes das opções A)–E) ou A.–E.; bullets e ênfase nos marcadores são aceitos. Linhas com quatro ou mais espaços são continuação; assertivas I/II/III e colunas permanecem no enunciado. Cabeçalho sem questão, texto anterior ao primeiro cabeçalho e seção posterior às alternativas são recusados, inclusive delimitadores isolados de correção/justificativa em negrito ou com dois-pontos. Marcador explícito de solução no título é recusado antes de descartar o cabeçalho. Bloco cercado integralmente por `markdown`/`md` é aceito; cercas internas ou outro tipo de bloco não são interpretados. IDs repetidos e rótulos de alternativa repetidos continuam na entrada para detecção, sem colapsar em dicionário.

JSON aceita array de projeções de sessão existentes com `session_id`, `prompt` e `alternatives: [{"id":"A","text":"..."}, ...]`. Campos auxiliares da sessão não são reproduzidos. O rótulo opcional `format` permite classificação explícita de autoria, sem acrescentá-lo à sessão MCP; quando ausente, o parser identifica associação pelas colunas, V/F pelo comando/sequências, numerado pelas assertivas e direto como padrão. A classificação automática não substitui a classificação humana do corpus. Formato explícito fora de `direto | numerado | vf | associacao` é erro.

Limitação conhecida: listas com numeração arábica, sem a palavra “afirmativas”, podem ser classificadas como diretas. A distribuição automática exige conferência de autoria; JSON com `format: "numerado"` permite classificação explícita. Esse achado menor ficou registrado para evolução posterior.

`--gabarito` lê objeto JSON como `{"1":"C","2":"A"}`. Em projeção privada/corrigida, `correct_option` pode fornecer chave interna; a dataclass guarda esse campo opcional fora do repr, sem mudar o MCP. Chaves externas e internas são confrontadas; letras fora de A–E, IDs órfãos ou contradições são erros. Chaves JSON repetidas são recusadas antes de decodificar o objeto, inclusive no gabarito. Ausência de chave interna e externa deixa o item fora das métricas dependentes de gabarito.

| Estado | Significado |
| --- | --- |
| `reprovado_estruturalmente` | Entrada vazia, ilegível, não interpretável ou com erros de estrutura/chave/vazamento explícito. |
| `checagem_parcial` | Sem erros encontrados, mas há item sem estrutura/chave elegível; não recebe aprovação global. |
| `aprovado_estruturalmente` | Estrutura verificada e chave compatível para todos os itens; mérito e fontes continuam não verificados. |

A CLI retorna 2 diante de erros; 0 indica execução sem erro estrutural, inclusive quando parcial. Consulte `status` e `not_checked`, não apenas o exit code. Expressões como “assinale a alternativa correta” não são vazamento; marcadores explícitos como “Gabarito: C”, “Resposta correta: letra B” e marca de correta são detectados. Esse detector não encontra toda pista indireta, justificativa implícita ou defeito semântico: não certifica segurança pré-tentativa.

Relatórios com chave são **privados de autoria/avaliação**. Não contêm enunciados, texto das alternativas ou gabaritos individuais, mas distribuições de letras podem revelar uma chave em amostra pequena. Nunca anexe esse relatório, nem o arquivo de gabarito, à apresentação pré-tentativa do candidato. Nenhum exemplo de desempenho pessoal deve ser versionado por padrão.

### Métricas e limites

- `answer_coverage`: itens elegíveis com chave válida sobre total de questões; a distribuição de letras e os padrões usam somente esses itens, excluindo duplicatas, estrutura inválida e chaves contraditórias.
- `format_distribution`: formatos reconhecidos sobre itens de formato suportado, independentemente de outros erros; não representa distribuição de questões juridicamente válidas.
- `alternative_lengths`: caracteres e palavras de cada texto interpretável, inclusive sem chave ou em questão estruturalmente inválida, sobre todas as entradas de alternativas. Duplicatas permanecem nas medidas.
- `absolute_frequency`: alternativas com termo absoluto sobre alternativas com texto; `counts` mede ocorrências de sempre, nunca, apenas, somente, exclusivamente, necessariamente, em qualquer caso e em nenhuma hipótese. Termo absoluto não prova erro jurídico.
- `length_pattern`: chave como única alternativa mais longa; empate não conta. `absolute_pattern`: correta sem termo absoluto enquanto todos os quatro distratores os contêm. Ambos mostram numerador, denominador e fração; fração sem amostra é `null`.

Avisos agregados de extensão/absolutos surgem somente com **ao menos oito itens elegíveis e frequência estritamente superior a 75%**. O limiar é heurística editorial do projeto, não estatística oficial da FGV/ENAM. Três ou mais letras iguais consecutivas geram aviso; item sem chave válida interrompe a sequência. Esses padrões não invalidam questão nem alteram sua ordem.

`--perfil` aceita objeto JSON por leitura. Dict arbitrário permanece `profile_not_validated`. A task 7 acrescenta [registro/perfil de corpus](calibracao-enam/README.md) recomputável: registro declarado oficial com itens elegíveis pode alimentar comparação descritiva de formatos, sem quota, certificação de fidelidade ao ENAM ou mudança da chave. Perfil reconhecido inconsistente é erro; fixture sintética não se torna referência empírica. Fundamentação, fontes, plausibilidade dos distratores e unicidade jurídica sempre exigem revisão humana posterior.

## Comparação da task 8

As [42 capturas da task 8](task8/README.md) usam duas variantes congeladas,
três sessões por caso, modelo/cliente/fontes comuns e rubrica posterior.
Cada captura conserva caso e saída com hashes, sem aprovação humana.
O caso de simulado sem corpus é controle negativo; não comprova calibração
empírica. MCP stdio real, anexo no ChatGPT e testes do widget têm escopos
separados; ausência de conexão candidata deixa card/fullscreen pendentes.
