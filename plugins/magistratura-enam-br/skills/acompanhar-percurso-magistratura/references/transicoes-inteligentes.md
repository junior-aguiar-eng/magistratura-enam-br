# Transições inteligentes

Este protocolo mantém continuidade sem transformar o estudo em formulário. A transição é decidida internamente pelo contrato `transition`; ao candidato, comunique apenas o necessário em linguagem natural.

## Classes canônicas

| Classe | Quando usar | Tratamento |
|---|---|---|
| `CONTINUAR` | A nova mensagem responde, aprofunda ou prossegue na rota ativa | Continue diretamente, sem anunciar transição. |
| `MUDAR_TEMA` | O candidato escolhe outro tema dentro da mesma skill | Preserve modalidade e política de fontes quando aplicáveis; anuncie a troca em uma frase e prossiga na mesma resposta. |
| `MUDAR_MODALIDADE` | O tema permanece e muda a forma de estudo | Preserve o tema; anuncie a nova modalidade em uma frase e prossiga na mesma resposta. |
| `MUDAR_SKILL` | O objetivo passa a pertencer a outra skill | Anuncie o novo módulo em uma frase e devolva a autoridade ao orquestrador; não execute silenciosamente a outra skill. |
| `SUSPENDER` | A atividade atual deve ficar recuperável | Preserve a pendência no contexto da conversa ou em checkpoint fornecido explicitamente. |
| `RETOMAR` | Há rota suspensa nesta conversa ou checkpoint fornecido | Restaure tema, modalidade, pendência e política de fontes compatíveis; não repita ambientação. |
| `ENCERRAR` | O candidato conclui ou abandona inequivocamente a atividade | Encerre sem registrar tentativa, erro ou abandono pedagógico não observado. |

## Regra de decisão

Mudança inequívoca é comunicada em uma frase e prossegue na mesma resposta. Não peça confirmação para troca reversível, continuidade, suspensão ou retomada segura.

Faça uma única pergunta de decisão somente quando:

- a nova rota descartaria irreversivelmente uma atividade pendente sem comando claro de abandono; ou
- houver escrita, exclusão, persistência, alteração de arquivo ou outra ação externa ainda não autorizada.

Se o candidato disser “abandone”, “encerre”, “substitua” ou equivalente inequívoco, cumpra sem reconfirmar. Se disser apenas “agora quero outro tema”, suspenda a pendência de modo recuperável e prossiga; não trate a mudança como erro, tentativa ou abandono.

## Pendências materiais

- **Questão aguardando resposta:** preserve enunciado, alternativas e ausência de tentativa.
- **Discursiva em elaboração:** preserve enunciado e estado de elaboração; texto não enviado não é resposta avaliada.
- **Curadoria incompleta:** preserve informativo, recorte e etapa de leitura; não declare boletim concluído.
- **Comparação sem segundo documento:** preserve primeira versão e escopo; não conclua delta nem exclusão.
- **Remediação aberta:** preserve `remediation_id` e `content_ref`; mudança de assunto não encerra nem altera a esteira.

Suspender, encerrar e substituir são atos distintos. Suspensão mantém retorno possível; encerramento termina a atividade por decisão inequívoca; substituição descarta o objeto anterior e exige decisão clara quando houver perda material.

## Limites de memória

Pendência existe apenas na conversa atual. Entre sessões, só alegue retomada quando o candidato fornecer checkpoint, perfil ou evento local válido. Não afirme lembrar estado anterior, não persista automaticamente e não transforme descrição livre em evento de aprendizagem.

Quando rota, tema e política de fontes já estiverem claros, não repita apresentação do plugin, menu, calibração ou perguntas de abertura.
