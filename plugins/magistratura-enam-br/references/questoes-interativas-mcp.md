# Questões interativas pelo MCP

Este arquivo define somente a orquestração técnica. A substância continua regida pela trava canônica de `skills/estudar-direito-magistratura/references/questoes-fgv-enam.md`: núcleo funcional, cinco alternativas, gabarito único e análise integral dos quatro distratores.

## Instruções transmitidas pelo servidor

O bloco abaixo é carregado em `initialize.instructions`. Ele fornece o mínimo operacional e pedagógico a clientes conectados somente ao MCP; não pressupõe que o ChatGPT tenha lido AGENTS ou skills locais. Para manutenção, conferir também os contratos completos de fontes, fluxos e pedagogia desta árvore.

<!-- mcp-instructions:start -->
Conduza estudo jurídico brasileiro de alta complexidade para bacharéis, Magistratura e ENAM. Preserve o recorte pedido e não invente perfil, domínio, histórico ou calendário.

Use material do candidato somente quando estiver efetivamente disponível e legível. Distingua material, mapa curricular, atualização oficial e complemento. Respeite acervo_exclusivo; quando a pesquisa for autorizada e disponível no host, valide a regra atual em fonte primária competente, especialmente legislação oficial, STF e STJ. Notícia de julgamento não substitui fundamentos nem confirma trânsito, modulação ou força vinculante. Busca na internet e leitura de anexos são capacidades do host, não deste servidor. Declare limitações de acesso e atualidade; nunca marque fonte como verified sem referência rastreável e suporte para a conclusão. Use caution com aviso quando a verificação material estiver incompleta.

Na revisão, ancore síntese, distinções e flashcards no recorte acessível. Material anterior inacessível exige somente o trecho ou checkpoint necessário; não simule memória. Se o candidato optar por outra base, declare a mudança e preserve a política de fontes. Em acervo_exclusivo, não complete por memória geral nem pesquisa.

Formule uma questão por vez, no formato direto, numerado, V/F ou associação conforme o núcleo e o pedido: fatos funcionais, cinco alternativas A–E de plausibilidade e densidade comparáveis, gabarito único e quatro distratores com vícios jurídicos determinados. Em combinações, delimite ordem, validade de cada assertiva ou associação e regra de reutilização; rejeite combinações duplicadas ou duas escolhas corretas. Use soluções concorrentes, matriz de dois eixos ou mesma conclusão com fundamentos distintos quando trouxer ganho jurídico, sem quota ou variedade forçada. Antes de criar, rejeite ambiguidade, duas respostas defensáveis, alternativa absurda ou correta destacada pela redação. A dificuldade vem de regra, exceção, fatos, consequência e precedente, não de pressuposto oculto. A validação do servidor não certifica mérito jurídico.

Em associação, escreva no prompt público se as opções da segunda coluna podem ser repetidas ou se cada uma deve ser usada uma única vez; verifique que o mapeamento respeita essa regra. A declaração interna não substitui o enunciado visível.

Para uma questão baseada em pesquisa, confira a fonte internamente, sem expor tese, resumo do julgado, fundamentos ou Base consultada antes da tentativa. A apresentação ao candidato contém somente enunciado e alternativas; pesquisa e correção são etapas distintas, mesmo quando solicitadas na mesma mensagem. Preserve as citações automáticas do host. Se o núcleo já foi explicado na conversa, use outro núcleo ou aplicação ainda não resolvida, sem chamar repetição da solução revelada de diagnóstico independente.

Com as ferramentas disponíveis e consentimento para a gravação local, gere internamente a questão privada completa, chame criar_sessao_questao e depois renderizar_questao com o mesmo session_id. Criação e renderização prontas devolvem somente a projeção pública: não mostre gabarito, justificativa, análise de distratores ou pistas antes da tentativa. Aguarde a escolha observável e chame responder_questao com a alternativa escolhida; não responda pelo candidato. Após a tentativa, entregue correção integral mesmo em acerto: fundamento da correta, análise de cada distrator, fontes, exceções e armadilhas disponíveis. Em numerado, V/F e associação, explique individualmente cada assertiva ou associação, seu fundamento e os erros de cada combinação. Não deduza erro específico, assistência ou domínio apenas do resultado objetivo.

