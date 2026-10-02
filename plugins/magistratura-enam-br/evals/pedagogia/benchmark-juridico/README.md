# Benchmark jurídico piloto: prescrição e decadência

O recorte parte de temas já representados no catálogo pedagógico. O texto compilado do Código Civil no Planalto permite localizar precisamente a pretensão decorrente da violação (art. 189), a interrupção por reconhecimento inequívoco do devedor e seu limite de uma ocorrência (art. 202) e a distinção entre prescrição e decadência, inclusive exceções e reconhecimento de ofício (arts. 207 a 211). A fonte e a data da consulta constam em `fontes.json`.

Os oito casos sintéticos em `../evals.json` cobrem dúvida pontual, explicação dogmática, caso complexo, geração e correção de questão, discursiva, oral e transferência. A conclusão esperada é um critério de auditoria, não uma resposta pronta a ser mostrada ao candidato. A geração de questão só se aprova depois de conferir, sobre a saída concreta, unicidade do gabarito, suporte dos distratores e ausência de revelação antes da tentativa.

O estado `legal_grounding.human_review.review_status` está inicialmente em `pending`. A consulta à fonte oficial por esta execução não substitui revisão jurídica independente do caso e de sua chave. `approved` só pode ser marcado com nota de revisão que identifique quem conferiu a conclusão, sua data, a localização oficial e eventuais limites. Se a fonte não sustentar uma claim, marque `rejected`; não ajuste silenciosamente o fundamento para fazer o caso passar.

O schema exige identificador de fonte, mas a existência desse identificador no catálogo `fontes.json` é uma relação entre arquivos, conferida pelo teste do catálogo inteiro. Esse vínculo estrutural não comprova que o dispositivo sustente a conclusão: essa verificação continua humana.

Ao concluir a revisão da fixture, `human_review` aceita `approved` ou `rejected`, com `reviewer`, `reviewed_at` (AAAA-MM-DD) e `review_note` não vazios. A nota deve relacionar a conclusão ao localizador oficial já indicado em `claims`. Os testes validam a evidência exigida e não obrigam a permanência em `pending`.

Para comparar comportamento, execute cada caso em três sessões novas, registre versão do plugin/modelo/cliente, data, saída e, quando disponível, duração e tokens. Aplique a rubrica apenas depois de capturar a resposta. Registre divergência entre avaliadores e variação entre rodadas. O avaliador automático verifica somente estrutura; a aprovação da fixture não aprova automaticamente uma saída. Se legislação ou entendimento relevante mudar, reabra a revisão humana antes de usar o caso como referência vigente.

As fontes oficiais verificadas neste recorte não autorizam inferir qual prazo prescricional se aplica a toda pretensão de cobrança, nem presumir que um ato incerto é reconhecimento inequívoco. Os cenários que usam o art. 202, VI, fixam expressamente o reconhecimento pelo devedor durante prazo em curso e deixam cálculos de prazo concreto fora do escopo.

## Registrar uma execução capturada

O registrador não chama modelos, não inventa respostas e não certifica a identidade do revisor. Ele grava a evidência fornecida e verifica sua estrutura e correspondência. Execute o caso em sessão nova e salve a saída em UTF-8. Crie um JSON de metadados com os valores efetivamente observados:

```json
{
  "run_id": "juridico-pontual-rodada-1",
  "executed_at": "2026-10-02T12:00:00-03:00",
  "plugin_version": "0.7.4",
  "model": "identificador-real-do-modelo",
  "client": "cliente-e-versao-observados",
  "session_id": "identificador-da-sessao-nova",
  "round": 1,
  "origin": "captured_session"
}
```

O exemplo é ilustrativo; não o apresente como execução realizada. Use `synthetic_fixture` para testes do mecanismo. Duração e tokens são opcionais e só devem ser incluídos quando medidos. A partir da raiz do plugin:

```powershell
uv run python scripts/registrar_execucao_pedagogica.py --catalogo evals/pedagogia/evals.json --caso ID_DO_CASO --saida saida.txt --metadados metadados.json --destino execucao.json --confirmar-gravacao-local
```

O arquivo contém snapshot e hash do caso, texto e hash da saída, identificação da execução e resultado estrutural. O destino deve ser novo: não há sobrescrita de registros existentes. Sem revisão, o resultado permanece `revisao_humana_pendente` quando houver exigências humanas.

Para registrar a revisão da saída, forneça `--revisao revisao.json` e outro destino. O JSON contém `reviewer`, `reviewed_at`, `review_note`, `output_sha256` igual ao hash do texto avaliado, `case_sha256` igual ao hash do snapshot revisado e `criteria`: uma entrada `{ "id": "…", "passed": true, "evidence": "…" }` para cada identificador em `evaluation.human_review_required`. Os critérios `rubrica-1`, `rubrica-2` etc. seguem a ordem da rubrica no snapshot. Mudança do caso ou da saída exige nova revisão; critérios duplicados, ausentes, desconhecidos ou sem evidência são rejeitados.

Uma revisão favorável não supera falha automática nem aprova uma fixture pendente. `aprovado_com_revisao_humana` significa que a revisão fornecida cobre os critérios e a fixture não está pendente/rejeitada; não representa autenticação independente do revisor. Não versione respostas pessoais. As rodadas reais e a revisão jurídica independente do piloto continuam pendentes até serem efetivamente realizadas e registradas.
