# Política de fontes jurídicas

O candidato escolhe, expressa ou implicitamente pelo pedido, uma das três políticas. A escolha controla a pesquisa; não altera a hierarquia jurídica das fontes.

## Seleção padrão

A escolha expressa sempre prevalece. Sem escolha expressa, material substancial fornecido adota `acervo_com_validacao_oficial`; comparação restrita aos documentos e organização de julgados já selecionados adotam `acervo_exclusivo`; pedido de pesquisa, complementação ampla ou resposta sem acervo cuja atualidade seja material adota `pesquisa_juridica_completa`. Se duas políticas permanecerem plausíveis e puderem mudar o resultado, faça uma única pergunta discriminante, sem transformar a abertura em formulário.

## Modos

### `acervo_exclusivo`

Usa somente o material efetivamente disponível na conversa. Não pesquisa, completa ou corrige silenciosamente com conteúdo externo. Se o núcleo necessário não estiver acessível, informa a limitação e solicita o trecho ou arquivo.

### `acervo_com_validacao_oficial`

Mantém o material do candidato como base pedagógica e consulta apenas fontes primárias registradas para verificar lei, precedente, situação processual ou atualização relevante. Toda divergência é apresentada em camada separada; a fonte oficial prevalece quanto ao estado atual do Direito.

### `pesquisa_juridica_completa`

Admite fontes primárias e secundárias registradas. A pesquisa começa pelas fontes oficiais adequadas. Fontes editoriais servem a contexto, doutrina, análise ou localização, nunca a comprovação isolada de vigência, tese, resultado, modulação, trânsito em julgado ou situação processual.

## Registro fechado

Somente fontes incluídas deliberadamente em `references/fontes-confiaveis.json` podem ser usadas. A expressão “site conceituado” não abre pesquisa indiscriminada. A inclusão de nova fonte exige alteração explícita do registro, classificação, finalidades, domínios canônicos e limitações.

O domínio é validado pelo `hostname` normalizado da URL e por igualdade exata com `canonical_domains`. Correspondência por substring, sufixo não cadastrado, redirecionador, URL de busca ou domínio visualmente semelhante é proibida. Por exemplo, `www.stf.jus.br.evil.example` não corresponde a `www.stf.jus.br`.

Links podem ser fornecidos quando úteis à rastreabilidade, mas a resposta deve organizar o conteúdo para estudo e não assumir aparência de portfólio de notícias.

## Hierarquia

Para geração de questões com complementação externa, siga a ordem operacional: Planalto → STF/STJ → acervo local → fonte jurídica subsidiária. A posição operacional do acervo não reduz sua função pedagógica nem altera a prevalência da fonte oficial sobre o estado atual do Direito.

1. Planalto para texto legal federal consolidado e atos nele publicados.
2. STF e STJ para jurisprudência, informativos e situação processual de sua competência.
3. Dizer o Direito, JOTA e Thomson Reuters / Revista dos Tribunais somente nas finalidades editoriais declaradas no registro.

Notícia institucional não substitui acórdão, tese, legislação ou andamento processual. Fonte secundária nunca confirma isoladamente regra jurídica atual.
