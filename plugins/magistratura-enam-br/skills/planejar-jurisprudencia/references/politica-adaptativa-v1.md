# Política adaptativa de revisão v1

A política é opt-in e opera inicialmente em modo sombra. `proxima_revisao` continua obedecendo ao ciclo fixo; `intervalo_sugerido` e `motivo_sugestao` apenas registram a alternativa calculada.

| Evidência observada | Sugestão |
|---|---:|
| Incorreto | 1 dia e remediação aberta |
| Parcial | menor valor entre 3 dias e o intervalo fixo |
| Correto sem confiança ou justificativa | intervalo fixo |
| Correto com baixa confiança | intervalo fixo e contraste breve |
| Correto com alta confiança, fundamento e sem transferência | piso de 1,25 vezes o intervalo fixo |
| Correto com alta confiança, fundamento e transferência | piso de 1,5 vezes o intervalo fixo, limitado a 90 dias |
| Reincidência do mesmo erro | 1 dia e remediação mantida |

Resultado, confiança e evidências devem estar expressamente registrados. Ausência desses dados não autoriza recomendação. O cálculo não inclui atividade alheia à jurisprudência nem cria cronograma geral.

O grau de assistência altera a leitura do resultado: acerto com condução completa não demonstra autonomia. Transferência independente para hipótese nova e retenção em revisão posterior sustentam ampliação mais forte do intervalo sugerido. A política não cristaliza fraqueza histórica; evidência posterior, mais autônoma e pertinente ao mesmo conteúdo deve atualizar a recomendação. Enquanto o modo sombra vigorar, esses fatores explicam `motivo_sugestao` e não alteram o ciclo fixo.
