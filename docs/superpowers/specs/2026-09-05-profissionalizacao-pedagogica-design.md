# Profissionalização pedagógica e despersonificação

**Data:** 2026-09-05

**Linha de base:** plugin `magistratura-enam-br` 0.5.0

**Estado:** especificação para revisão

## 1. Finalidade

Esta evolução transforma o plugin em um produto jurídico especializado para bacharéis em Direito que se preparam para concursos de alta complexidade, especialmente Magistratura e ENAM. A mudança preserva a densidade jurídica existente, elimina pressupostos vinculados ao perfil de seu autor e torna cada frente de estudo tecnicamente especializada em seu próprio objetivo.

Profissionalização não será medida pela redução do número de instruções ou de linhas. Neste projeto, higiene técnica significa refinar: preservar o que sustenta qualidade, aprofundar o que está subespecificado, realocar regras para a camada correta, generalizar preferências pessoais e remover apenas o que seja redundante, contraditório ou sem função demonstrável.

## 2. Princípios de produto

1. **Especialização jurídica:** o público pressuposto é formado por bacharéis em Direito. O plugin pode explicar fundamentos, mas não converte o estudo em introdução genérica nem simplifica institutos complexos até perder precisão.
2. **Profundidade funcional:** legislação, doutrina e jurisprudência entram porque esclarecem a estrutura, o alcance, os limites ou a aplicação do problema jurídico. Acumular conteúdo sem função não equivale a aprofundar.
3. **Estrutura interna e fluidez externa:** as skills operam com contratos rigorosos, mas a conversa não assume a forma de formulário. O plugin aproveita o pedido, o contexto da sessão, os materiais fornecidos e, se autorizado, o perfil persistente. Faz no máximo uma pergunta realmente discriminante antes de iniciar, salvo impossibilidade material.
4. **Progressão sem engessamento:** cada frente possui uma lógica própria, mas seleciona os componentes adequados ao pedido. Recursos como quadros, flashcards, questões e roteiros não aparecem por obrigação formal.
5. **Rastreabilidade:** afirmações jurídicas temporalmente sensíveis devem ser verificáveis. Norma, precedente, inferência pedagógica e conclusão permanecem distinguíveis.
6. **Personalização consentida:** nenhum perfil pessoal integra a distribuição. A personalização é opcional, individual, persistente, local e depende de autorização explícita para gravar ou atualizar dados.
7. **Conservadorismo arquitetural:** a evolução parte dos contratos, scripts, schemas e testes da versão 0.5.0. Mudanças de estrutura devem demonstrar preservação ou ganho de capacidade.

## 3. Escopo e limites

Entram no escopo:

- despersonificação de instruções, exemplos, defaults e recomendações;
- especialização didática das frentes de estudo;
- aprofundamento do estudo dogmático como eixo central;
- aperfeiçoamento dos contratos de fontes e de perfil;
- redução de duplicações e contradições entre `AGENTS.md`, skills e referências;
- avaliações comportamentais e jurídicas representativas;
- compatibilidade e migração dos dados locais existentes.

Não entram nesta etapa:

- MCP, serviço remoto ou nova camada de infraestrutura;
- conta de usuário, sincronização em nuvem ou telemetria;
- ampliação para educação geral ou público sem formação jurídica;
- substituição integral das skills maduras;
- redução de conteúdo por meta abstrata de concisão.

## 4. Organização das instruções

As responsabilidades serão distribuídas por função:

- `AGENTS.md`: identidade do produto, invariantes transversais, regras de segurança jurídica, fluidez conversacional e roteamento;
- `skills/*/SKILL.md`: gatilho, objetivo, fluxo e critérios próprios de cada frente;
- `skills/*/references/`: contratos extensos, modelos de saída, taxonomias, exemplos e critérios especializados carregados quando necessários;
- `scripts/` e `schemas/`: operações determinísticas, validação, persistência, reconstrução e migração;
- `evals/` e testes: comprovação estrutural, comportamental e jurídica.

Uma regra normativa terá uma fonte canônica. As skills podem apontar para ela e acrescentar regras locais, sem manter cópias divergentes. A reorganização só poderá excluir uma regra depois de identificar sua finalidade, consumidores e cobertura equivalente.

## 5. Arquitetura pedagógica das frentes

### 5.1. Orquestração do percurso

