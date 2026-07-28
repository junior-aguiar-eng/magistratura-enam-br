---
name: planejar-jurisprudencia
description: Organize a leitura e a revisão espaçada de julgados brasileiros já selecionados para Magistratura e ENAM. Use quando o usuário pedir cronograma, priorização de revisões, reorganização após atrasos, diagnóstico de carga, criação ou atualização de uma esteira de jurisprudência. Não use para escolher julgados de um informativo, explicar mérito jurídico ou comparar materiais do ENAM.
---

# Planejamento de jurisprudência

## Objetivo

Organize julgados já curados em uma rotina sustentável de leitura inicial e revisão espaçada, sempre subordinada à capacidade real do candidato e ao prazo até a prova. Esta skill administra o tempo de estudo; não seleciona precedentes e não altera sua análise jurídica.

Antes de interpretar o pedido ou escolher o modo de atuação, leia e cumpra integralmente `../../AGENTS.md`. Suas diretrizes prevalecem sobre preferências genéricas de formato, concisão ou simplificação.

## Fluxo

1. Receba apenas julgados já selecionados pela curadoria ou pelo próprio usuário.
2. Priorize revisões vencidas, preserve folga semanal e comunique com clareza quando o volume não couber no prazo.
3. Use `scripts/atualizar_esteira.py` para criar, alimentar, atualizar ou consultar a planilha de esteira.
4. Quando a fonte for a planilha de precedentes da skill de curadoria, use `scripts/preparar_itens_esteira.py` para gerar o CSV de entrada. Preserve estado jurisprudencial, grau de confiança e fontes essenciais como metadados de consulta; não os use para inferir prioridade alta ou vínculo com erro.
5. Consulte `references/fluxo-da-esteira.md` antes de explicar regras de prioridade, ciclos, regimes ou capacidade.

## Limites

Prioridade alta exige precedente qualificado ou erro documentado do candidato. A esteira deve expor a insuficiência de tempo, não produzir cronograma artificialmente otimista. Em regime de consolidação, não incorpore material novo.

Use `../../references/diretrizes-estudo-juridico-brasileiro.md` antes de classificar prioridades.
