# Relatório de orquestração e fontes — 0.5.0

## Método

Avaliação executada em 4 de setembro de 2026 com `gpt-5.6-sol`, o mesmo modelo do baseline `0.4.1`. Os 18 casos de entrada, transição e fontes foram executados três vezes em sessões efêmeras independentes. As respostas integrais permaneceram em armazenamento temporário local; este relatório registra somente métricas e sínteses sem material pessoal.

Saídas inicialmente reprovadas foram tratadas como defeitos, corrigidas e reexecutadas em três novas sessões. A matriz final usa exclusivamente as repetições posteriores às correções. Uma auditoria qualitativa independente aplicou a rubrica após a captura das respostas.

## Resultado final

- Execuções finais: 54/54 concluídas e aprovadas.
- Acerto de rota: 54/54.
- Ambientação no clique genérico: 3/3; baseline `0.4.1`: 0/3.
- Preservação de pendência nas transições avaliadas: 9/9; baseline `0.4.1`: 5/9.
- Políticas de fontes respeitadas nos casos aplicáveis: 18/18.
- Consultas externas em `acervo_exclusivo`: 0.
- Memória entre sessões ou estado fictício: 0.
- Descarte ou persistência silenciosa de atividade: 0.
- Exposição de JSON ou YAML interno: 0.

## Correções produzidas pela avaliação

1. Mudança de modalidade com disciplina ampla passou a solicitar apenas o tema específico, sem inventar subtema.
2. Tema amplo sem finalidade deixou de iniciar aula, questão ou flashcards unilateralmente.
3. Mudança apenas de tema passou a preservar a modalidade anterior sem perguntá-la novamente.
4. Pedido de continuidade sem checkpoint passou a solicitar somente o último ponto disponível.
5. Menção incidental ou intenção futura deixou de criar rota suspensa ou pendência fictícia.

Cada correção foi reexecutada três vezes; a auditoria integral posterior aprovou 54 saídas e não identificou ocorrência impeditiva.

## Comparação cega com 0.4.1

Seis casos representativos foram pareados com novas execuções da release instalada `0.4.1`, sem identificação das versões. Dois avaliadores independentes produziram 12 decisões: cinco preferências pela candidata, seis pelo baseline e um empate. Nenhum avaliador identificou regressão impeditiva; a qualidade jurídica das questões e das respostas de fontes permaneceu equivalente. A candidata apresentou ganho consistente em ambientação e preservação de transições, enquanto algumas respostas do baseline foram preferidas apenas por concisão ou formulação estilística.

O resultado sustenta não inferioridade jurídica e operacional dentro da amostra, mas não demonstra superioridade pedagógica geral nem permite inferir retenção, desempenho em prova ou probabilidade de aprovação.

## Gate

A release fica bloqueada se reaparecer mistura de skills, busca no modo exclusivo, memória fictícia, descarte silencioso, seleção arbitrária de conteúdo ou fonte editorial apresentada como autoridade oficial. Nenhuma dessas ocorrências permaneceu na matriz final.
