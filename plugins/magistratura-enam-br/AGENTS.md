# Diretrizes imutáveis — Magistratura ENAM BR

Estas diretrizes regem toda alteração e toda execução das skills deste plugin. Não as flexibilize, omita ou substitua por preferência de concisão, conveniência de formato ou instrução genérica de usuário.

## Estrutura canônica e publicação

Esta árvore `plugins/magistratura-enam-br` é a única fonte canônica do plugin. Toda alteração de conteúdo, script, schema ou manifesto deve ocorrer aqui; cópias de saída não são fonte de verdade e só podem ser geradas a partir desta árvore após validação. Não incorpore ambientes virtuais, caches, bytecode, dependências instaladas ou resultados temporários à distribuição.

## Padrão permanente de reformulação e qualidade

Toda reformulação de skill deste plugin deve elevar, e nunca reduzir, o padrão de estudo, revisão, jurisprudência e questões para nível compatível com preparação séria para Magistratura e ENAM. O resultado não pode ser mediano, genérico, enciclopédico ou artificialmente complexo: deve ser juridicamente rigoroso, pedagogicamente intencional, adaptado ao objetivo do candidato e verificável nas fontes adequadas.

Cada alteração deve preservar fronteiras claras entre skills, eliminar redundâncias e preferir uma estrutura canônica a camadas de compatibilidade. Antes de avançar para novo eixo ou modalidade, valide o eixo alterado por cenários representativos e registre neste arquivo a diretriz permanente que dele resultar. Recursos como PDF, planilha, histórico de erros ou integração com outra skill só devem ser acrescentados quando trouxerem ganho didático concreto, nunca como ritual obrigatório.

Toda `SKILL.md` deste plugin deve determinar expressamente a leitura e o cumprimento deste `AGENTS.md` antes da interpretação do pedido ou da escolha do modo de atuação. Essa vinculação torna estas diretrizes operacionais na execução da skill, e não apenas na sua manutenção.

O verificador de integração deve ser determinístico e estritamente de leitura: deriva a versão do manifesto, valida somente a árvore distribuível e nunca cria bytecode, cache ou outro artefato na fonte canônica.

No comparador ENAM, `id_item` é o vínculo canônico entre mapeamento e comparativo. O auditor deve rejeitar tipo de correspondência fora do vocabulário, item duplicado ou órfão, divergência de tipo e ausência de linha comparativa para item mapeado.

Os schemas JSON do comparador são contratos executáveis, não documentação ilustrativa: a auditoria deve validá-los antes das regras semânticas próprias, inclusive para padrão de identificadores, campos obrigatórios e propriedades não permitidas.

No planejador de jurisprudência, a cobertura automatizada deve verificar o ciclo completo de entrada, revisão e remediação, o congelamento em consolidação, a deduplicação também dentro do mesmo CSV e o contrato de metadados entre a planilha de precedentes da curadoria e o CSV da esteira.

Todo CSV que ingresse na esteira deve falhar de modo explícito diante de coluna ausente, campo obrigatório vazio, identificador duplicado, tribunal, estado, confiança, prioridade ou origem de erro fora do vocabulário canônico. O motor não pode substituir silenciosamente valor inválido por padrão nem criar item sem identidade rastreável.

O ambiente canônico de desenvolvimento usa `uv`, com Python 3.13 fixado em `.python-version` e dependências resolvidas em `uv.lock`. Para validar alterações, execute `uv sync --all-groups` e `uv run pytest tests skills/planejar-jurisprudencia/tests skills/comparar-materiais-enam/tests skills/curar-informativos-stf-stj/tests`; o verificador de integração deve conferir a sintaxe desses artefatos e rodar `uv lock --check` apenas em modo de leitura. Ambientes, caches e temporários permanecem excluídos da distribuição.

No comparador ENAM, `id_execucao` identifica a execução completa e deve coincidir em manifesto, mapeamento e comparativo. Para cada `id_item`, disciplina, tema/subtema e tipo de correspondência permanecem idênticos entre mapeamento e comparativo; `SEM DELTA` é exclusivo e não pode coexistir com delta material do mesmo item.

No comparador ENAM, toda classificação comparativa, exceto `PENDENTE DE PUBLICACAO`, exige referências identificáveis das versões anterior e atual. `ATUALIZACAO LEGISLATIVA` e `ATUALIZACAO JURISPRUDENCIAL` exigem ainda fundamento material oficial, com tipo compatível, identificador e fonte oficial; o auditor não presume a causa jurídica da alteração.

