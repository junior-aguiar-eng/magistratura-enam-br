# Roteamento do percurso

Use esta referência somente quando o objetivo combinar etapas ou não indicar com segurança uma skill. A recomendação escolhe uma competência; não executa a tarefa nem cria estado.

## Roteamento positivo

| Objetivo observável | Skill recomendada | Dados mínimos |
|---|---|---|
| Decidir a próxima etapa entre duas ou mais competências do plugin | `acompanhar-percurso-magistratura` | objetivo expresso e insumos disponíveis |
| Comparar versões publicadas, classificar delta ou orientar atualização documental | `comparar-materiais-enam` | versões e recorte comparável |
| Selecionar e comentar informativos ou precedentes oficiais | `curar-informativos-stf-stj` | fonte oficial identificável |
| Explicar tema, criar questão, corrigir resposta ou remediar erro jurídico | `estudar-direito-magistratura` | tema ou atividade e tentativa, quando houver |
| Organizar agenda, capacidade, revisões ou remediações da esteira | `planejar-jurisprudencia` | disponibilidade e estado da esteira pertinente |

Agenda pertence exclusivamente a `planejar-jurisprudencia`. Atualização documental pertence exclusivamente a `comparar-materiais-enam`. Se uma mudança documental envolver julgado já presente na esteira, recomende primeiro a comparação e indique o planejamento como etapa posterior dependente de confirmação.

## Near-miss

| Pedido limítrofe | Não encaminhar para | Encaminhamento correto |
|---|---|---|
| Pedido jurídico substantivo com tema já delimitado | `acompanhar-percurso-magistratura` | `estudar-direito-magistratura` |
| Explicação geral sobre mudança legislativa sem duas versões documentais | `comparar-materiais-enam` | `estudar-direito-magistratura` |
| Notícia, comentário doutrinário ou decisão sem fonte oficial verificável | `curar-informativos-stf-stj` | solicitar fonte; não simular curadoria |
| Pedido apenas de calendário ou fila de revisão | `estudar-direito-magistratura` | `planejar-jurisprudencia` |
| Pedido de comparar documentos, sem agenda ou capacidade | `planejar-jurisprudencia` | `comparar-materiais-enam` |

Em ambiguidade residual, recomende `acompanhar-percurso-magistratura` e liste um único dado discriminante. Não invente perfil, histórico, remediação ou referência de conteúdo para decidir.

O valor de `skill_recomendada` deve ser literalmente um dos cinco nomes canônicos desta referência. Nunca invente nome de skill; questões objetivas pertencem a `estudar-direito-magistratura`.
