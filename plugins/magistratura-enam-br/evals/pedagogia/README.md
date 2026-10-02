# Avaliações pedagógicas

Este diretório mede o comportamento das skills com casos sintéticos e versionados. Os testes automatizados validam estrutura e riscos observáveis; a rubrica humana decide precisão jurídica, qualidade pedagógica e defensabilidade.

## Piloto em uso real da candidata 0.7.3

Use o plugin em atividades normais, sem roteiro de 24 execuções. Quando houver resposta suspeita, registre apenas cliente, versão, data, pergunta e trecho necessário da saída, após retirar dados pessoais e material protegido. Confira o ponto contestado na fonte apropriada e converta defeitos confirmados em casos sintéticos de regressão. Ausência de relatos não comprova qualidade; este piloto não altera o estado `pending` do benchmark formal.

## Execução do baseline

1. Use uma sessão nova para cada execução, sem histórico de outro caso.
2. Execute cada caso três vezes com a versão indicada em `baseline`.
3. Capture texto, duração e tokens quando disponíveis.
4. Rode `scripts/avaliar_saida_pedagogica.py` para asserções automáticas.
5. Aplique `rubrica.md` somente depois da saída.
6. Registre apenas resultados agregados e evidências sintéticas no relatório versionado.

Não use material pessoal, prova protegida ou resposta real do candidato como fixture versionada.

O piloto jurídico em `benchmark-juridico/` acrescenta fonte oficial, data de corte, proposições verificáveis e estado de revisão humana aos casos sintéticos. Fonte localizada não torna a saída correta: a análise da aplicação da norma ao caso, da unicidade do gabarito e da proporcionalidade permanece humana. Casos com fixture `pending` não são referência jurídica aprovada.

## Profissionalização 0.6.0

Testes literais protegem somente contratos textuais e proibições objetivamente enumeráveis. Profundidade dogmática, função das fontes, plausibilidade de soluções e qualidade de correção exigem rubrica semântica e revisão jurídica humana. Nenhum caso versionado contém material ou desempenho pessoal de candidato.