A orquestração interpreta a intenção presente e oferece continuidade natural. Não presume concurso, banca, disciplina vulnerável, percentuais de ciclo ou percurso anterior. Quando houver perfil autorizado, utiliza-o como evidência auxiliar, nunca como comando irrevogável.

Pedidos específicos entram diretamente na frente correspondente. Pedidos amplos podem receber uma proposta breve de direção, sem menu obrigatório, diagnóstico compulsório ou sequência de perguntas. A recomendação deve explicar por que a atividade é adequada à evidência disponível.

### 5.2. Estudo dogmático integrado

O estudo dogmático é a principal frente do plugin. Seu produto não é uma sinopse, um glossário nem um texto editorial exaustivo. É uma sessão cumulativa que constrói domínio sobre institutos e problemas complexos em unidades intelectualmente completas, conectadas entre si.

O fluxo interno distingue quatro situações:

- **resposta pontual:** resolve uma dúvida delimitada com a profundidade necessária;
- **sessão de estudo:** desenvolve progressivamente um tema complexo em múltiplos blocos;
- **revisão:** recompõe estruturas decisórias já estudadas e testa distinções;
- **síntese:** organiza conhecimento previamente desenvolvido, sem substituir o estudo principal.

Uma sessão começa pelo problema organizador do tema e estabelece seu mapa conceitual: função, fundamentos, categorias, relações, controvérsias, consequências e fronteiras. Esse mapa não precisa ser exibido como índice rígido; ele orienta a progressão e evita tanto lacunas quanto despejo de conteúdo.

#### Integração entre dogmática, legislação e jurisprudência

Norma e jurisprudência serão incorporadas durante a explicação dos conceitos, no ponto em que desempenham função cognitiva. A referência legal deve ser cirúrgica: identifica o dispositivo que institui, delimita, excepciona ou conecta a categoria explicada. A jurisprudência entra para definir, confirmar, restringir, excepcionar, atualizar ou aplicar a construção dogmática.

Isso produz a seguinte unidade de explicação:

1. apresenta-se o problema ou a distinção;
2. desenvolve-se a categoria dogmática necessária;
3. ancora-se a construção nos dispositivos pertinentes;
4. incorpora-se o precedente quando ele modifica a compreensão ou mostra seu funcionamento;
5. explicita-se a consequência prática, a controvérsia ou o limite;
6. conecta-se o resultado ao próximo núcleo do estudo.

Não haverá bloco isolado de jurisprudência quando o julgado for parte da própria compreensão do instituto. Também não haverá desfile de artigos e precedentes. Uma referência só permanece se o estudante puder perceber sua função explicativa.

As fontes jurisprudenciais oficiais utilizadas serão reunidas de forma compacta ao final de cada resposta, com identificação suficiente para consulta. No corpo, a citação permanece leve e vinculada à proposição que sustenta. Teses qualificadas, súmulas e entendimentos determinantes recebem prioridade sobre decisões meramente ilustrativas.

#### Ritmo e continuidade

Cada bloco deve resolver um núcleo relevante e preparar o seguinte. O encerramento registra o ponto alcançado e a conexão natural da continuidade, sem repetir sumários padronizados. O plugin pode usar pergunta de transferência, quadro, flashcard ou caso curto quando isso consolidar aquela etapa; nenhum desses recursos é obrigatório em todas as respostas.

O usuário pode aprofundar uma controvérsia, retornar a um pressuposto ou mudar o recorte sem perder a arquitetura da sessão. A progressão é orientada, não linearmente imposta.

### 5.3. Casos complexos

Essa frente treina qualificação jurídica, seleção de fatos relevantes e construção de soluções concorrentes. O caso deve conter fatos com função analítica, sem ruído artificial usado apenas para aumentar dificuldade.

A resolução identifica questões, regimes incidentes, fontes, argumentos plausíveis, relação entre regra e fato, consequências e limites. Havendo mais de uma solução defensável, explicita-se o pressuposto que altera o resultado e o entendimento prevalente ou mais atual. A correção distingue erro de identificação, enquadramento, fonte, inferência e conclusão.

### 5.4. Questões objetivas

Mantém-se o padrão técnico consolidado: caso consistente, cinco alternativas plausíveis, chave única, paralelismo e auditoria prévia. As alternativas erradas devem representar erros jurídicos reconhecíveis, não simples caricaturas.

