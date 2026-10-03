# Corpus e calibração de simulado

Estado nesta implementação: **mecanismo local validado por testes; perfil empírico pendente**. Nenhuma prova oficial foi coletada, nenhum corpus real foi selecionado pelo candidato e nenhuma classificação recebeu aprovação jurídica humana nesta task. As fixtures dos testes são inteiramente sintéticas, incluindo URLs inexistentes, hashes e revisores fictícios. Seus números não são estatísticas da FGV/ENAM.

## Registro por edição e caderno

O [schema executável](../../../modelos/pedagogia/exam-corpus.schema.json) recebe um registro por edição/caderno. Use `corpus_id` distinto para cada caderno ou versão; não misture versões de prova/gabarito nem conte cadernos equivalentes duas vezes. A implementação não agrega automaticamente várias edições.

| Campo | Contrato |
| --- | --- |
| `schema_version`, `corpus_id` | Versão `1.0.0` e identidade rastreável do caderno. |
| `evidence_kind` | `official` para registro documental declarado oficial; `synthetic` para fixture/teste. Nenhuma contagem converte fixture em referência empírica. |
| `edition`, `exam_type`, `date` | Edição/caderno identificáveis, `enam` ou `magistratura`, e data da prova. |
| `expected_questions` | Total do caderno conferido no documento, sem preencher total fictício. |
| `official_source` | `url`, `sha256` dos bytes originais e `accessed_at`. |
| `document_review` | Conferência documental identificada: `reviewer`, `date`, `note`. |
| `answer_key` | `status`: `definitivo`, `provisorio` ou `ausente`. Definitivo exige `url` e `sha256` próprios; registre resultado final após recursos. |
| `questions` | Apenas ID, situação oficial e revisões de classificação; nenhum enunciado, alternativa, letra de chave ou resposta pessoal. |

URLs documentais devem usar HTTPS sem credenciais, em domínio `.jus.br`, `.gov.br` ou `conhecimento.fgv.br`. Essa lista fechada é uma verificação de origem admitida; não consulta o endereço, não prova autoria do arquivo e não declara verdadeiro o hash. Nova banca fora da lista exige alteração explícita do contrato, sem aceitar silenciosamente um blog como fonte oficial.

Cada questão possui `id`, `status` (`valida`, `anulada`, `pendente`) e `reviews`. Cada revisão registra `id`, `reviewer`, `date`, `note`, `format` (`direto`, `numerado`, `vf`, `associacao`), `discipline` e `point_source` (`type` e `reference`, com URL opcional). Formato, disciplina ou fonte ainda não definidos usam `null`; revisão ausente usa lista vazia, sem inventar revisor. `point_source.type` distingue legislação, jurisprudência, doutrina, material e outro; não transforma a classificação em autoridade jurídica atual.

`difficulty` é opcional ou `null`; quando presente, exige `label` (`baixa`, `media`, `alta`), `author` e `method`. O autor descreve o critério editorial empregado, como recuperação da regra, aplicação, distinção de exceções ou articulação entre consequências. O script não estima dificuldade por extensão, duração ou disciplina e não calcula taxa de acerto sem dados de desempenho. Classificação editorial não substitui revisão do mérito jurídico.

Todas as revisões permanecem no registro. Divergências de formato, disciplina, fonte ou estimativa/método de dificuldade excluem o item até uma `resolution` identificada, com `selected_review_id`, `reviewer`, `date` e `note`. A resolução seleciona uma revisão existente, não cria uma média, e não pode ser anterior às revisões. Retifique uma classificação por nova revisão e resolução, sem apagar a divergência histórica. Duas revisões concordantes não dispensam conferência documental.

## Elegibilidade, cobertura e perfil

`validate_corpus(corpus)` valida schema, datas, domínio documental admitido, duplicatas, total declarado e resolução. IDs e hashes exigem fim real da string; espaços/quebras de linha não são normalizados, e SHA-256 tem exatamente 64 caracteres hexadecimais minúsculos. Erro de contrato, origem ausente, hash ausente, revisão documental ausente ou gabarito definitivo sem referência/hash impede a geração do perfil. Campos inesperados, inclusive resposta pessoal, são recusados.

