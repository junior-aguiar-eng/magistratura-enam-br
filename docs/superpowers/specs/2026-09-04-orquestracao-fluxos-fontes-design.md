# Orquestracao conversacional e governanca de fontes 0.5.0

## Proposito

Evoluir o Estudo Juridico Avancado de um conjunto de cinco skills coordenadas por descricoes para um ambiente de estudo com fluxo conversacional explicito, transicoes inteligentes e politica de fontes controlada pelo candidato. A estrutura interna deve ser rigorosa, mas a experiencia externa deve permanecer natural, sem formularios, entrevistas ou menus repetitivos.

## Principios invariantes

1. Pedido generico orienta; pedido especifico executa diretamente.
2. O candidato controla tema, modalidade, fontes, persistencia e mudanca de percurso.
3. O sistema aproveita o contexto disponivel e nao pergunta novamente o que puder inferir com seguranca.
4. No maximo uma pergunta e feita quando a ambiguidade impedir materialmente o estudo seguro.
5. Transicoes de rota sao comunicadas em linguagem breve, sem confirmacao ritual.
6. Confirmacao e exigida somente para persistencia, abandono de atividade pendente, acao externa ou mudanca com perda material de contexto.
7. Estado da conversa e efemero por padrao. Continuidade entre sessoes depende de mecanismo local, caminho indicado e consentimento expresso.
8. Cada skill preserva sua autoridade de dominio e nao executa silenciosamente a competencia de outra.
9. Material do candidato nunca e confundido com fonte oficial, complemento doutrinario ou noticia.
10. Busca externa produz sintese juridica integrada e rastreavel, nunca portfolio de links ou agregador de noticias.

## Arquitetura

```text
interface.defaultPrompt
        |
        v
interpretacao da intencao
        |
        v
orquestrador de percurso
        |
        +--> estado efemero da sessao
        +--> politica de fontes
        +--> protocolo de transicao
        |
        v
skill especializada
        |
        v
continuar | mudar modo | mudar tema | mudar skill | suspender | retomar
```

### Camada de entrada

O manifesto oferece prompts iniciais distintos para jornada guiada, estudo de tema, treino, curadoria, comparacao e planejamento jurisprudencial. Um gatilho generico ativa o orquestrador; um gatilho especifico sinaliza diretamente a skill adequada.

### Camada de orquestracao

`acompanhar-percurso-magistratura` deixa de ser apenas um emissor de YAML e passa a coordenar a experiencia conversacional. Ele pode apresentar as capacidades na entrada generica, interpretar objetivo composto, preservar uma pendencia e anunciar uma transicao. Nao explica Direito, nao cura informativos, nao compara documentos e nao agenda revisoes.

### Camada de execucao

- `estudar-direito-magistratura`: explicacao aprofundada, revisao ativa, questao objetiva, discursiva, prova oral e estudo de julgado selecionado.
- `curar-informativos-stf-stj`: leitura integral, selecao e comentario de informativos oficiais.
- `comparar-materiais-enam`: comparacao de materiais e producao de deltas rastreaveis.
- `planejar-jurisprudencia`: esteira, revisao espacada e remediacoes de julgados.
- `acompanhar-percurso-magistratura`: entrada, roteamento, transicao e retomada.

## Estado conversacional

O estado minimo e um contrato interno, nao uma resposta mostrada ao candidato:

```yaml
schema_version: "1.0"
skill_ativa: estudar-direito-magistratura
modalidade_ativa: revisao_ativa
tema_ativo: controle_de_constitucionalidade
etapa: desenvolvimento
pendencia: null
rota_suspensa: null
politica_fontes: acervo_com_validacao_oficial
```

Valores de transicao:

- `CONTINUAR`: mesma skill, modalidade e tema.
- `MUDAR_TEMA`: mesma skill e modalidade, novo conteudo.
- `MUDAR_MODALIDADE`: mesma skill e tema, novo metodo de estudo.
- `MUDAR_SKILL`: transferencia entre autoridades de dominio.
- `SUSPENDER`: preserva pendencia retomavel apenas no contexto disponivel.
- `RETOMAR`: restaura uma rota efetivamente presente na conversa ou em registro fornecido.
- `ENCERRAR`: conclui a rota sem inventar persistencia ou progresso.

## Protocolo de transicao

### Transicao sem confirmacao

Quando a intencao for inequivoca e nao houver perda material, a skill comunica e executa:

> Manteremos o tema e passaremos da revisao para uma questao objetiva.

### Transicao com confirmacao

Uma unica pergunta e permitida quando existir atividade incompleta que seria descartada:

> A questao anterior ficou sem resposta. Voce prefere suspendê-la para retomada nesta conversa ou encerra-la?

### Mudanca incidental

Mencionar outro instituto, precedente ou disciplina nao muda automaticamente a rota. A mudanca exige pedido funcional reconhecivel, como estudar, comparar, curar, planejar, suspender ou retomar.

