# Protocolo de comparação de materiais do ENAM

## Escopo e fontes

A unidade de comparação é o tema ou subtema, e não o número do PDF. Antes de comparar, delimite as edições, a disciplina, os pontos e os documentos efetivamente publicados. Não amplie a varredura para matérias fora do recorte autorizado nem registre como pendente conteúdo de edição posterior que não pertença ao tema solicitado.

Hierarquia das fontes: edital e retificações oficiais; materiais originais identificados de cada edição; quadros editoriais expressos; e, por último, inferência temática claramente rotulada como tal. Uma fonte secundária não se converte em fonte oficial pela repetição ou pela conveniência da comparação.

## Mapeamento de correspondências

Faça busca ampla nos documentos potencialmente pertinentes e escolha, ao final, o menor conjunto de correspondentes principais capaz de cobrir o núcleo temático. Menções laterais, aplicações ou exemplos em outro contexto são referências auxiliares; não tornam a relação automaticamente muitos-para-um.

Admite-se correspondência um-para-um, um-para-muitos, muitos-para-um, divisão, condensação ou deslocamento entre pontos, disciplinas e módulos. Classifique-a como **correspondência editorial expressa**, **deslocamento editorial expresso**, **correspondência temática confirmada**, **correspondência parcial**, **correspondência temática provável** ou **correspondência não confirmada**.

Os qualificadores “expressa” exigem prova documental direta. A correspondência temática confirmada exige equivalência central demonstrada pela leitura dos materiais. A provável registra coincidência relevante com lacuna documental; a não confirmada impede conclusão material. Para cada relação, registre documento, página, seção ou subtítulo e localização identificável do trecho.

## Deltas juridicamente relevantes

Reconheça delta apenas quando houver evidência textual suficiente de atualização legislativa, atualização jurisprudencial, alteração doutrinária material, correção de conteúdo, inclusão material ou exclusão material confirmada. A ordem de prevalência é: atualização legislativa; atualização jurisprudencial; alteração doutrinária material; correção de conteúdo; inclusão material; exclusão material confirmada.

Não constituem delta, isoladamente: mudança de título, ordem, numeração, diagramação, divisão, fusão, condensação, redação, local de estudo, disciplina editorial, exemplo ou citação quando a tese jurídica permanecer. Precedente novo que apenas repete tese já estudada tampouco basta; precedente novo com aplicação relevante e ausente do material anterior pode configurar atualização jurisprudencial.

Use “supressão aparente — revisão humana” se houver indício de retirada sem prova suficiente. A categoria “exclusão material confirmada” só é cabível quando o material anterior contém claramente o conteúdo, a unidade posterior está integralmente publicada, deslocamento e condensação foram afastados e a ausência representa efetiva retirada jurídica demonstrada nas duas versões.

Toda classificação comparativa, exceto “pendente de publicação”, exige referências identificáveis nas versões anterior e atual. Para inclusão material, a referência anterior deve demonstrar a cobertura da unidade em que a ausência foi verificada; para exclusão, a referência atual deve demonstrar a cobertura da unidade posterior. Atualização legislativa ou jurisprudencial exige `fundamento_material` com o tipo correspondente, o identificador da lei ou precedente e a fonte oficial. Esse fundamento explica a causa jurídica da atualização; as referências bilaterais demonstram sua incorporação ou ausência nos materiais comparados.

## Entrega e auditoria

Cada linha do comparativo deve indicar `acao_recomendada`: `INCLUIR` para inclusão material; `SUBSTITUIR` para atualização, correção, alteração doutrinária ou exclusão confirmada; `REVISAR` para supressão aparente ou ambiguidade; `AGUARDAR_PUBLICACAO` para pendência; e `SEM_ACAO` quando não houver delta. A resposta final segue `formato-entrega-comparativo.md` e não fixa datas ou ciclos de revisão.

A tabela final deve conter disciplina, tema/subtema, referências das duas versões, tipo de correspondência, classificação, delta real, fonte/página e observação curta quando necessária. Sem delta, use uma linha compacta por unidade. Quando houver alterações materiais autônomas, use uma linha por alteração, sem fragmentação artificial.

Nos fluxos estruturados, registre o universo documental no manifesto, o mapeamento e o comparativo nos modelos da skill. Use o mesmo `id_execucao` nos três artefatos. Atribua a cada item do mapeamento um `id_item` estável e repita-o em cada delta do comparativo que dele decorrer, preservando disciplina, tema/subtema e tipo de correspondência. Todo item mapeado deve receber ao menos uma linha comparativa, inclusive quando a classificação for “sem delta”; essa classificação é exclusiva para o item, enquanto múltiplas linhas só são admitidas para deltas materiais distintos. Execute a auditoria antes da entrega. A auditoria verifica campos, cobertura e rastreabilidade; ela não substitui leitura, comparação jurídica ou juízo editorial.
