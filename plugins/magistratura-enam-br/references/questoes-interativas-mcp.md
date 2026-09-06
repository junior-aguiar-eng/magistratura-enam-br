# Questões interativas pelo MCP

Este arquivo define somente a orquestração técnica. A substância continua regida pela trava canônica de `skills/estudar-direito-magistratura/references/questoes-fgv-enam.md`: caso concreto funcional, cinco alternativas, gabarito único e análise integral dos quatro distratores.

## Fluxo preferencial

Quando MCP Apps estiver disponível, a skill deve: buscar opcionalmente o recorte do acervo local; verificar fontes atuais conforme a política; gerar internamente a questão privada completa; chamar `criar_sessao_questao`; chamar `renderizar_questao`; aguardar a tentativa; e chamar `responder_questao`. Não substitua silenciosamente essas chamadas por uma questão em texto nem presuma que a ferramenta está indisponível sem tentar chamá-la. A criação e a renderização recebem apenas a projeção pública. Correção, gabarito e distratores permanecem no servidor até a primeira tentativa válida.

A questão é gerada dinamicamente pelo modelo; o MCP valida, persiste e projeta os dados, mas não substitui o juízo jurídico da skill. Se a verificação atual for materialmente incompleta, use `source_status: caution` e inclua aviso explícito de cuidado.

## Fallback

Sem MCP Apps, ou depois de uma chamada retornar erro explícito de indisponibilidade do servidor ou da interface, use fallback textual: informe brevemente a falha, envie apenas enunciado e alternativas, aguarde a resposta e só então apresente a correção canônica. O fallback textual não antecipa o gabarito, não simula persistência e não pode ser acionado apenas por suposição.
