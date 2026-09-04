# Avaliações pedagógicas

Este diretório mede o comportamento das skills com casos sintéticos e versionados. Os testes automatizados validam estrutura e riscos observáveis; a rubrica humana decide precisão jurídica, qualidade pedagógica e defensabilidade.

## Execução do baseline

1. Use uma sessão nova para cada execução, sem histórico de outro caso.
2. Execute cada caso três vezes com a versão indicada em `baseline`.
3. Capture texto, duração e tokens quando disponíveis.
4. Rode `scripts/avaliar_saida_pedagogica.py` para asserções automáticas.
5. Aplique `rubrica.md` somente depois da saída.
6. Registre apenas resultados agregados e evidências sintéticas no relatório versionado.

Não use material pessoal, prova protegida ou resposta real do candidato como fixture versionada.
