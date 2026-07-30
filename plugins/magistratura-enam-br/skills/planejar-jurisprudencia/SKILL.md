---
name: planejar-jurisprudencia
description: Organize a leitura e a revisão espaçada de julgados brasileiros já selecionados para Magistratura e ENAM. Use quando o usuário pedir cronograma, priorização de revisões, reorganização após atrasos, diagnóstico de carga, criação ou atualização de uma esteira de jurisprudência, ou uma resposta operacional como “o que faço hoje?”. Não use para escolher julgados de um informativo, explicar mérito jurídico ou comparar materiais do ENAM.
---

# Planejamento de jurisprudência

## Objetivo

Organize julgados já curados em uma rotina sustentável de leitura inicial e revisão espaçada, sempre subordinada à capacidade real do candidato e ao prazo até a prova. Esta skill administra o tempo de estudo; não seleciona precedentes e não altera sua análise jurídica.

Na abertura de nova sessão de planejamento, leia e cumpra integralmente `../../AGENTS.md`. Suas diretrizes prevalecem sobre preferências genéricas de formato, concisão ou simplificação. Em continuidade da mesma esteira e do mesmo objetivo de planejamento, reaproveite essa leitura e releia apenas se houver nova fonte, mudança de regime ou novo pedido que altere materialmente o planejamento.

Quando uma nova sessão trouxer e-books, verticalizados, análises estratégicas ou cronogramas de curso, leia `../../references/protocolo-uso-do-acervo.md` antes de incorporá-los ao contexto. Preserve a classificação para a continuidade da mesma esteira e reavalie-a somente com novo material.

## Fluxo

1. Receba apenas julgados já selecionados pela curadoria ou pelo próprio usuário.
2. Priorize revisões vencidas, preserve folga semanal e comunique com clareza quando o volume não couber no prazo.
3. Use `scripts/atualizar_esteira.py` para criar, alimentar, atualizar ou consultar a planilha de esteira.
4. Quando a fonte for a planilha de precedentes da skill de curadoria, use `scripts/preparar_itens_esteira.py` para gerar o CSV de entrada. Preserve estado jurisprudencial, grau de confiança e fontes essenciais como metadados de consulta; não os use para inferir prioridade alta ou vínculo com erro.
5. Consulte `references/fluxo-da-esteira.md` antes da primeira explicação de regras de prioridade, ciclos, regimes ou capacidade para aquela esteira; reaproveite-o enquanto essas regras e o objetivo permanecerem os mesmos.
6. Para “o que faço hoje?”, atrasos ou carga imediata, use o modo operacional descrito em `references/fluxo-da-esteira.md`: informe carga mínima viável, fila em ordem de execução, itens adiados e custo concreto do adiamento. Não transforme essa resposta em calendário amplo.

## Limites

Prioridade alta exige precedente qualificado ou erro documentado do candidato. A esteira deve expor a insuficiência de tempo, não produzir cronograma artificialmente otimista. Em regime de consolidação, não incorpore material novo.

Verticalizados e análises estratégicas podem apenas ajudar o candidato a descrever julgados que ele já selecionou; não criam item, prioridade, prazo ou ciclo de revisão. Cronogramas e planos de remessa de curso não são entrada da esteira e não autorizam inferir disponibilidade de material. Somente escolha expressa do candidato e os critérios canônicos desta skill definem o planejamento.

Não consulte `../../references/diretrizes-estudo-juridico-brasileiro.md` para classificar prioridade, pois esta skill organiza tempo de estudo e não redefine o conteúdo jurídico dos julgados. Se o pedido depender de atualização do mérito, encaminhe para curadoria ou estudo antes de alterar a esteira.
