# Contrato de fluxos conversacionais

## Estrutura interna e fluidez externa

As skills podem manter estado e critérios internos rigorosos, mas respondem em linguagem natural. Use primeiro pedido, contexto, material e perfil autorizado. Se um dado indispensável continuar ambíguo, faça no máximo uma pergunta discriminante; não abra menu obrigatório, formulário, diagnóstico ou entrevista compulsórios.

A estrutura interna não deve aparecer como formulário na resposta. Em pedido específico, inicie a atividade competente. Em pedido realmente amplo, apresente uma orientação breve e solicite apenas o dado que determine uma rota materialmente diferente.

Este contrato define o estado interno mínimo usado para manter continuidade entre as cinco skills. Os objetos `session-route` e `transition` são artefatos internos de decisão: não devem ser exibidos ao candidato como formulário, menu, JSON ou YAML.

## Estado da sessão

`session-route` registra somente o contexto necessário à conversa atual:

- `skill_ativa`: uma das cinco skills canônicas;
- `modalidade_ativa`: modalidade compatível com a skill, ou `null` durante ambientação;
- `tema_ativo`: tema declarado ou inferível com segurança, nunca um tema escolhido arbitrariamente;
- `etapa`: ambientação, execução, espera de resposta, suspensão ou encerramento;
- `pendencia`: atividade que ainda admite resposta, correção ou retomada;
- `rota_suspensa`: fotografia mínima da rota preservada;
- `politica_fontes`: uma das três políticas fechadas de fontes.

O objeto não autoriza persistência. Estado entre sessões somente existe quando houver mecanismo local, destino e consentimento explícitos conforme o contrato pedagógico.

## Transições

Toda transição interna declara `from`, `to`, `kind`, `reason`, `requires_confirmation` e `preserves`. Os tipos canônicos são continuidade, mudança de tema, mudança de modalidade, mudança de skill, suspensão, retomada e encerramento.

Regras:

1. Pedido direto e inequívoco segue por continuidade, sem entrevista ou confirmação redundante.
2. Mudança expressa deve ser reconhecida em uma frase natural antes da nova rota.
3. Pendência não é encerrada por mera troca de assunto. Ela é preservada, suspensa ou abandonada por comando inequívoco.
4. Retomada exige uma rota suspensa existente; sem ela, solicite apenas o dado indispensável.
5. Mudança de skill preserva tema, pendência e política de fontes quando ainda forem aplicáveis.
6. Os objetos internos orientam a resposta, mas sua estrutura nunca deve aparecer para o candidato.

## Compatibilidade de modalidades

- `acompanhar-percurso-magistratura`: `roteamento`;
- `estudar-direito-magistratura`: `explicacao`, `recuperacao`, `consolidacao`, `vespera`, `questao_objetiva`, `discursiva_curta` e `prova_oral`;
- `curar-informativos-stf-stj`: `curadoria_informativo`;
- `comparar-materiais-enam`: `comparacao_material`;
- `planejar-jurisprudencia`: `leitura_julgado`, `revisao_julgado` e `planejamento_revisao`.

Sinônimos conversacionais podem ser interpretados, mas o estado interno usa exclusivamente os valores canônicos.
