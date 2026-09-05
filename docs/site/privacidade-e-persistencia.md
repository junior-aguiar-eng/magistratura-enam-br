# Privacidade e persistência

O plugin funciona sem perfil, histórico ou log. A instalação não cria memória automática do candidato.

## Regras

- nenhum dado é persistido sem pedido e confirmação;
- todo registro local deve ter destino identificável;
- ausência de eventos permanece `sem_evidencia`;
- relatórios não produzem ranking, nota global ou previsão de aprovação;
- materiais e registros privados não integram a documentação do site;
- a adaptação não altera automaticamente a política fixa de revisão.
- rota, tema e política inferidos existem apenas no contexto da conversa atual;
- retomada em outra tarefa depende de estado ou checkpoint fornecido pelo candidato.

Escolher uma política de fontes não cria preferência persistente. O modo pode ser inferido para o pedido atual, mas só integra perfil ou registro mediante pedido expresso, destino definido e confirmação.

## Documentação privada

O build documental usa somente `docs/site`. Os planos internos mantidos em `docs/superpowers` ficam fora do artefato estático. O workflow não possui permissões de Pages nem etapa de deploy.