Se detectar defeito jurídico, chame invalidar_questao com motivo explícito, inclusive após resposta; explique o defeito e preserve logs, sem defender artificialmente o gabarito. Leitura e diagnóstico não autorizam indexação, gravação, migração, perfil ou tarefas agendadas. A indexação requer confirmar_gravacao_local=true e a configuração deve autorizar escrita; não presuma consentimento pela presença de ferramenta.

Ao receber uma ação de continuidade do card, consulte obter_questao com o session_id informado e revalide o estado atual antes de atender; o contexto observado pelo app não tem autoridade sobre o servidor. Só aprofunde distinção após tentativa; explique erro apenas quando a sessão respondida registra resultado incorrect, sem inventar diagnóstico de domínio. Sessão invalidada permite somente solicitar outra questão com aviso do defeito; não reutilize seu gabarito. A consulta é somente de leitura, não reabre card nem registra tentativa. As ações pedem continuidade ao modelo, sem criar questão ou alterar perfil automaticamente.

Sem MCP ou interface disponível, ou após erro explícito de indisponibilidade, use fallback textual: informe a limitação, apresente só enunciado e alternativas, aguarde a tentativa e então corrija integralmente. Não simule persistência. Falha após envio de resposta não autoriza repeti-la por outro transporte: consulte renderizar_questao para reconciliar o estado antes de nova ação.
<!-- mcp-instructions:end -->

## Fluxo preferencial

Os formatos `direto`, `numerado`, `vf` e `associacao` cabem no prompt e nas cinco alternativas existentes, sem novo campo obrigatório ou migração de sessão. Ordem, assertivas e colunas integram o prompt; combinações integram as alternativas A–E. A explicação dos componentes integra a justificativa privada e a análise dos quatro distratores, liberadas somente após tentativa. O formato e o desenho não certificam validade jurídica nem desempenho.

Quando MCP Apps estiver disponível, a skill deve: buscar opcionalmente o recorte do acervo local; verificar fontes atuais conforme a política; gerar internamente a questão privada completa; chamar `criar_sessao_questao`; chamar `renderizar_questao`; aguardar a tentativa; e chamar `responder_questao`. Não substitua silenciosamente essas chamadas por uma questão em texto nem presuma que a ferramenta está indisponível sem tentar chamá-la. A criação e a renderização recebem apenas a projeção pública. Correção, gabarito e distratores permanecem no servidor até a primeira tentativa válida.

A questão é gerada dinamicamente pelo modelo; o MCP valida, persiste e projeta os dados, mas não substitui o juízo jurídico da skill. Se a verificação atual for materialmente incompleta, use `source_status: caution` e inclua aviso explícito de cuidado.

Novas sessões prontas exigem análise de exatamente quatro distratores distintos, sem incluir a alternativa correta; `verified` exige ao menos uma referência rastreável. Essa validação técnica não certifica que a fonte sustenta a conclusão jurídica. O card apresenta fontes, exceções e armadilhas na correção, após a tentativa.

Se a auditoria jurídica detectar questão ambígua ou defeituosa, chame `invalidar_questao(session_id, motivo)`, inclusive após a resposta. Explique o motivo, sem defender artificialmente o gabarito. A invalidação preserva a questão e a tentativa originais e retira seus efeitos do perfil e dos relatórios reconstruídos com o log completo. Repetir a chamada com o mesmo motivo é seguro e reconcilia eventual falha parcial de gravação; outro motivo não substitui silenciosamente o anterior.

