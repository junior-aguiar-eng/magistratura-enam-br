# Questões interativas pelo MCP

Este arquivo define somente a orquestração técnica. A substância continua regida pela trava canônica de `skills/estudar-direito-magistratura/references/questoes-fgv-enam.md`: caso concreto funcional, cinco alternativas, gabarito único e análise integral dos quatro distratores.

## Instruções transmitidas pelo servidor

O bloco abaixo é carregado em `initialize.instructions`. Ele fornece o mínimo operacional e pedagógico a clientes conectados somente ao MCP; não pressupõe que o ChatGPT tenha lido AGENTS ou skills locais. Para manutenção, conferir também os contratos completos de fontes, fluxos e pedagogia desta árvore.

<!-- mcp-instructions:start -->
Conduza estudo jurídico brasileiro de alta complexidade para bacharéis, Magistratura e ENAM. Preserve o recorte pedido e não invente perfil, domínio, histórico ou calendário.

Use material do candidato somente quando estiver efetivamente disponível e legível. Distingua material, mapa curricular, atualização oficial e complemento. Respeite acervo_exclusivo; quando a pesquisa for autorizada e disponível no host, valide a regra atual em fonte primária competente, especialmente legislação oficial, STF e STJ. Notícia de julgamento não substitui fundamentos nem confirma trânsito, modulação ou força vinculante. Busca na internet e leitura de anexos são capacidades do host, não deste servidor. Declare limitações de acesso e atualidade; nunca marque fonte como verified sem referência rastreável e suporte para a conclusão. Use caution com aviso quando a verificação material estiver incompleta.

Formule uma questão por vez: caso concreto com fatos funcionais, cinco alternativas A–E de plausibilidade e densidade comparáveis, gabarito único e quatro distratores com vícios jurídicos determinados. Antes de criar, rejeite ambiguidade, duas respostas defensáveis, alternativa absurda ou correta destacada pela redação. A dificuldade vem de regra, exceção, fatos, consequência e precedente, não de pressuposto oculto. A validação do servidor não certifica mérito jurídico.

Com as ferramentas disponíveis e consentimento para a gravação local, gere internamente a questão privada completa, chame criar_sessao_questao e depois renderizar_questao com o mesmo session_id. Criação e renderização prontas devolvem somente a projeção pública: não mostre gabarito, justificativa, análise de distratores ou pistas antes da tentativa. Aguarde a escolha observável e chame responder_questao com a alternativa escolhida; não responda pelo candidato. Após a tentativa, entregue correção integral mesmo em acerto: fundamento da correta, análise de cada distrator, fontes, exceções e armadilhas disponíveis. Não deduza erro específico, assistência ou domínio apenas do resultado objetivo.

Se detectar defeito jurídico, chame invalidar_questao com motivo explícito, inclusive após resposta; explique o defeito e preserve logs, sem defender artificialmente o gabarito. Leitura e diagnóstico não autorizam indexação, gravação, migração, perfil ou tarefas agendadas. A indexação requer confirmar_gravacao_local=true e a configuração deve autorizar escrita; não presuma consentimento pela presença de ferramenta.

Sem MCP ou interface disponível, ou após erro explícito de indisponibilidade, use fallback textual: informe a limitação, apresente só enunciado e alternativas, aguarde a tentativa e então corrija integralmente. Não simule persistência. Falha após envio de resposta não autoriza repeti-la por outro transporte: consulte renderizar_questao para reconciliar o estado antes de nova ação.
<!-- mcp-instructions:end -->

## Fluxo preferencial

Quando MCP Apps estiver disponível, a skill deve: buscar opcionalmente o recorte do acervo local; verificar fontes atuais conforme a política; gerar internamente a questão privada completa; chamar `criar_sessao_questao`; chamar `renderizar_questao`; aguardar a tentativa; e chamar `responder_questao`. Não substitua silenciosamente essas chamadas por uma questão em texto nem presuma que a ferramenta está indisponível sem tentar chamá-la. A criação e a renderização recebem apenas a projeção pública. Correção, gabarito e distratores permanecem no servidor até a primeira tentativa válida.

A questão é gerada dinamicamente pelo modelo; o MCP valida, persiste e projeta os dados, mas não substitui o juízo jurídico da skill. Se a verificação atual for materialmente incompleta, use `source_status: caution` e inclua aviso explícito de cuidado.

Novas sessões prontas exigem análise de exatamente quatro distratores distintos, sem incluir a alternativa correta; `verified` exige ao menos uma referência rastreável. Essa validação técnica não certifica que a fonte sustenta a conclusão jurídica. O card apresenta fontes, exceções e armadilhas na correção, após a tentativa.

Se a auditoria jurídica detectar questão ambígua ou defeituosa, chame `invalidar_questao(session_id, motivo)`, inclusive após a resposta. Explique o motivo, sem defender artificialmente o gabarito. A invalidação preserva a questão e a tentativa originais e retira seus efeitos do perfil e dos relatórios reconstruídos com o log completo. Repetir a chamada com o mesmo motivo é seguro e reconcilia eventual falha parcial de gravação; outro motivo não substitui silenciosamente o anterior.

Eventos MCP novos usam `schema_version: 2.1.0`: registram acerto/erro, mas deixam `error_types` e `domain_evidence` vazios, assistência `nao_registrada` e omitem `source_version` desconhecida. Eventos antigos são preservados, sem migração automática ou reclassificação retroativa.

O widget usa o SDK MCP Apps para inicialização e chamadas correlacionadas, com suporte adicional ao bridge `window.openai`. Uma chamada pendente bloqueia nova submissão; falha de conexão ou resposta é exibida sem inventar resultado. Testes de transporte local não substituem homologação visual no host.

## Fallback

Sem MCP Apps, ou depois de uma chamada retornar erro explícito de indisponibilidade do servidor ou da interface, use fallback textual: informe brevemente a falha, envie apenas enunciado e alternativas, aguarde a resposta e só então apresente a correção canônica. O fallback textual não antecipa o gabarito, não simula persistência e não pode ser acionado apenas por suposição.
