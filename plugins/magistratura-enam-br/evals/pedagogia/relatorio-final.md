# Relatório final da evolução pedagógica

## Escopo

Foram executados 16 casos em três sessões efêmeras independentes por caso: os 12 casos derivados do baseline `0.3.3` e quatro casos adicionais sobre persistência recusada, perfil contraditório, remediação cruzada e roteamento ambíguo. A candidata foi executada com `gpt-5.6-sol`, configuração sem memória persistente e sandbox de leitura.

Três casos originalmente subespecificados foram corrigidos antes da rodada final: correção sem enunciado integral e dois cenários de curadoria sem conteúdo sintético suficiente. Por isso, a comparação quantitativa desses casos com o baseline antigo não é direta.

## Resultado técnico

- 48 saídas produzidas e preservadas em `fase-6/runs/`.
- Nenhuma falha nas asserções automáticas após as correções.
- O baseline registrava 12 reprovações automáticas em 36 execuções, parte delas causada por casos insuficientemente instrumentados e por verificação textual incapaz de distinguir recusa de afirmação.
- O roteador deixou de inventar nomes de skills e passou a usar exclusivamente os cinco destinos canônicos.
- Dez cenários adicionais de roteamento, um positivo e um near-miss para cada skill, preservaram os cinco nomes canônicos e bloquearam execução quando faltava fonte ou objetivo discriminante.
- A capacidade diária deixou de sofrer desconto indevido da folga semanal.
- O planejador preserva o valor `erro` da planilha, sem convertê-lo em `incorreto`.
- A recusa de persistência informa apenas ausência de gravação, confirmação necessária e caminho local opcional.
- Remediação cruzada, fechamento por relato livre, persistência implícita e avaliação do candidato por delta documental foram recusados em todas as repetições pertinentes.

## Extensão, tokens e variância

Nos 12 casos comuns, o baseline teve média de 86 palavras por saída. A candidata, após instrumentação dos casos de curadoria, teve média de 229,8 palavras, com mínimo de 27 e máximo de 750. O aumento decorre principalmente da estrutura editorial completa da curadoria e da correção doutrinária detalhada. A comparação de extensão não é diretamente causal nos três casos cujo prompt foi corrigido.

O harness preservou apenas a mensagem final; a contagem exata de tokens de cada execução não ficou disponível. Palavras foram usadas como proxy explícita de extensão. A variância qualitativa caiu nos ciclos fixos, no fechamento de remediação e no roteamento; permaneceu maior nas respostas jurídicas abertas, sem alteração de conclusão material.

## Revisão independente

A primeira revisão automatizada independente bloqueou a candidata por quatro problemas: orçamento diário, vocabulário da remediação, skill inexistente e recusa de persistência contaminada por instruções do harness. Os quatro foram corrigidos e reexecutados três vezes. Duas revisões automatizadas focadas aprovaram integralmente as saídas corrigidas. Essas revisões não substituem a revisão humana exigida pelo plano.

## Gate

Os gates automatizados e a revisão independente automatizada estão aprovados. Não houve regressão jurídica material identificada, vazamento textual de gabarito, inferência de memória, persistência sem opt-in ou fechamento indevido de remediação.

Os gates finais registraram 161 testes aprovados, Ruff aprovado, lock sincronizado, integração aprovada com 33 arquivos essenciais e validação estrutural do plugin aprovada. Uma instalação limpa isolada reconheceu a versão `0.4.0`, a quinta skill e o script de relatório; nenhum perfil ou log foi criado durante a instalação.

Revisão humana aprovada pelo responsável pelo repositório em 4 de setembro de 2026. O gate da Fase 6 está liberado.
