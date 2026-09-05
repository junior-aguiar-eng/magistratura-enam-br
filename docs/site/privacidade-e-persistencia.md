# Privacidade e persistência

O plugin funciona sem perfil, histórico ou log. A instalação não cria memória automática do candidato.

Quando o candidato habilita a biblioteca de questões, a autorização é restrita a uma pasta local. A indexação lê recursivamente arquivos Markdown dessa pasta, respeita exclusões configuradas e grava seus artefatos apenas na subpasta `.estudo-juridico`: `index.json`, `questoes.jsonl`, `tentativas.jsonl` e `eventos.jsonl`. Os Markdown originais não são modificados.

Cada usuário pode manter seu próprio perfil em caminho local escolhido. Carregar o arquivo, usá-lo na sessão, gravar eventos, reconstruir o perfil, exportar e excluir são operações distintas. Somente as operações de escrita ou exclusão exigem suas confirmações explícitas correspondentes.

## Regras

- nenhum dado é persistido sem pedido e confirmação;
- todo registro local deve ter destino identificável;
- ausência de eventos permanece `sem_evidencia`;
- relatórios não produzem ranking, nota global ou previsão de aprovação;
- materiais e registros privados não integram a documentação do site;
- a adaptação não altera automaticamente a política fixa de revisão.
- rota, tema e política inferidos existem apenas no contexto da conversa atual;
- retomada em outra tarefa depende de estado ou checkpoint fornecido pelo candidato.
- preferências declaradas permanecem separadas de inferências derivadas do desempenho;
- eventos preservam identidade da atividade, versão da fonte e grau de assistência quando produzidos no contrato v2.
- o gabarito permanece no servidor e só é revelado ao componente depois do envio da tentativa;
- o túnel usa conexão de saída e não transforma a biblioteca em armazenamento remoto;
- credenciais e perfis do túnel não são versionados nem incorporados ao widget.

Escolher uma política de fontes não cria preferência persistente. O modo pode ser inferido para o pedido atual, mas só integra perfil ou registro mediante pedido expresso, destino definido e confirmação.

## Documentação privada

O build documental usa somente `docs/site`. Os planos internos mantidos em `docs/superpowers` ficam fora do artefato estático. O workflow não possui permissões de Pages nem etapa de deploy.
