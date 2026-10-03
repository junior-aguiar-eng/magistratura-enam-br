# Incrementos MCP e calibração pedagógica

Status: proposta para implementação; nenhum incremento implementado por este documento.

## Objetivo e base

Evoluir a experiência de questões no ChatGPT e aproveitar as ideias úteis da skill Claude `estudo-juridico-magistratura-br` 2.2.0, mantendo o rigor jurídico, a correção integral e o funcionamento sem MCP da versão 0.7.5.

Base conferida: `main`, commit `8b245f10bce3aa85fa41c2b114a46fcdc9251342`, em 2026-10-02. Fonte canônica: `plugins/magistratura-enam-br`. O ZIP do Claude está em `C:/Users/Boni Jr/Desktop/estudo-juridico-magistratura-br_v2.2.0.zip`; SHA-256 conferido: `e564b285337877fd7233282a9fd88b7bf2761171d2d9b3aa6ffc29971ccf371c`. Reconfirmar a identidade na execução. O pacote é referência de ideias, não fonte normativa nem prova de desempenho do Claude instalado.

A análise do ZIP reproduziu duas falhas: `validar_julgado.py` exige campos diferentes dos prescritos pela skill e aprova apenas rótulos; `auditar_questoes.py` aprova cinco alternativas com a mesma letra. Não importar os scripts sem redesenho. As proporções de formatos e dificuldade atribuídas ao ENAM não vieram acompanhadas dos dados de contagem; não adotá-las como estatística comprovada.

## Frente A — MCP e ChatGPT

### A1. Instruções gerais e contratos

Enviar instruções compactas pelo servidor, derivadas de seções canônicas versionadas: política de fontes, elaboração da questão, sequência criar/renderizar/responder, correção integral, invalidação e fallback. Declarar que pesquisa externa e leitura de anexos dependem das capacidades do cliente. A conexão MCP não carrega automaticamente as skills locais.

Padronizar a visibilidade de ferramentas pelo campo `ui.visibility`, mantendo responder e renderizar acessíveis ao modelo e ao app para preservar resposta textual e interativa. Ferramentas de administração continuam disponíveis ao modelo, sem necessidade de exposição pelo card. Confirmar os `outputSchema` efetivamente anunciados e tornar específicos os resultados de sessões, diagnóstico e histórico; não presumir que `structured_output=True` já descreva todas as invariantes.

Não transformar anotações MCP em mecanismo de autorização. Confirmar gravação e preservar a semântica de leitura/escrita mesmo quando o host oferecer menos solicitações de permissão.

### A2. Bridge e ciclo de vida

Priorizar `App` e o protocolo MCP Apps quando negociados pelo host. Manter compatibilidade OpenAI em hosts que exponham somente esse bridge. Escolha por capacidades; não tentar os dois caminhos para a mesma mutação. Não repetir automaticamente uma resposta por outro transporte após timeout, pois o primeiro envio pode ter sido efetivado.

Tratar entrada após aprovação, resultados tardios, envelopes inválidos e descarte do componente. Entrada de renderização fornece somente `session_id`; a questão vem de resultado validado. Não ler nem renderizar payload privado de criação. Preservar as proteções contra regressão de estado e resultados de outra sessão.

### A3. Continuidade card–conversa

Após tentativa concluída, oferecer: **Explique meu erro** (apenas no erro), **Aprofunde esta distinção** e **Outra questão sobre este ponto**. Cada ação é iniciada pelo usuário e gera uma mensagem vinculada à sessão. Não gera questão nem registra desempenho automaticamente.

Adicionar consulta de uma sessão sem renderização, reutilizando `QuestionRepository.get_session`. O modelo recupera o estado autorizado pelo servidor antes de aprofundar ou criar outra questão; a consulta não reabre card nem grava tentativa. Contexto emitido pelo widget contém somente identificador, ação, tema e estado observado. O servidor continua decidindo o que liberar.

Se o host não suportar mensagens, apresentar texto curto copiável. Após invalidação, desativar ações que pressupõem gabarito válido; permitir apenas solicitar nova questão com aviso do defeito. Falha de envio não anuncia continuidade iniciada.

### A4. Estado, aparência e fullscreen

Preservar somente estado de apresentação: sessão, alternativa ainda não enviada e painéis expandidos. Não guardar gabarito, correção, fontes privadas, resultado ou evidência de domínio em `widgetState`. Restaurar apenas snapshot versionado válido da mesma sessão; servidor prevalece em answered/invalidated. Não usar localStorage como banco de questões.

Aplicar variáveis de estilo e tema do host na inicialização e nas mudanças, com fallback local. Preservar identidade visual discreta, navegação por teclado, foco da correção, contraste, largura móvel e redução de movimento.

Fullscreen incluído na primeira entrega por decisão de Boni: oferecer **Expandir para estudar** no card e **Voltar ao chat** no modo expandido, quando o host permitir a mudança. Entrada somente por ação explícita; a apresentação inicial permanece inline. Solicitar `fullscreen`/`inline` por `App.requestDisplayMode`, ou pela extensão OpenAI compatível quando esse for o bridge negociado. O modo efetivamente concedido pelo host define layout e rótulo; uma solicitação recusada ou limitada não simula expansão nem perde a sessão.

