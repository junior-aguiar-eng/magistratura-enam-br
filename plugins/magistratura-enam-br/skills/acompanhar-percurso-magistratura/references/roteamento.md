# Roteamento do percurso

Use esta referência somente quando o objetivo combinar etapas ou não indicar com segurança uma skill. A recomendação escolhe uma competência; não executa a tarefa nem cria estado.

## Precedência obrigatória

1. **Invocação explícita de skill ou modalidade:** respeite o destino declarado, salvo impossibilidade material ou conflito com segurança, privacidade ou fonte.
2. **Objetivo e insumo inequívocos:** tema substantivo segue para estudo; informativo oficial para curadoria; duas versões para comparação; capacidade ou fila para planejamento.
3. **Continuidade da rota ativa:** mantenha tema, modalidade e skill quando a nova mensagem for resposta, aprofundamento ou continuação.
4. **Inferência conservadora:** escolha somente quando uma rota for claramente mais específica e não exigir inventar objetivo, material ou histórico.
5. **Uma pergunta discriminante:** se nenhuma rota for segura, faça uma única pergunta compacta sobre o dado que efetivamente separa os destinos.

O resultado é comunicado em linguagem natural. `session-route` e `transition` são estados internos e nunca devem aparecer como YAML ou formulário por padrão.

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
| Pedido para estudar o mérito de um julgado já identificado | `curar-informativos-stf-stj` | `estudar-direito-magistratura` |
| Pedido para selecionar julgados de um informativo oficial | `estudar-direito-magistratura` | `curar-informativos-stf-stj` |
| Pedido para distribuir revisões de julgados já selecionados | `curar-informativos-stf-stj` | `planejar-jurisprudencia` |

Em ambiguidade residual, recomende `acompanhar-percurso-magistratura` e liste um único dado discriminante. Não invente perfil, histórico, remediação ou referência de conteúdo para decidir.

O roteamento não presume banca, disciplina ou percurso. Perfil autorizado é evidência auxiliar e nunca supera o pedido atual. Quando o pedido já contiver verbo de ação, objeto e insumo suficientes, encaminhe diretamente sem entrevista de calibração.

Citação incidental a outro ramo, material ou atividade não muda a rota. Considere mudança apenas quando houver verbo de ação ou decisão atual incompatível com a continuidade.

O destino interno deve ser literalmente um dos cinco nomes canônicos desta referência. Nunca invente nome de skill; questões objetivas pertencem a `estudar-direito-magistratura`.