### Retomada

Retomada na mesma conversa usa o estado efetivamente disponivel. Em nova conversa, o plugin somente retoma a partir de perfil, log, evento ou checkpoint fornecido pelo candidato. Nunca alega memoria implicita.

## Politicas de fontes

### `acervo_exclusivo`

- Usa somente o material efetivamente disponibilizado pelo candidato.
- Nao pesquisa nem complementa por memoria externa.
- Identifica lacunas, contradicoes e sinais de possivel desatualizacao.
- Nao certifica atualidade legislativa ou jurisprudencial sem fonte suficiente.

### `acervo_com_validacao_oficial`

- E o padrao quando existe material pertinente e o candidato nao restringiu a pesquisa.
- Mantem o material como base pedagogica.
- Consulta fonte oficial apenas quando isso alterar precisao, atualidade, alcance ou defensabilidade.
- Explica divergencias sem substituir silenciosamente o texto original.

### `pesquisa_juridica_completa`

- Aplica-se quando nao ha acervo suficiente ou quando o candidato pede aprofundamento externo.
- Prioriza fontes primarias e usa fontes secundarias apenas para contextualizacao, doutrina, debate ou localizacao.
- Distingue fato normativo, tese judicial, fundamento determinante, interpretacao editorial e inferencia analitica.

## Registro de fontes confiaveis

### Nivel 1: fontes primarias

- STF: jurisprudencia, informativos, temas de repercussao geral, sumulas e dados processuais.
- STJ: jurisprudencia, informativos, temas repetitivos, IAC, sumulas e dados processuais.
- Planalto: Constituicao, codigos, leis, decretos e demais atos federais disponibilizados no portal oficial.

Fontes primarias controlam texto vigente, tese, resultado, estado processual e qualificacao do precedente. Quando o assunto depender de outro orgao competente, a inclusao de nova fonte oficial exige identificacao expressa no registro, sem abrir pesquisa irrestrita.

### Nivel 2: fontes juridicas secundarias aprovadas

- Dizer o Direito.
- JOTA.
- Thomson Reuters / Revista dos Tribunais.
- Outra fonte somente depois de cadastrada com nome, finalidade, dominio verificado, tipo editorial e limites de uso.

Fontes secundarias podem explicar, contextualizar, localizar controversias e apresentar doutrina. Nao provam sozinhas vigencia normativa, teor de tese, resultado de julgamento, modulacao ou transito em julgado.

## Politica de apresentacao

A resposta integra as fontes ao raciocinio juridico. Nao apresenta manchetes, cards, listas de resultados nem comentarios pagina a pagina. Quando a rastreabilidade for relevante, encerra com referencia compacta:

> **Base consultada:** CF, art. X; STF, Tema Y; STJ, REsp Z; complemento editorial: Dizer o Direito.

Links brutos nao sao reproduzidos no corpo. Citacoes clicaveis geradas automaticamente pela plataforma podem permanecer, mas nao alteram o formato editorial da skill.

## Inferencia e perguntas

O fluxo segue `observar -> inferir -> comunicar -> executar`.

- Material anexado e pedido de estudo: inferir `acervo_com_validacao_oficial`.
- Pedido "use somente meu material": inferir `acervo_exclusivo`.
- Pedido "pesquise e aprofunde": inferir `pesquisa_juridica_completa`.
- Pedido direto de questao com tema: executar sem ambientacao.
- Clique em jornada guiada sem tema: apresentar capacidades e fazer uma unica pergunta compacta.
- Ambiguidade nao material: aplicar o padrao e seguir.
- Ambiguidade juridicamente relevante: perguntar antes de concluir ou pesquisar.

## Persistencia

O estado de rota nao e gravado automaticamente. Se o candidato solicitar continuidade entre sessoes, a persistencia reutiliza os contratos locais existentes e registra apenas o minimo necessario. Preferencia de fontes somente integra o perfil quando declarada pelo candidato e confirmada para gravacao; inferencia contextual nao se transforma em preferencia permanente.

## Criterios de sucesso

1. Um pedido generico recebe ambientacao curta e nao gera tema ou questao arbitrarios.
2. Um pedido especifico chega diretamente a skill e modalidade corretas.
3. Mudanca de tema, modalidade ou skill e corretamente distinguida.
4. Atividade pendente nao e perdida silenciosamente.
5. A conversa nao repete menus, perguntas ou politicas ja estabelecidas.
6. `acervo_exclusivo` nao realiza busca externa.
7. Complementacao externa prioriza STF, STJ e Planalto e limita fontes secundarias ao registro aprovado.
8. Fontes secundarias nao substituem verificacao primaria.
9. A resposta nao se converte em portfolio de noticias ou links.
10. Nenhum estado ou preferencia e persistido sem consentimento e caminho adequado.