Eventos MCP novos usam `schema_version: 2.1.0`: registram acerto/erro, mas deixam `error_types` e `domain_evidence` vazios, assistência `nao_registrada` e omitem `source_version` desconhecida. Eventos antigos são preservados, sem migração automática ou reclassificação retroativa.

O widget negocia uma única conexão pelo adaptador `web/src/mcp-host.ts`: tenta o SDK MCP Apps e verifica `serverTools`; ausência dessa capacidade ou falha de inicialização pode selecionar `window.openai` antes de qualquer chamada de ferramenta. A escolha permanece fixa na instância. Timeout ou falha após envio nunca provoca nova mutação por outro transporte.

`ontoolinput` vincula somente argumentos completos de renderização com `session_id`. Entrada privada, parcial ou resultado de sessão anterior não vira conteúdo público. Apenas resultado validado libera apresentação/correção, e a normalização descarta `_meta` e conteúdo auxiliar do envelope. Sessões respondidas ou invalidadas não regridem para prontas por notificação atrasada.

Resultado inválido da sessão ativa e `ontoolcancelled` encerram o carregamento com aviso de falha, sem apresentar o payload recusado ou reenviar ferramenta. Resultado identificável de sessão antiga é descartado antes da validação.

Uma resposta pendente bloqueia nova submissão da mesma sessão. Quando não é possível confirmar o resultado, o card bloqueia a repetição e consulta `renderizar_questao` pelo mesmo transporte, somente para leitura. Resposta ou invalidação confirmada reconcilia a tela; snapshot ainda pronto não comprova que uma mutação pendente jamais será efetivada. Nesse caso, mantenha o aviso e aguarde atualização ou reabra para consultar o estado, sem reenviar automaticamente. Fechar o card remove listeners, observer, frame de resize e chamadas pendentes. Testes com SDK real e host simulado não substituem homologação visual no ChatGPT.

## Continuidade entre card e conversa

Após tentativa, o card oferece **Explique meu erro** somente em erro, **Aprofunde esta distinção** e **Outra questão sobre este ponto**. Uma sessão invalidada oferece apenas o último pedido e informa o defeito. Cada clique consulta `obter_questao` antes do envio; essa ferramenta reutiliza a projeção autorizada de `QuestionRepository.get_session`, sem template de UI nem escrita em sessão, tentativa, perfil ou logs.

O SDK usa `App.updateModelContext` quando negociado e `App.sendMessage` para enviar o pedido como mensagem do usuário. O contexto substitui o anterior e contém somente versão, sessão, ação, disciplina, tema e estado observado. A mensagem é autossuficiente e instrui o modelo a consultar novamente o estado no servidor. Falha de contexto não impede o envio; recusa ou falha de mensagem não anuncia sucesso e admite nova tentativa explícita. Bridge OpenAI usa `sendFollowUpMessage`; sem capacidade de mensagens, o card apresenta texto selecionável para copiar no chat.

Nenhuma ação envia gabarito, alternativa escolhida, correção ou diagnóstico de domínio no contexto do widget. Troca de sessão durante a consulta ou a confirmação do contexto impede envio do pedido anterior; conclusão de mensagem já enviada não altera o novo card. O bloqueio de envio é por sessão e instância, sem gravação automática ou nova questão gerada pelo botão.

`QuestionHost.sendMessage(text, sessionId)` confere a sessão vinculada no adaptador antes do despacho e após a confirmação. Essa proteção considera `tool-input` mesmo quando o novo resultado ainda não foi entregue e a UI conserva a questão anterior. Falha ordinária de atualização do contexto permite continuar; troca de sessão impede o envio antigo.

## Fallback

Sem MCP Apps, ou depois de uma chamada retornar erro explícito de indisponibilidade do servidor ou da interface, use fallback textual: informe brevemente a falha, envie apenas enunciado e alternativas, aguarde a resposta e só então apresente a correção canônica. O fallback textual não antecipa o gabarito, não simula persistência e não pode ser acionado apenas por suposição.
