---
name: curar-informativos-stf-stj
description: Realize curadoria jurisprudencial de informativos do STF e do STJ para Magistratura e ENAM. Use quando o usuário fornecer um ou mais informativos e pedir leitura integral, seleção hierarquizada, comentário técnico ou boletim dos julgados mais relevantes. Não use para explicar julgado isolado, comparar materiais do ENAM ou montar calendário de revisão.
---

# Curadoria de informativos STF/STJ

## Objetivo

Selecionar, dentre os julgados de um informativo, aqueles que efetivamente merecem estudo aprofundado para a Magistratura. O resultado deve ser um boletim jurídico conciso e denso, não um resumo integral do informativo nem um capítulo de manual.

Antes de interpretar o pedido ou escolher o modo de atuação, leia e cumpra integralmente `../../AGENTS.md`. Suas diretrizes prevalecem sobre preferências genéricas de formato, concisão ou simplificação.

## Método

1. Leia integralmente o informativo e registre limitações materiais que impeçam compreensão segura.
2. Compare os julgados entre si, considerando relevância constitucional ou infraconstitucional, inovação, repercussão geral, repetitivos, IAC, IRDR, súmulas, impacto prático e aderência ao ENAM.
3. Selecione, em regra, até dez julgados em ordem decrescente de relevância. Se não houver dez relevantes, não complete artificialmente. Se o informativo for excepcionalmente denso, ultrapasse dez apenas quando for estritamente necessário para não excluir decisão essencial.
4. Consulte fontes oficiais quando o informativo não bastar para precisar a tese, o alcance, a modulação, a pendência ou a evolução posterior.
5. Separe STF e STJ e aplique, sem exceção, o padrão de entrega obrigatória abaixo a cada julgado selecionado.

## Padrão de entrega obrigatório

Não entregue sinopses temáticas, tópicos telegráficos, ementas reescritas ou um único parágrafo conclusivo por julgado. Cada precedente selecionado é uma unidade autônoma de estudo e deve conter, nesta ordem:

1. **Cabeçalho técnico completo:** classe, número, unidade federativa quando houver e título que expresse a controvérsia decidida; em seguida, órgão julgador, relator, redator do acórdão se houver, data e natureza qualificada do precedente.
2. **Situação precedental:** informe técnica decisória e respectiva força vinculante, com fundamento aplicável; número e texto nuclear de tema de repercussão geral, repetitivo, IAC, IRDR ou súmula, se existentes; estado processual, trânsito em julgado e embargos pendentes; modulação, com termo inicial e alcance subjetivo e material, ou a sua inexistência; e relação precisa com a jurisprudência anterior — reafirmação, distinção, restrição, esclarecimento ou superação. Registre expressamente quando qualquer desses elementos não estiver presente ou não puder ser confirmado em fonte oficial.
3. **Tese em destaque:** use **Tese:** para núcleo de formulação oficial fiel; na sua falta, use **Síntese da tese:** e identifique expressamente a formulação como editorial.
4. **Quatro parágrafos analíticos autônomos:** (a) controvérsia e contexto necessário; (b) base normativa e fundamentos determinantes, com reconstrução da ratio; (c) aplicação, alcance e limites; e (d) consequência prática e chave de leitura para a Magistratura.

Em julgados estruturantes, desenvolva os quatro parágrafos com a extensão necessária para explicar o caminho decisório. Não reduza nenhum deles a uma ou duas frases. A densidade decorre da reconstrução da razão de decidir e de suas fronteiras, não da multiplicação de tópicos ou da transcrição de ementas. Leia `references/comentario-jurisprudencial.md` integralmente antes de redigir.

## Direito brasileiro e fontes

Parta da Constituição, da legislação oficial e da jurisprudência dos tribunais competentes. Em precedentes, dê relevo às teses fixadas, aos fundamentos determinantes e aos limites de incidência à luz do sistema brasileiro, especialmente do CPC. Não atribua ao tribunal fundamento ou consequência sem fonte suficiente.

Use `../../references/diretrizes-estudo-juridico-brasileiro.md` antes de redigir. Para o padrão editorial de comentário e de seleção, consulte `references/comentario-jurisprudencial.md` e `references/curadoria-editorial.md`.

## Recursos de apoio

Os recursos desta skill servem a organizacao e a verificacao material do trabalho, sem substituir a leitura integral do informativo nem a avaliacao juridica humana.

- Antes da analise, use `scripts/checar_estrutura_informativo.py` quando for util confirmar a extracao de texto e a legibilidade do PDF. O resultado e apenas diagnostico.
- Gere boletim em PDF somente se o usuario o solicitar, com `scripts/gerar_pdf_boletim.py` e o modelo `modelos/boletim.schema.json`.
- Crie ou atualize a planilha de precedentes somente se isso for pedido, com `scripts/atualizar_planilha_precedentes.py` e o modelo `modelos/precedentes.schema.json`.
- Os modelos registram campos minimos e estados de verificacao; eles nao substituem a tese oficial, o inteiro teor ou a fundamentacao do julgado.
- Execute os testes em `tests/` sempre que os scripts forem alterados ou migrados.

## Limites

Não transforme o boletim em lista de memorização, não atribua frequência de cobrança à FGV sem base objetiva e não trate decisão isolada, cautelar ou pendente como entendimento consolidado.
