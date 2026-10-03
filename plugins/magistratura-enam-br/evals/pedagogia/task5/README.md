# Task 5 — avaliação da candidata pedagógica

Estado: **candidata pendente de revisão humana**. Capturas em 2026-10-03 no Codex desktop; instruções anteriores em `d00540c` e candidata local sobre essa base, ainda sob versão 0.7.5. Não houve execução do modelo no ChatGPT nem uso de resposta real de candidato.

## Método e rastreabilidade

Cinco sessões novas por variante executaram o mesmo pedido de associação, sem histórico herdado, override de modelo, chave ou rubrica. O controle leu AGENTS, skill, referência FGV e protocolo de acervo congelados antes da edição; a candidata leu o mesmo conjunto de arquivos com as novas instruções. O identificador exato do modelo não foi exposto: a configuração herdada foi mantida, mas não se comprova igualdade de revisão interna do modelo. Tokens e duração não estavam disponíveis. O horário registrado corresponde à gravação da saída.

O [catálogo](catalogo.json) contém pedido/material, turnos de correção e critérios posteriores. Os registros em `runs/` foram gerados com `registrar_execucao_pedagogica.registrar_execucao` e validados pelo schema existente. O [manifesto](manifest.json) relaciona hashes de instruções, casos e saídas. A fixture é sintética, apoiada no [CPC, art. 64, §§ 2º–4º](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm), conferido em fonte oficial em 2026-10-03; sua revisão jurídica humana permanece `pending`.

Os agentes receberam somente arquivos de instruções, pedido e material. Não receberam `expected_output`, assertions, chave ou rubrica do catálogo. Após capturar a geração, a sessão candidate1 recebeu a tentativa sintética C e pedido de correção; a sessão V/F recebeu o mesmo tipo de tentativa. Revisão de trecho, material anterior inacessível e V/F usaram sessões adicionais novas. Os arquivos de evidência não são material a consultar antes da tentativa em uma sessão de estudo.

## Observações posteriores do agente mantenedor

Esta leitura é automatizada, posterior à captura; **não é revisão humana**. As checagens automáticas de geração verificam somente cinco alternativas e encerramento na E. Todos os 15 registros continuam `revisao_humana_pendente`.

| Captura | Observação posterior, sem aprovação jurídica |
| --- | --- |
| baseline1 | Associação 3–2–1, letra C inferida; remessa, cessação expressa e substituição. Reutilização não explicitada. |
| baseline2 | Associação 2–3–1, C inferida; rejeição/acolhimento e efeitos. Reutilização não explicitada. |
| baseline3 | Associação 1–2–4, C inferida; cinco soluções, três situações. Informa soluções excedentes, mas não regra de reutilização. |
| baseline4 | Associação 2–3–1, B inferida; conservação, cessação expressa e substituição. Reutilização não explicitada. |
| baseline5 | Associação 2–3–1, D inferida; substituição parcial dos efeitos. Reutilização não explicitada. |
| candidate1 | Associação 3–1–5, C inferida; uso uma, várias ou nenhuma vez explícito. Distratores mobilizam ratificação e retroatividade. |
| candidate2 | Associação 2–3–1, D inferida; cada solução uma vez. A conservação integral é distinguida de substituição parcial. |
| candidate3 | Associação 1–2–3, C inferida; uso no máximo uma vez e excedentes explícitos. Distrator acrescenta trânsito não fornecido. |
| candidate4 | Associação 1–2–3, D inferida; uso único explícito; rejeição da arguição varia também o destino dos autos. |
| candidate5 | Associação 1–3–2, B inferida; uso único explícito; substituição por medida mais restrita. |
| candidate1-correcao | Confirma C após tentativa; explica I, II, III e as cinco combinações, com vícios próprios dos quatro distratores. |
| revisao | Identifica seção 2, distingue destino/efeitos, conserva ressalva e “se for o caso”; entrega dois flashcards sem agenda ou questão. |
| inacessivel | Declara ausência do material anterior e pede página/trecho/checkpoint, preservando acervo exclusivo. |
| vf | Três assertivas e cinco sequências distintas; V–F–V/C inferido, sem solução anunciada. |
| vf-correcao | Explica I, II, III e as cinco sequências depois de C, inclusive no acerto. |

O controle já conseguia produzir associação. A regra de reutilização apareceu expressamente em 5/5 candidatas e não nas cinco anteriores; isso descreve esta amostra, não demonstra superioridade geral, ganho estatístico ou qualidade FGV certificada. Nas associações, a competência é frequentemente um dado já estabelecido e os efeitos concentram a variação: não considerar o desenho de matriz com dois eixos independentes homologado por essas capturas.

## Rubrica humana ainda pendente

Para cada questão/correção, verificar suporte oficial/material, núcleo funcional, plausibilidade dos componentes, unicidade do mapeamento, comparação dos distratores e limite de fonte. Para revisão sem questão, justificar a inaplicabilidade de unicidade/distratores e avaliar rastreabilidade, ressalvas, fidelidade e proporcionalidade. Identificar revisor/data, decisão por critério e hashes antes de aprovar.

Q13 (notícia sem fundamentos) e Q17 (mesma conclusão com fundamentos distintos) foram especificados, mas não executados neste ensaio; Q11, Q12, Q14 e Q15 tiveram capturas, e a cobertura de Q16 é parcial. Numerado/direto conservam as travas existentes e não receberam nova amostra comportamental. Os contratos textuais e os 388 testes Python não substituem essa cobertura ou revisão humana. Não promover novas orientações a AGENTS com base apenas neste relatório. A homologação em host real e o benchmark comparativo mais amplo permanecem na task 8.