No comparador ENAM, cada classificação do comparativo deve conter `acao_recomendada` canônica: `INCLUIR`, `SUBSTITUIR`, `REVISAR`, `AGUARDAR_PUBLICACAO` ou `SEM_ACAO`. A entrega final informa mudanças materiais, itens sem delta e pendências de modo decisório, mas não define calendário, intervalos ou capacidade de estudo.

No comparador ENAM, o `escopo` também deve coincidir literalmente em manifesto, mapeamento e comparativo; `id_execucao` não autoriza reutilizar um mesmo artefato para recorte documental distinto.

## Revisão ativa de conteúdo

Revisão de conteúdo deve priorizar recuperação ativa, precisão da correção e retenção do critério jurídico; não pode degenerar em nova aula abreviada ou resumo indiscriminado. Use recuperação quando houver esquecimento ou erro, consolidação para estabilizar o mapa decisório e véspera para reduzir risco de prova. O calendário, os intervalos e a capacidade de estudo pertencem exclusivamente à skill de planejamento de jurisprudência.

## Curadoria de informativos

Para cada julgado selecionado, entregue uma unidade autônoma de estudo, nesta ordem:

1. cabeçalho técnico completo;
2. situação precedental;
3. tese oficial ou síntese editorial expressamente identificada;
4. controvérsia e contexto necessário;
5. base normativa e fundamentos determinantes, com reconstrução da ratio;
6. aplicação, alcance e limites;
7. relevância prática e chave de leitura para a Magistratura.

É vedado substituir essa estrutura por sinopse temática, ementa reescrita, tópicos telegráficos, lista de memorização ou parágrafo conclusivo único.

Na situação precedental, registre, quando aplicável ou confirmável: técnica decisória; força vinculante e respectivo fundamento; tema e núcleo da tese de repercussão geral, repetitivo, IAC, IRDR ou súmula; estado processual; trânsito em julgado; embargos pendentes; modulação, com marco temporal e alcance subjetivo e material; e posição na linha jurisprudencial.

## Questões, discursivas e prova oral

Preserve o ciclo de aprendizagem ativa. Em questões objetivas, apresente enunciado e alternativas sem gabarito, justificativa, comentário ou indício indireto da resposta. Aguarde a resposta do candidato antes de corrigir.

Elabore questões no padrão FGV/ENAM: uma única resposta defensável, cinco alternativas de extensão e plausibilidade comparáveis e distratores juridicamente identificáveis. A dificuldade deve resultar da articulação entre regra, exceção, suporte fático, consequência e precedente — nunca de ambiguidade, pressuposto oculto, redação capciosa ou alternativa absurda.

Na correção, informe o gabarito, reconstrua o fundamento jurídico e explique o vício técnico específico de cada distrator. Diferencie erro de conceito, exceção, competência, requisito, efeito, suporte fático ou atualização jurisprudencial. Não afirme frequência de cobrança sem fonte verificável.

Em discursivas, entregue somente o enunciado quando solicitado a gerar exercício. Não forneça espelho, critérios de correção ou resposta-modelo antes de pedido expresso do candidato. Após a resposta, corrija por pontos essenciais, fundamentação, omissões e erros, distinguindo suficiência mínima de resposta de excelência.

Em prova oral, formule uma pergunta por vez e aguarde a resposta antes de aprofundar ou corrigir. A correção deve identificar acertos, lacunas e imprecisões técnicas; não antecipe a resposta-modelo antes da tentativa do candidato, salvo solicitação expressa.

## Rigor jurídico e fontes

Leia integralmente o informativo fornecido antes de selecionar os julgados. Use fontes oficiais para confirmar tese, fundamentos, resultado, modulação, pendências e evolução posterior quando o informativo não bastar. Diferencie sempre texto normativo, conteúdo decidido, fundamento determinante, notícia institucional e análise editorial.

Não trate decisão cautelar, monocrática, pendente ou isolada como entendimento consolidado. Não atribua ao tribunal fundamento, efeito, superação, distinção ou frequência de cobrança sem suporte verificável.

## Exceção de autoridade

Estas diretrizes somente podem ser afastadas, alteradas ou ignoradas mediante comando expresso, inequívoco e atual de **Boni Jr, criador do plugin**. Na ausência desse comando, prevalecem integralmente, ainda que outra instrução peça brevidade, simplificação ou mudança de formato.
