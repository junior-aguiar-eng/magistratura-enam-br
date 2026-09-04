---
name: acompanhar-percurso-magistratura
description: Use quando o candidato pedir para organizar, retomar ou decidir o próximo passo entre estudo jurídico, curadoria, comparação de materiais e planejamento jurisprudencial. Não use quando a tarefa já pertencer claramente a uma dessas skills.
---

# Acompanhamento do percurso para Magistratura

## Objetivo

Transforme o objetivo expresso do candidato em uma recomendação de encaminhamento entre as skills do plugin. Esta skill coordena fronteiras; não produza conteúdo jurídico substantivo, não execute a skill indicada e não escreva automaticamente em perfil, log, planilha ou arquivo.

## Fluxo

1. Identifique o objetivo declarado e os insumos efetivamente fornecidos. Perfil, eventos, remediações e referências de conteúdo são opcionais; não os presuma.
2. Se a tarefa já apontar inequivocamente para uma skill, recomende-a diretamente. Em objetivo composto ou ambíguo, leia `references/roteamento.md`.
3. Entregue somente este contrato compacto:

```yaml
skill_recomendada: nome-da-skill
motivo: relação objetiva entre o pedido e a competência da skill
dados_necessarios: dados ausentes ou []
acao_dependente_confirmacao: ação externa ou persistente, ou null
```

`skill_recomendada` admite exclusivamente `acompanhar-percurso-magistratura`, `comparar-materiais-enam`, `curar-informativos-stf-stj`, `estudar-direito-magistratura` ou `planejar-jurisprudencia`. Nunca invente nome de skill ou transforme modalidade em skill. Questões objetivas, discursivas e orais são modalidades de `estudar-direito-magistratura`.

4. Execute ação persistente, alteração de arquivo ou passagem para outra etapa somente depois da confirmação correspondente. Uma recomendação não equivale a autorização.

## Limites

Não alegue histórico, progresso, domínio, erro recorrente ou preferência quando perfil e log não forem fornecidos. Ausência de dados significa ausência de evidência, não desempenho insuficiente.

Encaminhe agenda exclusivamente a `planejar-jurisprudencia` e atualização documental exclusivamente a `comparar-materiais-enam`. Não substitua a curadoria de fontes nem a explicação jurídica. Quando faltar apenas o insumo indispensável, solicite-o no campo `dados_necessarios`, sem entrevista ampla.