`build_calibration_profile(corpus)` separa cadastro válido de item elegível. Gabarito provisório/ausente exclui todos os itens das distribuições. Questão anulada/pendente, revisão ausente, classificação incompleta e divergência sem resolução também são exclusões. Todos os motivos constam em `exclusions`; um item pode ter vários motivos, sem dupla contagem na quantidade excluída.

`coverage` informa `expected`, `registered`, `reviewed`, `eligible`, `excluded` e `missing`. `reviewed` conta classificações completas e resolvidas, inclusive de item anulado; `eligible` acrescenta situação válida e gabarito definitivo. Questões ainda não cadastradas ficam em `missing`, sem IDs inventados. Cada distribuição informa numerador (`sample_size`), denominador e contagens; dificuldade usa somente itens elegíveis com estimativa, e sua ausência não é convertida em baixa dificuldade.

O perfil incorpora origem/edição/tipo, hashes documentais, declaração de revisão, hash SHA-256 da serialização JSON canônica do registro e o próprio corpus de metadados/classificações. `validate_calibration_profile(profile)` recalcula todo o perfil dessa evidência antes do uso; contagens/hash/status divergentes são recusados. Isso detecta inconsistência interna, não assinatura/autenticidade: adulterar conjuntamente evidência e perfil exige conferência externa do documento.

| Estado | Significado |
| --- | --- |
| `sem_calibracao` | Nenhum item elegível; distribuições vazias, sem referência utilizável. |
| `parcial` | Há itens elegíveis, mas o total do caderno não está integralmente elegível. |
| `descritivo` | Todos os itens declarados estão elegíveis segundo o registro; não é aprovação jurídica ou prova de representatividade. |

`empirical_reference_available` significa apenas registro **declarado oficial** com ao menos um item elegível, para comparação descritiva do subconjunto. `verification_basis` permanece `declared_document_review`; os bytes não são verificados por essa CLI. Amostra menor que oito recebe aviso editorial de cautela, nunca certificado de suficiência acima desse limiar. `not_checked` preserva autenticidade dos bytes, mérito jurídico, representatividade, natureza não oficial da dificuldade e ausência de medição de acertos. Uma única edição não demonstra padrão histórico da banca.

## Execução por leitura

A partir da raiz canônica `plugins/magistratura-enam-br`:

```powershell
uv run python scripts/calibrar_provas.py --corpus CAMINHO_DO_REGISTRO.json
uv run python scripts/auditar_questoes.py --questoes BLOCO.md --formato markdown --perfil PERFIL.json
```

O primeiro comando imprime perfil no stdout. Não cria arquivo de saída, coleta documento, indexa biblioteca, registra tentativa nem modifica entradas. UTF-8 com BOM é aceito; JSON duplicado/não finito e arquivos ilegíveis são recusados, com erro JSON sem eco do conteúdo. Exit code 2 indica entrada inválida; 0 inclui perfil sem calibração ou parcial, portanto consulte `status` e cobertura. Salvar stdout em destino exige autorização correspondente; o exemplo não presume gravação.

O auditor reconhece `kind: "exam_calibration_profile"` e recalcula o perfil. Se declarado oficial/elegível e o bloco não tiver erro estrutural, compara frações de formatos, com hash de referência e tamanhos de ambas as amostras. Deltas são descritivos; não reordenam opções, geram questões ou impõem quota. Perfil reconhecido inconsistente é erro; dict arbitrário continua `profile_not_validated`; fixture ou referência sem elegibilidade continua `profile_not_empirical`. A falta de gabarito no bloco mantém `checagem_parcial` mesmo com comparação de formatos. O auditor não conhece disciplina/fonte/dificuldade do bloco apenas por seu formato.

Use o perfil somente quando fornecido ou disponível na sessão e escolhido pelo candidato. Simulado pode variar demandas cognitivas conforme essa referência e o recorte; treino preserva alta complexidade e correção integral. A divisão 75/25 do Claude não é estatística/default do plugin. Nenhuma comparação dispensa unicidade da chave, plausibilidade dos distratores ou âncoras jurídicas. Divergência com AGENTS deve ser apresentada para decisão expressa do criador, sem reduzir silenciosamente o padrão.

