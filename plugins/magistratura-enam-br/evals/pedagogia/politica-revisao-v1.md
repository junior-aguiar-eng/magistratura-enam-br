# Comparação da política de revisão v1

Execução sintética em 2026-09-04, com intervalo fixo de 21 dias e modo sombra ativo.

| Caso | Intervalo fixo | Intervalo sugerido | Data fixa | Data sugerida | Data efetiva | Remediação |
|---|---:|---:|---|---|---|---|
| Incorreto | 21 | 1 | 2026-09-25 | 2026-09-05 | 2026-09-25 | aberta |
| Parcial | 21 | 3 | 2026-09-25 | 2026-09-07 | 2026-09-25 | aberta |
| Correto com baixa confiança | 21 | 21 | 2026-09-25 | 2026-09-25 | 2026-09-25 | não |
| Reincidência | 21 | 1 | 2026-09-25 | 2026-09-05 | 2026-09-25 | mantida |
| Correto com transferência | 21 | 31 | 2026-09-25 | 2026-10-05 | 2026-09-25 | não |

Na janela de sete dias, a política fixa efetiva agenda zero revisões; a sugestão sombra sinaliza três, equivalentes a 30 minutos pelos parâmetros atuais. A quantidade de remediações permanece três em ambas as políticas: o modo sombra não fecha nem cria remediação por conveniência de carga.

O intervalo só foi ampliado com acerto, alta confiança, fundamentação e transferência observáveis. Como ainda não há evidência longitudinal de retenção, a política permanece em modo sombra e nenhuma `proxima_revisao` é substituída.

