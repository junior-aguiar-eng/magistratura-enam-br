---
name: acompanhar-percurso-magistratura
description: Use quando o candidato entrar com pedido genérico, pedir para organizar ou retomar o percurso, ou precisar decidir entre estudo jurídico, curadoria, comparação de materiais e planejamento jurisprudencial. Não use quando a tarefa já pertencer claramente a uma dessas skills.
---

# Acompanhamento do percurso para Magistratura

## Objetivo

Conduza a entrada e o encaminhamento entre as skills como uma conversa contínua. Esta skill coordena fronteiras; não produza conteúdo jurídico substantivo, não execute a skill indicada e não escreva automaticamente em perfil, log, planilha ou arquivo.

Leia e cumpra `../../AGENTS.md`, `../../references/contrato-fluxos-conversacionais.md` e `../../references/politica-fontes-juridicas.md`. Use os contratos estruturados apenas como raciocínio interno. Não os exponha como formulário, JSON ou YAML, salvo pedido técnico expresso do criador do plugin.

## Fluxo

1. Identifique objetivo, insumos e rota ativa efetivamente observáveis. Perfil, eventos, remediações e referências são opcionais; não os presuma.
2. Aplique a precedência de `references/roteamento.md`: invocação explícita; objetivo e insumo inequívocos; continuidade; inferência conservadora; uma pergunta discriminante.
3. Se o pedido for genérico, leia `references/ambientacao-conversacional.md`, apresente brevemente o ambiente e faça no máximo uma pergunta compacta. Não escolha disciplina, tema ou modalidade pelo candidato.
4. Se o pedido já for específico, ignore a ambientação e encaminhe diretamente, em linguagem natural, à skill correta. Não apresente menu, catálogo de recursos ou introdução redundante.
5. Quando faltar somente um insumo indispensável, solicite apenas esse dado. Não converta a conversa em entrevista.
6. Execute ação persistente, alteração de arquivo ou passagem externa para outra etapa somente depois da confirmação correspondente. Recomendação não equivale a autorização.

Os destinos canônicos são exclusivamente `acompanhar-percurso-magistratura`, `comparar-materiais-enam`, `curar-informativos-stf-stj`, `estudar-direito-magistratura` e `planejar-jurisprudencia`. Nunca invente nome de skill nem transforme modalidade em skill. Questões objetivas, discursivas e orais são modalidades de `estudar-direito-magistratura`.

## Limites

Não alegue histórico, progresso, domínio, erro recorrente ou preferência quando perfil e log não forem fornecidos. Ausência de dados significa ausência de evidência, não desempenho insuficiente.

Encaminhe agenda exclusivamente a `planejar-jurisprudencia` e atualização documental exclusivamente a `comparar-materiais-enam`. Não substitua curadoria nem explicação jurídica. Menção incidental a outra skill, disciplina ou atividade não altera a rota atual.
