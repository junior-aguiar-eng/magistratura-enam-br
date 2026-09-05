---
name: comparar-materiais-enam
description: Compare materiais publicados do ENAM por capítulo, tema e subtema para identificar mudanças juridicamente relevantes entre edições ou versões e orientar a atualização do estudo em tabela. Use quando o usuário fornecer materiais, edital ou retificações e pedir mapeamento, comparação, conferência de atualização ou auditoria de rastreabilidade. Não use para explicar tema isolado, triar informativo ou planejar revisões.
---

# Comparação de materiais do ENAM

## Política de fontes na comparação

Leia `../../references/politica-fontes-juridicas.md` e `../../references/protocolo-uso-do-acervo.md`. Se o escopo for comparar exclusivamente os documentos fornecidos, aplique `acervo_exclusivo`: não introduza pesquisa externa, não complete lacunas e não use conhecimento externo para classificar delta. Aponte o que os documentos permitem ou não concluir.

Em `acervo_com_validacao_oficial`, valide externamente apenas alteração legislativa ou jurisprudencial material que dependa de confirmação atual. Em `pesquisa_juridica_completa`, consulte primeiro a fonte oficial competente antes de atribuir causa jurídica a uma diferença; fonte editorial cadastrada é apenas apoio secundário. Só transite entre políticas quando o candidato alterar efetivamente o universo de fontes.

Quando houver consulta externa relevante, apresente as fontes decisivas em `Base consultada`, sem manchetes, cards, URLs brutas no corpo ou lista de resultados. Identifique expressamente qualquer fonte secundária por sua natureza editorial.

## Diretriz obrigatória do plugin

Na abertura de nova comparação, leia e cumpra integralmente `../../AGENTS.md`. Suas diretrizes prevalecem sobre preferências genéricas de formato, concisão ou simplificação. Em continuidade do mesmo par documental e escopo, reaproveite essa leitura e releia apenas se houver nova versão, mudança de escopo ou dúvida real de fonte.

A entrega deve distinguir ausência aparente, mudança editorial e alteração jurídica antes de recomendar a ação de estudo. Preserve os originais e permita retorno da conclusão à localização documental que a sustenta.

Na abertura de nova comparação com documentos do candidato, leia `../../references/protocolo-uso-do-acervo.md` antes de classificá-los. Mantenha a classificação no contexto da comparação; não a refaça a cada mensagem sem novo documento.

## Objetivo

Compare materiais delimitados pelo usuário para identificar mudanças jurídicas reais e sua utilidade para atualização do estudo, sem confundir alteração editorial, numeração ou diagramação com atualização do Direito brasileiro. A entrega padrão é uma tabela didática no chat, não uma sinopse, parecer ou mini-laudo.

## Fluxo

1. Delimite edições, disciplina, pontos e documentos efetivamente publicados que integram a comparação. Verticalizados e análises estratégicas podem esclarecer o escopo, mas não substituem versões originais nem demonstram delta material.
2. Leia `references/protocolo-comparacao-enam.md` antes de mapear correspondências ou classificar deltas de um novo par documental; reaproveite-o nas etapas posteriores da mesma comparação.
3. Use edital e retificações oficiais como referência prioritária; depois, os materiais originais identificados.
4. Compare por capítulo, tema e subtema, mantendo evidência de documento, página e localização para cada conclusão. Para cada unidade, registre o que havia antes, o que há agora, a densidade relativa, eventual supressão ou deslocamento e a consequência concreta para o estudo.
5. Leia `references/formato-entrega-comparativo.md` uma vez antes de apresentar o resultado e entregue a tabela no chat. Para cada delta material, acrescente leitura decisória concisa: o que mudou, por que importa no material de estudo, ação recomendada e grau de certeza documental. Use os modelos em `modelos/` e execute `scripts/auditar_rastreabilidade.py` somente se o usuário pedir auditoria de rastreabilidade, JSON, artefatos estruturados ou arquivo; não crie nem cite arquivos de saída por padrão.
6. Exporte um evento `material_atualizado` somente mediante pedido expresso. Vincule `INCLUIR`, `SUBSTITUIR` ou `REVISAR` ao `content_ref` do delta, sem converter a comparação documental em erro, acerto ou domínio do candidato. Não atribua data, intervalo ou prioridade. Encaminhe explicação à skill de estudo e eventual planejamento somente quando o delta tratar de julgado já presente na esteira.

## Limites

Não conclua exclusão sem demonstração de cobertura integral do material posterior e sem afastar deslocamento editorial. Não trate coincidência lexical como equivalência jurídica, não atribua correspondência editorial sem fonte documental e não preencha lacunas com conhecimento externo.

Cronogramas e planos de remessa de curso não comprovam disponibilidade, versão, alteração, prioridade ou exclusão de conteúdo. Não infira a existência de documento não fornecido, nem converta análise estratégica em prova de mudança jurídica ou editorial.

Consulte `../../references/diretrizes-estudo-juridico-brasileiro.md` antes de classificar delta jurídico, legislativo ou jurisprudencial; não o carregue para conferir alteração meramente editorial e reaproveite a leitura enquanto o conjunto documental permanecer o mesmo.

Trate novo recorte do mesmo par documental como continuidade e não repita ambientação. Se o pedido mudar para explicação jurídica, curadoria ou planejamento, anuncie a mudança em uma frase e devolva a autoridade a `acompanhar-percurso-magistratura`; não execute silenciosamente a outra skill. Aplique `../acompanhar-percurso-magistratura/references/transicoes-inteligentes.md` quando faltar o segundo documento ou houver suspensão, retomada e encerramento. Mudança de assunto não confirma delta, exclusão, tentativa, erro ou abandono. Entre sessões, só retome com estado ou checkpoint fornecido.
