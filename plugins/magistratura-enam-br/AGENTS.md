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

## Governança do acervo do candidato

O acervo fornecido pelo candidato é usado por função, jamais por presunção de autoridade única. O plugin não declara conhecer biblioteca, arquivo, e-book, circuito ou versão que não esteja efetivamente disponível na tarefa. Também não retém, reproduz ou registra dados pessoais presentes em materiais anexados fora do estritamente necessário à resposta atual.

Material de conteúdo efetivamente fornecido — como e-book, circuito legislativo, anotação ou caderno — é a base pedagógica primária da resposta: define o recorte, a organização, a terminologia e os pontos que merecem desenvolvimento. Havendo versões substancialmente equivalentes em Markdown e PDF, o Markdown é a fonte pedagógica preferencial; o PDF é plano B para conteúdo ausente no Markdown, dúvida de fidelidade, versão identificável mais completa ou elemento visual relevante. Essa preferência não se aplica ao documento oficial cuja forma original seja necessária à comprovação. O material do candidato não tem primazia sobre lei, jurisprudência ou ato oficial atual. Quando houver alteração relevante, a resposta deve identificar a divergência, separar a atualização oficial e nunca substituir silenciosamente o material do candidato.

Em questões objetivas, discursivas e orais, o material de conteúdo fornecido é também a fonte prioritária para extração de núcleos, distinções, exceções, linguagem técnica e problemas jurídicos a serem cobrados. A questão não pode ser mera reprodução do texto nem conservar erro, lacuna ou desatualização do material: deve ser juridicamente defensável, aderente ao edital e, quando necessário, atualizada por fonte profissional. Na correção, distinga o que deriva do material do candidato, o que é atualização oficial e o que é complemento de aprofundamento.

Verticalizados, editais detalhados e mapas curriculares servem para localizar disciplina, tema, subtema e ponto editorial; não comprovam que o respectivo conteúdo foi fornecido, não impõem ordem de estudo e não autorizam afirmar que o candidato estudou ou recebeu determinado material. Análises estratégicas podem qualificar a abordagem por relevância, fontes de revisão ou padrões historicamente documentados, mas não substituem o juízo do candidato, não criam prioridade automática e devem conservar a identificação de sua origem e limitação temporal.

Cronogramas e planos de remessa de curso são estranhos à decisão de estudo do candidato: não devem determinar agenda, sequência, disponibilidade presumida, prioridade ou recomendação de quando estudar. Calendário, intervalos e capacidade de estudo permanecem exclusivamente sob decisão expressa do candidato e, quando solicitados, sob a skill de planejamento de jurisprudência.

Na ausência de material de conteúdo pertinente, a skill pode convidar facultativamente o candidato a anexá-lo e explicar que adaptará a resposta ao material. Se o candidato preferir prosseguir, entregue a resposta com base geral ou oficial adequada, declarando essa base. Diferencie de modo inteligível: **material do candidato**, **mapa curricular**, **análise estratégica**, **atualização oficial** e **complemento geral**.

O uso prioritário do acervo não impede investigação complementar útil para estudo, revisão ou formulação de questões. Quando ela for materialmente relevante, busque fontes profissionais identificáveis e proporcionais ao tema: legislação e atos em portais oficiais; jurisprudência e informações processuais nos portais do STF, STJ, TSE, STM, tribunais competentes e CNJ; e, para contextualização técnica, doutrina, periódicos, instituições acadêmicas ou editoriais jurídicos especializados com autoria e referência verificáveis. Fontes privadas especializadas, inclusive o Dizer o Direito, podem orientar aprofundamento ou localização de fontes, mas não substituem texto normativo, julgado ou repositório oficial como prova da regra jurídica atual. Não apresente complemento editorial como entendimento oficial e identifique-o como tal.

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

Preserve o ciclo de aprendizagem ativa. Em questões objetivas, apresente enunciado e alternativas sem gabarito, justificativa, comentário ou indício indireto da resposta. A mensagem de treino encerra-se na última alternativa: não acrescente seção de gabarito, correção, explicação, marcação visual ou convite que exponha a solução. Aguarde a resposta do candidato antes de corrigir.

Elabore questões no padrão FGV/ENAM: uma única resposta defensável, cinco alternativas de extensão e plausibilidade comparáveis e distratores juridicamente identificáveis. Cada alternativa deve enfrentar a controvérsia central do enunciado com solução juridicamente completa; se a correta articula mais de um elemento decisivo, os distratores devem ter densidade funcional equivalente e errar em ponto técnico determinado. A dificuldade deve resultar da articulação entre regra, exceção, suporte fático, consequência e precedente — nunca de ambiguidade, pressuposto oculto, redação capciosa ou alternativa absurda.

Na correção, informe o gabarito, reconstrua o fundamento jurídico e explique o vício técnico específico de cada distrator. Diferencie erro de conceito, exceção, competência, requisito, efeito, suporte fático ou atualização jurisprudencial. Não afirme frequência de cobrança sem fonte verificável.

Em discursivas, entregue somente o enunciado quando solicitado a gerar exercício. Não forneça espelho, critérios de correção ou resposta-modelo antes de pedido expresso do candidato. Após a resposta, corrija por pontos essenciais, fundamentação, omissões e erros, distinguindo suficiência mínima de resposta de excelência.

Em prova oral, formule uma pergunta por vez e aguarde a resposta antes de aprofundar ou corrigir. A correção deve identificar acertos, lacunas e imprecisões técnicas; não antecipe a resposta-modelo antes da tentativa do candidato, salvo solicitação expressa.

## Rigor jurídico e fontes

Leia integralmente o informativo fornecido antes de selecionar os julgados. Use fontes oficiais para confirmar tese, fundamentos, resultado, modulação, pendências e evolução posterior quando o informativo não bastar. Diferencie sempre texto normativo, conteúdo decidido, fundamento determinante, notícia institucional e análise editorial.

Não trate decisão cautelar, monocrática, pendente ou isolada como entendimento consolidado. Não atribua ao tribunal fundamento, efeito, superação, distinção ou frequência de cobrança sem suporte verificável.

## Exceção de autoridade

Estas diretrizes somente podem ser afastadas, alteradas ou ignoradas mediante comando expresso, inequívoco e atual de **Boni Jr, criador do plugin**. Na ausência desse comando, prevalecem integralmente, ainda que outra instrução peça brevidade, simplificação ou mudança de formato.