A expansão serve ao estudo do enunciado, alternativas, correção e fontes, com coluna de leitura confortável, rolagem acessível e respeito ao composer e às áreas reservadas pelo host. Preservar alternativa pendente, painéis e resultado ao entrar/sair; expandir não responde questão, cria sessão ou libera gabarito. Ausência de suporte mantém o card utilizável. Homologar ida e volta, troca de tema e recusa em desktop e viewport móvel.

## Frente B — melhorias pedagógicas do Claude

### B1. Revisão ancorada

Revisão destila o conteúdo efetivamente estudado ou enviado. Relacionar síntese, distinção e flashcards ao trecho disponível. Se esse material existir mas estiver inacessível, solicitar somente o recorte necessário; se o candidato preferir prosseguir, declarar a nova base. Não simular memória de outras sessões. Manter separadas recuperação, consolidação e véspera; cronograma continua sob a skill de planejamento.

### B2. Formatos e desenho das questões

Ampliar os formatos: alternativas diretas, assertivas numeradas, V/F com sequências e associação de colunas. Todos terminam em cinco escolhas A–E e uma chave única; cada assertiva deve ser comentada na correção. Associação somente quando a classificação tiver valor jurídico real.

Formalizar três desenhos de alternativas: soluções diferentes; variação controlada de duas dimensões jurídicas; mesma conclusão com fundamentos diferentes. O núcleo, os fatos, as âncoras e os vícios continuam rastreáveis. Não impor variedade a toda sessão curta nem fixar proporção de formatos sem corpus. As strings atuais de enunciado e alternativas comportam esses formatos; não criar migration apenas para armazenar um rótulo de formato.

### B3. Auditor de blocos

Criar auditor somente leitura de Markdown e JSON de questões. Validar unicidade A–E, IDs de questões, gabarito compatível e não contraditório, vazamento textual de solução e formatos suportados. Arquivo sem questões, formato não interpretável ou gabarito incompleto não recebe aprovação global.

Calcular distribuições de letras e formatos, extensão das alternativas e frequência de termos absolutos, com denominador e tamanho de amostra. Separar erros estruturais, avisos e checagens não executadas. Heurística é alerta editorial, não certificação jurídica. Sequência repetida ou alternativa longa não invalida questão automaticamente. Não reordenar escolhas sem atualizar chave e análise dos distratores.

A auditoria de gabarito ocorre em arquivo privado de autoria/avaliação, nunca no texto entregue ao candidato antes da tentativa. Nenhuma saída pessoal integra o repositório por padrão.

### B4. Calibração por provas reais e dificuldade

Definir registro de corpus com edição, tipo, fonte oficial, data, hash e gabarito definitivo. Registrar por questão formato, fonte do ponto cobrado, disciplina e revisão identificada da classificação. Dificuldade é estimativa editorial identificada, não propriedade oficial da prova; não inferir estatística de acertos sem dados.

Usar somente entradas verificadas para calcular perfil do corpus. Sem corpus suficiente, informar ausência de calibração empírica e seguir critérios jurídicos qualitativos. Treino mantém aprofundamento; simulado busca variedade de demandas cognitivas sustentada pela referência escolhida. Variedade não afasta a unicidade do gabarito, a plausibilidade dos distratores ou as diretrizes atuais de alta complexidade.

Não reduzir o padrão permanente por disciplina, nem copiar a regra do Claude de correção abreviada após acerto. Se um corpus sugerir mudança incompatível com AGENTS, apresentar a divergência para decisão explícita, em vez de flexibilizar silenciosamente.

## Evidência e homologação

Os testes atuais demonstram contratos e comportamentos, não superioridade jurídica. Comparar a versão base e a candidata no mesmo modelo/cliente, com o mesmo material, em três sessões limpas por cenário. Não confundir comparação de instruções com comparação entre modelos. Aplicar rubrica somente após capturar saída; exigir revisão humana identificada, hashes do caso/saída e registro de falhas.

Homologar: chat textual sem MCP; Codex com MCP; ChatGPT conectado somente ao MCP; ChatGPT com card. Confirmar busca oficial e leitura de anexo em cenários próprios; elas não são fornecidas pelo servidor do plugin. Registrar indisponibilidade do host como limitação, sem substituir por teste simulado.

## Extensões futuras condicionais

MCP Events fica fora da primeira entrega: requer ambiente compatível, armazenamento de assinaturas, webhook autenticado, revogação, replay/deduplicação e política de conteúdo transmitido. Avaliar posteriormente apenas para evento mínimo de alteração do índice, com opt-in e sem conteúdo do acervo. Não anunciar monitoramento de STF/STJ: não existe coletor que o sustente.

Upload/seleção de arquivo dentro do card permanece para demanda comprovada. Anexos diretos no chat continuam suficientes para estudo; incluir upload no widget não produz automaticamente ingestão, OCR ou índice. Fullscreen foi antecipado e integra A4.

## Referências oficiais consultadas

- [Changelog de plugins](https://developers.openai.com/plugins/changelog): instruções gerais, visibilidade, tema e lifecycle.
- [UI MCP](https://developers.openai.com/plugins/build/chatgpt-ui): bridge, mensagens e separação de estado.
- [Referência de apresentação](https://developers.openai.com/plugins/reference): requestDisplayMode e modo efetivo do host.
- [MCP Events](https://developers.openai.com/plugins/build/mcp-events): capacidades e restrições da extensão futura.

Confirmar APIs e disponibilidade novamente antes da implementação e antes da homologação; a documentação atual não prova habilitação na conta do usuário.
