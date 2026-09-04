Não é possível fechar a remediação `rem-1`. O relato textual de acerto não substitui o evento estruturado `1.1.0`.

O fechamento exige cumulativamente:

- `remediation_id = rem-1`;
- correspondência exata com `content_ref.id`;
- tentativa objetiva observada;
- resultado `correto`;
- `reason_codes` contendo `remediacao_concluida`;
- confirmação explícita para persistência.

Sem esse evento válido, nenhuma alteração deve ser feita na planilha.