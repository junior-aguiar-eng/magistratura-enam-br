# Baseline de roteamento, transições e fontes — 0.4.1

## Método

Execução em 4 de setembro de 2026 com a release instalada `0.4.1`, modelo `gpt-5.6-sol` e 18 cenários repetidos três vezes em sessões efêmeras independentes. Cenários com estado anterior receberam uma transcrição sintética explícita no mesmo prompt; portanto, medem decisão diante do estado informado, não persistência entre sessões. As 54 respostas integrais permaneceram apenas em armazenamento temporário local. Este documento versiona somente métricas, sínteses e evidências anônimas.

## Métricas agregadas

- Execuções concluídas: 54/54; indisponibilidades: 0.
- Extensão média: 183,2 palavras; mínimo: 6; máximo: 3.290.
- Acerto da família de skill: 54/54.
- Acerto de modalidade quando expressa: 12/12.
- Respeito explícito às três políticas de fonte: 27/27 nas situações diretamente avaliáveis.
- Preservação inequívoca de atividade pendente: 5/9; em quatro respostas houve encerramento ou interrupção sem estado recuperável claro.
- Ambientação inicial satisfatória: 0/3; as três respostas começaram por coleta de dados, sem apresentação breve do ambiente ou do fluxo.
- Efeito "portfólio de notícias": 1/54, concentrado em uma execução de curadoria com 3.290 palavras e nove links.
- Perguntas no gatilho genérico: entre uma e três solicitações; variância de formato entre lista e pergunta corrida.

## Resultado por cenário

| Cenário | Rota | Transição | Fontes | Síntese das três repetições |
|---|---|---|---|---|
| Clique genérico | 3/3 | 0/3 | n/a | Pediu tema/modalidade; não apresentou o ambiente e variou entre uma pergunta e lista de três dados. |
| Tema direto | 3/3 | 3/3 | 3/3 | Iniciou estudo substantivo sem menu; respostas longas e com exercício final não solicitado. |
| Questão direta | 3/3 | 3/3 | 3/3 | Gerou cinco alternativas sem gabarito, preservando a modalidade. |
| Curadoria direta | 3/3 | 2/3 | 2/3 | Duas execuções bloquearam por falta do anexo; uma pesquisou silenciosamente, produziu curadoria extensa e exibiu nove links. |
| Comparação direta | 3/3 | 3/3 | 3/3 | Solicitou as duas versões ausentes sem alegar acesso. |
| Planejamento direto | 3/3 | 3/3 | n/a | Respeitou 40 minutos, mas variou entre cronograma livre e contrato canônico da esteira. |
| Tema com pendência | 3/3 | 1/3 | n/a | Uma suspensão recuperável; duas respostas declararam encerramento sem confirmação inequívoca. |
| Tema sem pendência | 3/3 | 3/3 | 3/3 | Mudou de tema; uma repetição perguntou recorte e duas iniciaram aula diretamente. |
| Modalidade com pendência | 3/3 | 3/3 | n/a | Respeitou o abandono expresso e pediu apenas o tema ausente. |
| Modalidade sem pendência | 3/3 | 3/3 | 3/3 | Iniciou questão objetiva sem entrevista adicional. |
| Skill com pendência | 3/3 | 1/3 | 3/3 | Reconheceu interrupção, mas só uma repetição preservou explicitamente a pergunta sem correção. |
| Skill sem pendência | 3/3 | 3/3 | 3/3 | Mudou para comparação e pediu os arquivos necessários. |
| Acervo exclusivo | 3/3 | 3/3 | 3/3 | Bloqueou corretamente sem o trecho e não pesquisou. |
| Acervo com atualização oficial | 3/3 | 3/3 | 3/3 | Pediu material e objeto antes de consultar fontes externas. |
| Pesquisa completa | 3/3 | 3/3 | 3/3 | Pediu somente o tema ausente e não iniciou busca arbitrária. |
| Menção incidental | 3/3 | 3/3 | 3/3 | Manteve o estudo de prescrição e decadência, sem acionar comparação. |
| Secundária contra oficial | 3/3 | 3/3 | 3/3 | Recusou substituir o acórdão pelo blog e marcou superação como não confirmada. |
| Material ausente | 3/3 | 3/3 | 3/3 | Declarou ausência de acesso e solicitou o arquivo ou trecho. |

## Rubrica humana

A precisão jurídica e a hierarquia de fontes foram satisfatórias nas amostras avaliáveis. A naturalidade foi parcial: respostas diretas funcionam, mas o gatilho genérico se comporta como coleta de requisitos e as transições não compartilham fórmula estável. A clareza da mudança foi boa quando o candidato declarou abandono; foi insuficiente quando havia apenas intenção de trocar de rota. A resposta anômala de curadoria reprova proporcionalidade, fidelidade ao insumo e ausência de efeito "portfólio de notícias".

## Defeitos congelados para comparação

1. O gatilho genérico não inicia questão arbitrária nesta rodada, mas também não oferece apresentação inicial nem orientação breve; começa por perguntas de configuração.
2. Não existe contrato uniforme para distinguir suspender, abandonar, encerrar e retomar atividade pendente.
3. A indisponibilidade de anexo pode disparar comportamentos opostos: bloqueio correto ou pesquisa externa silenciosa.
4. A extensão varia em mais de duas ordens de grandeza e uma curadoria excedeu a necessidade pedagógica.
5. O planejador reconhece capacidade, mas alterna entre formatos operacionais incompatíveis.

## Gate

O baseline separa comportamento do modelo de validação estrutural: os testes do catálogo apenas validam schema e completude; as conclusões acima decorrem das 54 execuções e da rubrica humana posterior. Nenhuma instrução de produção foi alterada nesta fase.
