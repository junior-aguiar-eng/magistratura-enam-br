# Importação confirmada de remediação

Use o comando abaixo somente quando a skill de estudo produzir um evento `1.1.0` validado, com `remediation_id`, o mesmo `content_ref.id` da remediação, tentativa objetiva observada, resultado `correto` e `reason_codes` contendo `remediacao_concluida`.

```powershell
uv run python skills/planejar-jurisprudencia/scripts/importar_evento_remediacao.py `
  --arquivo esteira.xlsx `
  --evento evento.json `
  --confirmar
```

`--confirmar` representa autorização explícita para persistir o fechamento. Sem ele, o comando não altera a planilha. Evento parcial, inválido, referente a outro conteúdo, ambíguo ou já processado também não produz escrita.

Durante uma versão de migração, abas antigas que possuam apenas `id` podem ser usadas quando `remediation_id` e `content_ref.id` coincidirem exatamente com esse identificador. A importação acrescenta `resultado_remediacao` sem remover colunas ou dados preexistentes.
