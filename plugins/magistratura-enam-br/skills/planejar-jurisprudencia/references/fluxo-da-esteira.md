# Fluxo da esteira de jurisprudência

## Papel no método de estudo

A esteira recebe julgados já curados e os distribui no tempo. Ela não reabre a seleção editorial, não interpreta a ratio decidendi e não substitui o estudo analítico. Sua função é responder, com base no estado efetivamente registrado: o que revisar, o que ler em seguida e se o volume ainda cabe até a prova.

Há duas filas: **Entrada**, para a primeira leitura, e **Revisão**, para julgados que já passaram pela leitura inicial. Revisões vencidas ocupam a capacidade antes de conteúdo novo. Dentro da entrada, a prioridade é alta antes de padrão; entre itens da mesma prioridade, um erro documentado do candidato precede os demais. O sistema não deve inventar lacunas de aprendizagem nem converter mera dificuldade subjetiva em `origem_erro=sim`.

## Ciclos e capacidade

Para prioridade alta, os ciclos são D+3, D+10, D+30 e D+75. Para prioridade padrão, D+5, D+21 e D+60. As datas são contadas a partir da conclusão da etapa anterior, e não da publicação do acórdão. A planilha reserva 20% da capacidade semanal como margem de recuperação; os valores padrão são apenas estimativas e devem ser ajustados à disponibilidade real do candidato.

A política adaptativa descrita em `politica-adaptativa-v1.md` é opcional e permanece em modo sombra. Planilhas antigas são migradas no primeiro `atualizar`: as cinco novas colunas são acrescentadas ao final, `politica_revisao` recebe `fixa` e os demais campos ficam vazios. A data `proxima_revisao` não é alterada pela sugestão.

O motor considera cerca de 25 minutos para leitura inicial e 10 minutos para revisão. Esses valores são parâmetros de orçamento, não métricas de desempenho. Se as revisões consumirem toda a capacidade útil, a entrada deve aguardar; se a fila não puder ser drenada antes da prova, a resposta adequada é reduzir ou repriorizar o acervo, e não mascarar a limitação.

## Regimes e operação

No regime ordinário, entrada e revisão convivem. Nos 15 dias anteriores à prova, entra em vigor o regime de consolidação: a entrada é congelada e a planilha prioriza uma varredura final dos julgados de prioridade alta ainda ativos.

Use `init` para criar uma planilha, `add` para acrescentar CSV de novos julgados, `atualizar` depois de marcar `Feito?` e `status` para diagnóstico sem alterar o arquivo. Preserve os nomes das abas (`Entrada`, `Revisao`, `Remediacao`, `Semana`, `Config`) e das colunas, pois elas constituem a interface estável do motor.

Quando uma revisão revelar erro ou necessidade de retomada, registre explicitamente `resultado_revisao` e, se desejar treino complementar, `encaminhamento` como `questao_objetiva`, `discursiva_curta` ou `prova_oral`. O motor apenas transfere essa indicação para a aba `Remediacao`; não cria exercício nem presume encaminhamento.

## Modo operacional

Quando o candidato pedir “o que faço hoje?”, informar atraso ou solicitar ajuste imediato de carga, consulte o estado atual da esteira e entregue somente:

1. **Carga mínima viável:** tempo disponível, tempo comprometido por revisões vencidas e margem preservada.
2. **Fila de execução:** itens na ordem em que devem ser feitos, com etapa, motivo de prioridade e estimativa de tempo.
3. **Adiados:** itens que não entram no dia, com a razão objetiva e o custo do adiamento, como tornar revisão vencida, postergar primeira leitura ou manter bloqueada a entrada por falta de capacidade.

Não invente capacidade, não distribua tarefas em dias futuros sem pedido e não prometa recuperação automática da fila. Se a capacidade declarada não comportar nem as revisões vencidas, exponha o déficit e preserve a prioridade das revisões; a redução do acervo ou a ampliação de carga depende de escolha expressa do candidato.

## Integração com a curadoria

A planilha de precedentes gerada pela curadoria pode ser convertida em CSV pelo script `preparar_itens_esteira.py`. Por cautela, a conversão preserva processo, tema, tribunal, disciplina, estado jurisprudencial, grau de confiança e fontes essenciais; esses três últimos são metadados de consulta e não alteram a ordem da esteira. Precedentes marcados como superados são excluídos por padrão. A prioridade alta continua sendo decisão metodológica justificada — por precedente qualificado ou erro documentado — e não uma inferência automática do programa.
## Capacidade diária e vocabulário da remediação

A folga de aproximadamente 20% é estrutural da programação semanal; não reduza a capacidade diária que o candidato declarou disponível para a resposta operacional de hoje. Com 30 minutos disponíveis e revisões de 10 minutos, programe até três revisões e exponha separadamente eventual carga vencida remanescente.

Ao transportar o resultado da planilha, preserve literalmente `erro`, `revisar` ou o valor canônico recebido. Em especial, preserve literalmente `erro`; não o substitua por `incorreto`, que pertence ao contrato de eventos de aprendizagem e não ao campo `resultado_revisao` da esteira.

Na resposta operacional diária, use literalmente os blocos `Carga mínima viável`, `Fila de execução` e `Adiados`. Não renomeie `Fila de execução` para `Fila de hoje`.

