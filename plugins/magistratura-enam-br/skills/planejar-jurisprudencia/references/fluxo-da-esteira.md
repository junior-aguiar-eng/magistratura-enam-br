# Fluxo da esteira de jurisprudência

## Papel no método de estudo

A esteira recebe julgados já curados e os distribui no tempo. Ela não reabre a seleção editorial, não interpreta a ratio decidendi e não substitui o estudo analítico. Sua função é responder, com base no estado efetivamente registrado: o que revisar, o que ler em seguida e se o volume ainda cabe até a prova.

Há duas filas: **Entrada**, para a primeira leitura, e **Revisão**, para julgados que já passaram pela leitura inicial. Revisões vencidas ocupam a capacidade antes de conteúdo novo. Dentro da entrada, a prioridade é alta antes de padrão; entre itens da mesma prioridade, um erro documentado do candidato precede os demais. O sistema não deve inventar lacunas de aprendizagem nem converter mera dificuldade subjetiva em `origem_erro=sim`.

## Ciclos e capacidade

Para prioridade alta, os ciclos são D+3, D+10, D+30 e D+75. Para prioridade padrão, D+5, D+21 e D+60. As datas são contadas a partir da conclusão da etapa anterior, e não da publicação do acórdão. A planilha reserva 20% da capacidade semanal como margem de recuperação; os valores padrão são apenas estimativas e devem ser ajustados à disponibilidade real do candidato.

O motor considera cerca de 25 minutos para leitura inicial e 10 minutos para revisão. Esses valores são parâmetros de orçamento, não métricas de desempenho. Se as revisões consumirem toda a capacidade útil, a entrada deve aguardar; se a fila não puder ser drenada antes da prova, a resposta adequada é reduzir ou repriorizar o acervo, e não mascarar a limitação.

## Regimes e operação

No regime ordinário, entrada e revisão convivem. Nos 15 dias anteriores à prova, entra em vigor o regime de consolidação: a entrada é congelada e a planilha prioriza uma varredura final dos julgados de prioridade alta ainda ativos.

Use `init` para criar uma planilha, `add` para acrescentar CSV de novos julgados, `atualizar` depois de marcar `Feito?` e `status` para diagnóstico sem alterar o arquivo. Preserve os nomes das abas (`Entrada`, `Revisao`, `Semana`, `Config`) e das colunas, pois elas constituem a interface estável do motor.

## Integração com a curadoria

A planilha de precedentes gerada pela curadoria pode ser convertida em CSV pelo script `preparar_itens_esteira.py`. Por cautela, a conversão preserva processo, tema, tribunal e disciplina, exclui precedentes marcados como superados por padrão e atribui prioridade padrão, salvo indicação explícita por processo. A prioridade alta continua sendo decisão metodológica justificada — por precedente qualificado ou erro documentado — e não uma inferência automática do programa.
