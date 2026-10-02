# Questões interativas pelo MCP

Este arquivo define somente a orquestração técnica. A substância continua regida pela trava canônica de `skills/estudar-direito-magistratura/references/questoes-fgv-enam.md`: caso concreto funcional, cinco alternativas, gabarito único e análise integral dos quatro distratores.

## Fluxo preferencial

Quando MCP Apps estiver disponível, a skill deve: buscar opcionalmente o recorte do acervo local; verificar fontes atuais conforme a política; gerar internamente a questão privada completa; chamar `criar_sessao_questao`; chamar `renderizar_questao`; aguardar a tentativa; e chamar `responder_questao`. Não substitua silenciosamente essas chamadas por uma questão em texto nem presuma que a ferramenta está indisponível sem tentar chamá-la. A criação e a renderização recebem apenas a projeção pública. Correção, gabarito e distratores permanecem no servidor até a primeira tentativa válida.

A questão é gerada dinamicamente pelo modelo; o MCP valida, persiste e projeta os dados, mas não substitui o juízo jurídico da skill. Se a verificação atual for materialmente incompleta, use `source_status: caution` e inclua aviso explícito de cuidado.

Novas sessões prontas exigem análise de exatamente quatro distratores distintos, sem incluir a alternativa correta; `verified` exige ao menos uma referência rastreável. Essa validação técnica não certifica que a fonte sustenta a conclusão jurídica. O card apresenta fontes, exceções e armadilhas na correção, após a tentativa.

Se a auditoria jurídica detectar questão ambígua ou defeituosa, chame `invalidar_questao(session_id, motivo)`, inclusive após a resposta. Explique o motivo, sem defender artificialmente o gabarito. A invalidação preserva a questão e a tentativa originais e retira seus efeitos do perfil e dos relatórios reconstruídos com o log completo. Repetir a chamada com o mesmo motivo é seguro e reconcilia eventual falha parcial de gravação; outro motivo não substitui silenciosamente o anterior.

Eventos MCP novos usam `schema_version: 2.1.0`: registram acerto/erro, mas deixam `error_types` e `domain_evidence` vazios, assistência `nao_registrada` e omitem `source_version` desconhecida. Eventos antigos são preservados, sem migração automática ou reclassificação retroativa.

O widget usa o SDK MCP Apps para inicialização e chamadas correlacionadas, com suporte adicional ao bridge `window.openai`. Uma chamada pendente bloqueia nova submissão; falha de conexão ou resposta é exibida sem inventar resultado. Testes de transporte local não substituem homologação visual no host.

## Fallback

Sem MCP Apps, ou depois de uma chamada retornar erro explícito de indisponibilidade do servidor ou da interface, use fallback textual: informe brevemente a falha, envie apenas enunciado e alternativas, aguarde a resposta e só então apresente a correção canônica. O fallback textual não antecipa o gabarito, não simula persistência e não pode ser acionado apenas por suposição.