A execução distingue treino, simulado e remediação. Em simulado, a correção vem depois da resposta. Em treino, a interação pode focalizar um raciocínio específico. Em remediação, a nova questão deve transferir a estrutura do erro para hipótese independente, sem apenas reformular a questão anterior.

### 5.5. Discursiva

A frente discursiva avalia atendimento ao comando, identificação de problemas, fundamento jurídico, aplicação aos fatos, tratamento de objeções, conclusão e economia argumentativa. O espelho separa conteúdo indispensável, desenvolvimento de excelência e elementos acessórios.

A correção mostra onde a resposta perdeu pontos e como reconstruir a passagem deficiente. Não se limita a fornecer um modelo final. Quando pertinente, oferece reescrita dirigida do trecho crítico e uma nova variação para verificar transferência.

### 5.6. Oral

A simulação oral apresenta uma pergunta por vez e usa a resposta para escolher a intervenção seguinte. Repreguntas examinam precisão conceitual, fundamento, exceções e capacidade de sustentar a conclusão sob mudança dos fatos.

A correção principal ocorre ao final do ciclo, salvo erro que inviabilize sua continuidade. O feedback distingue conteúdo, organização, objetividade e segurança argumentativa. Em interação exclusivamente textual, o plugin não afirma avaliar voz, ritmo acústico ou linguagem corporal.

### 5.7. Revisão e remediação

A revisão recupera relações decisórias, não listas isoladas. O diagnóstico classifica o erro por natureza e grau de assistência. A remediação correspondente pode recompor o conceito, contrastar categorias, reconstruir o fundamento ou aplicar a estrutura em caso novo.

O sistema distingue:

- acerto ou recomposição com assistência;
- transferência independente para hipótese nova;
- retenção posterior em revisão espaçada.

Somente as duas últimas fornecem evidência forte de domínio autônomo.

### 5.8. Curadoria jurisprudencial

A estrutura técnica existente será preservada: tese, contexto, fundamento determinante, alcance, limites, distinções, situação processual e utilidade para prova. A apresentação passa a ser proporcional ao julgado; campos sem função não geram texto burocrático.

O produto deve separar conteúdo expresso da decisão, síntese do curador e inferência de aplicabilidade. Fontes oficiais permanecem prioritárias, e a atualidade da pesquisa integra o resultado.

### 5.9. Planejamento jurisprudencial

O planejamento mantém operações determinísticas e blocos de revisão quando forem funcionalmente necessários. A seleção considera relevância, dificuldade, atualidade e evidência individual disponível. O perfil não pode cristalizar fraquezas antigas: desempenho assistido, transferência e retenção alteram a prioridade de modos diferentes.

### 5.10. Comparação de materiais

A frente conserva rastreabilidade, preservação dos originais e identificação de diferenças por edição, tema e subtema. O aperfeiçoamento concentra-se na utilidade decisória: indicar o que surgiu, mudou, desapareceu ou recebeu novo tratamento e qual ação de estudo decorre da diferença.

Ausência aparente, mudança editorial e alteração jurídica não serão tratadas como equivalentes. Toda conclusão deve permitir retorno ao material de origem.

## 6. Perfil individual local

A personalização será um recurso opt-in. Cada usuário poderá criar, salvar, carregar, inspecionar, exportar, reconstruir e apagar seu próprio perfil em armazenamento local. O plugin deve pedir autorização explícita antes da primeira gravação e antes de adotar um local de persistência que ainda não tenha sido autorizado.

Carregar um perfil não autoriza novas gravações. A permissão de leitura, a permissão de atualização e a escolha de usar o perfil naquela sessão são estados distintos.

O modelo mantém eventos append-only como fonte primária e perfis derivados reconstruíveis. Cada evento relevante deve registrar, quando aplicável:

- identidade estável da atividade e da versão da fonte;
- disciplina, assunto, habilidade e modalidade;
- natureza do erro ou do acerto;
- grau de assistência recebido;
- evidência de transferência e de retenção;
- data e contexto mínimos para interpretação.

Preferências declaradas pelo usuário ficam separadas de inferências derivadas do desempenho. O plugin deve permitir correção ou exclusão sem editar silenciosamente o histórico: mudanças relevantes são representadas por novos eventos ou operações explícitas de descarte e reconstrução.

Os dados distribuídos com o plugin não conterão histórico, disciplinas vulneráveis, objetivos, percentuais, percursos ou estilo de estudo de seu autor.