Perfis são artefatos de autoria/classificação, não de desempenho pessoal. Relatórios do auditor com chave continuam privados e separados da apresentação pré-tentativa. Não versione registros pessoais por padrão.

## Coleta oficial como etapa própria

1. Selecionar com o candidato edição/caderno e finalidade; localizar prova e gabarito definitivo nas fontes competentes.
2. Conferir URLs, bytes e SHA-256 de cada documento, data, edição, variante do caderno e resultado final após recursos; identificar o responsável pela conferência.
3. Cadastrar todos os IDs/situações e classificar formato, disciplina e fonte do ponto, com revisor/data/nota. Registrar anuladas e ausência de revisão sem transformar pendência em validação.
4. Preservar divergências; obter resolução identificada antes de incluir o item. Se estimar dificuldade, identificar autor e método, sem inferir estatística de acertos.
5. Gerar perfil, revisar cobertura/exclusões e rotulagem; se publicar evidência, versionar apenas metadados/classificações autorizados, sem republicar caderno completo, gabarito pessoal ou conteúdo protegido.

Sem corpus selecionado e verificado, a entrega é o mecanismo e a declaração **perfil empírico pendente**. Não existe corpus padrão, coletor automático, números oficiais preenchidos ou aprovação humana implícita neste diretório.

## Validação e amostra rotulada

As fixtures de `tests/test_calibrar_provas.py` verificam manualmente as contagens esperadas e exclusões para itens diretos, V/F, anulados, sem revisão e revisões divergentes/resolvidas, além de CLI somente leitura e consumo pelo auditor. Essa amostra rotulada é sintética e não prova fidelidade ao ENAM. Os cenários `calibracao-*` no catálogo exercitam gabarito provisório, conflito e subconjunto pequeno; a rubrica é aplicada depois da resposta. Revisão jurídica humana e homologação em clientes reais continuam pendentes.

O controle anterior já rejeitou 75/25 como frequência empírica e reconheceu o limite do corpus sintético. Sua saída declarou não conhecer o contrato do auditor e produziu somente um registro descritivo não validado. A candidata adiciona o procedimento executável e a fronteira do perfil; esse contraste não demonstra superioridade jurídica ou estatística entre modelos.

Em 2026-10-03, a avaliação automatizada em sessão nova da candidata reconheceu o registro documental inválido do primeiro cenário, não inventou perfil compatível, manteve zero elegíveis sob gabarito provisório, preservou divergência sem média/última revisão e recusou aprovação do bloco/perfil indisponível. As três respostas foram avaliadas após emissão. O controle tem uma resposta, a candidata tem três cenários na mesma sessão; não é benchmark com três repetições, modelo interno identificado ou clientes reais homologados. Ambas são respostas automatizadas, sem aprovação jurídica humana. Os resultados foram observados nesta conversa, não capturas completas distribuídas ou estatísticas de prova.

Verificações locais iniciais: 47 testes específicos de corpus, 124 de corpus/auditor e 133 incluindo catálogo; suíte completa com 512 testes Python aprovados. Ruff, lockfile e 42 verificações de integração passaram. Os testes de CLI conferem entradas byte a byte e ausência de novos arquivos no destino.

Revisão independente automatizada de `235c4f0..eb4ca69`: nenhum achado crítico ou menor, um importante. IDs/hashes aceitavam quebra de linha final pelo comportamento de `$`, permitindo identidade visual duplicada e hash de tamanho inválido. Oito regressões RED foram corrigidas em uma passagem com fim real de string e comprimento exato; agora 55 testes do corpus, 132 corpus/auditor, 141 com catálogo e suíte completa com 520 Python passaram, além de Ruff/lock/42checks e MkDocs estrito. Sem segunda revisão independente. O revisor reproduziu o defeito em memória e não repetiu os gates gerais; autenticidade documental, revisores reais, representatividade/classificação jurídica e homologação humana/host real permanecem não certificados. O achado menor preexistente de numeração arábica da task6 continua registrado.
