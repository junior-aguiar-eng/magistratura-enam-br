# Benchmark jurídico piloto: prescrição e decadência

O recorte parte de temas já representados no catálogo pedagógico. O texto compilado do Código Civil no Planalto permite localizar precisamente a pretensão decorrente da violação (art. 189), a interrupção por reconhecimento inequívoco do devedor e seu limite de uma ocorrência (art. 202) e a distinção entre prescrição e decadência, inclusive exceções e reconhecimento de ofício (arts. 207 a 211). A fonte e a data da consulta constam em `fontes.json`.

Os oito casos sintéticos em `../evals.json` cobrem dúvida pontual, explicação dogmática, caso complexo, geração e correção de questão, discursiva, oral e transferência. A conclusão esperada é um critério de auditoria, não uma resposta pronta a ser mostrada ao candidato. A geração de questão só se aprova depois de conferir, sobre a saída concreta, unicidade do gabarito, suporte dos distratores e ausência de revelação antes da tentativa.

O estado `legal_grounding.human_review.review_status` está inicialmente em `pending`. A consulta à fonte oficial por esta execução não substitui revisão jurídica independente do caso e de sua chave. `approved` só pode ser marcado com nota de revisão que identifique quem conferiu a conclusão, sua data, a localização oficial e eventuais limites. Se a fonte não sustentar uma claim, marque `rejected`; não ajuste silenciosamente o fundamento para fazer o caso passar.

O schema exige identificador de fonte, mas a existência desse identificador no catálogo `fontes.json` é uma relação entre arquivos, conferida pelo teste do catálogo inteiro. Esse vínculo estrutural não comprova que o dispositivo sustente a conclusão: essa verificação continua humana.

Para comparar comportamento, execute cada caso em três sessões novas, registre versão do plugin/modelo/cliente, data, saída e, quando disponível, duração e tokens. Aplique a rubrica apenas depois de capturar a resposta. Registre divergência entre avaliadores e variação entre rodadas. O avaliador automático verifica somente estrutura; a aprovação da fixture não aprova automaticamente uma saída. Se legislação ou entendimento relevante mudar, reabra a revisão humana antes de usar o caso como referência vigente.

As fontes oficiais verificadas neste recorte não autorizam inferir qual prazo prescricional se aplica a toda pretensão de cobrança, nem presumir que um ato incerto é reconhecimento inequívoco. Os cenários que usam o art. 202, VI, fixam expressamente o reconhecimento pelo devedor durante prazo em curso e deixam cálculos de prazo concreto fora do escopo.
