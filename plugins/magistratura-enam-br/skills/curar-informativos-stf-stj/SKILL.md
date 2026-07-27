---
name: curar-informativos-stf-stj
description: Realize curadoria jurisprudencial de informativos do STF e do STJ para Magistratura e ENAM. Use quando o usuário fornecer um ou mais informativos e pedir leitura integral, seleção hierarquizada, comentário técnico ou boletim dos julgados mais relevantes. Não use para explicar julgado isolado, comparar materiais do ENAM ou montar calendário de revisão.
---

# Curadoria de informativos STF/STJ

## Objetivo

Selecionar, dentre os julgados de um informativo, aqueles que efetivamente merecem estudo aprofundado para a Magistratura. O resultado deve ser um boletim jurídico conciso e denso, não um resumo integral do informativo nem um capítulo de manual.

## Método

1. Leia integralmente o informativo e registre limitações materiais que impeçam compreensão segura.
2. Compare os julgados entre si, considerando relevância constitucional ou infraconstitucional, inovação, repercussão geral, repetitivos, IAC, IRDR, súmulas, impacto prático e aderência ao ENAM.
3. Selecione, em regra, até dez julgados em ordem decrescente de relevância. Se não houver dez relevantes, não complete artificialmente. Se o informativo for excepcionalmente denso, ultrapasse dez apenas quando for estritamente necessário para não excluir decisão essencial.
4. Consulte fontes oficiais quando o informativo não bastar para precisar a tese, o alcance, a modulação, a pendência ou a evolução posterior.
5. Separe STF e STJ e apresente, para cada selecionado, identificação, controvérsia, fundamentos determinantes, alcance e relevância para a Magistratura.

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
