# ENAM 2026.1 — Tipo 1: corpus adquirido, revisão pendente

Documentos vinculados pela [página oficial da FGV](https://conhecimento.fgv.br/exames/enam/5exame),
baixados em 2026-10-03. O caderno contém 80 questões; prova em 07/06/2026.
Gabarito definitivo publicado na página em 21/07/2026; item 42 anulado.

| Documento | Bytes | SHA-256 |
|---|---:|---|
| Caderno Tipo 1 | 599159 | `31a6228c7f2ec52358fffb1f6add267ed075ead17d5c3ad37a500d465d084aa4` |
| Gabarito definitivo | 127365 | `81c1cbfbcab8df8d6ba0cd2f1ac2950b16cefe6147ed6490af8799b14dbfbba7` |

`corpus.json` cadastra os 80 IDs e o estado oficial de anulação, com URLs,
hashes e verificação documental automatizada explicitamente identificada.
`extraction-inventory.json` guarda páginas/colunas, hashes dos textos extraídos
e sugestões de formato/disciplinas. PDF e textos integrais permanecem fora
da distribuição; não foram incluídos resultados ou respostas pessoais.

Extração pypdf por coordenadas, colunas esquerda/direita e ordem vertical;
80 IDs únicos completos confrontados com o gabarito. Aviso de texto rotacionado
na extração layout inicial: formato por coordenadas foi usado para os itens.
Heurística sugere 63 diretos, 16 numerados e um V/F nos 80 itens, incluindo
o anulado. São rascunhos a conferir, não estatística jurídica homologada.
Cabeçalhos quebrados também podem exigir retificação de disciplina.

`profile-pending.json` foi produzido pelo calibrador existente: estado
`sem_calibracao`, 80 cadastrados, zero elegíveis. `point_source` ausente
impede elegibilidade; dificuldade não foi inventada. A revisão humana
precisa confirmar formato/disciplina e completar origem jurídica específica,
com identidade/data/notas. O item anulado continuará excluído.

Assim, a pendência de **aquisição de corpus oficial** foi resolvida; a de
**classificação revisada/calibração empírica aprovada** continua aberta.
Use o [pacote de revisão](../../release-0.8.0/revisao-humana.md).