## 7. Higiene técnica sem perda de capacidade

Toda alteração será classificada como uma destas operações:

- **preservar:** regra já adequada e comprovadamente útil;
- **aprofundar:** contrato correto, mas insuficiente para a exigência da frente;
- **realocar:** regra válida mantida em fonte canônica mais apropriada;
- **generalizar:** preferência pessoal convertida em opção ou regra aplicável a qualquer usuário;
- **remover:** duplicação, contradição ou elemento sem função, com cobertura verificada.

Antes de mover ou remover conteúdo, será produzido um inventário que ligue cada regra a seu objetivo, consumidores, testes e destino. Contagem de linhas, tamanho do prompt ou redução de tokens não são critérios autônomos de qualidade.

Schemas receberão versionamento e migração explícitos. Scripts existentes serão preservados quando sua lógica continuar válida. Instruções probabilísticas não substituirão validações determinísticas de integridade, persistência ou formato.

## 8. Avaliação

A versão 0.5.0 constitui a linha de base. A suíte atual passa integralmente com diretório temporário local: **207 testes aprovados**. Essa evidência confirma a integridade técnica existente, mas não demonstra, isoladamente, superioridade pedagógica ou generalização entre usuários.

A profissionalização será avaliada em quatro camadas:

1. **integridade estrutural:** schemas, scripts, migrações, links, comandos e compatibilidade;
2. **comportamento:** cenários representativos por frente, incluindo pedidos vagos, específicos, continuidade, interrupção, ausência de perfil e perfil autorizado;
3. **qualidade jurídica:** correção normativa, precisão conceitual, atualidade jurisprudencial, distinções e rastreabilidade;
4. **efeito pedagógico observável:** independência, transferência e retenção, sem confundir respostas assistidas com domínio.

Testes de palavras-chave ficam restritos a contratos realmente literais. Critérios semânticos serão avaliados por rubricas, exemplos reservados e revisão humana especializada quando a automação não puder provar a qualidade jurídica.

Cenários obrigatórios incluem:

- estudo dogmático aprofundado com legislação e jurisprudência integradas no desenvolvimento;
- pedido simples que não deve acionar uma aula completa;
- continuidade de sessão sem repetição editorial;
- questão objetiva com distratores juridicamente plausíveis;
- caso com soluções concorrentes e pressuposto decisivo;
- correção discursiva que reconstrói o erro;
- oral com repregunta adaptativa;
- uso sem perfil, leitura de perfil e gravação autorizada;
- ausência de vazamento de preferências do autor;
- comparação e curadoria com fontes rastreáveis.

## 9. Compatibilidade e evolução

A implementação será incremental. Primeiro será inventariada a arquitetura atual e criada uma linha de base comportamental. Em seguida, serão reorganizadas as invariantes comuns sem alterar resultados pretendidos. O estudo dogmático e os casos complexos serão refinados antes das demais frentes, porque definem o núcleo pedagógico. As skills maduras receberão mudanças controladas. O perfil local evoluirá com migração versionada e possibilidade de reconstrução a partir dos eventos.

Cada etapa deve manter os contratos públicos necessários, registrar mudanças intencionais e provar que nenhuma capacidade jurídica foi perdida. Alterações amplas de redação só serão aceitas quando corresponderem a uma decisão arquitetural ou pedagógica identificável.

## 10. Critérios de aceitação

A profissionalização estará concluída quando:

- nenhum default distribuído pressupuser o perfil particular do autor;
- o uso sem perfil for completo e o uso com perfil depender de consentimento local explícito;
- o estudo dogmático construir temas complexos em progressão cumulativa, com normas e precedentes integrados de forma cirúrgica;
- as fontes jurisprudenciais oficiais aparecerem ao final da resposta em formato consultável, sem romper a fluidez do corpo;
- cada frente possuir objetivo, fluxo, produto e critérios de qualidade próprios;
- a conversa iniciar pelo pedido do usuário, sem entrevista compulsória;
- regras transversais possuírem fonte canônica e não divergirem entre arquivos;
- scripts, schemas e dados locais existentes tiverem compatibilidade ou migração documentada;
- avaliações comportamentais e jurídicas demonstrarem a preservação das capacidades atuais e os ganhos pretendidos;
- documentação e exemplos descreverem o produto geral, sem histórico pessoal incorporado.
