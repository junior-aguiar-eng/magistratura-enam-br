# Contrato pedagógico compartilhado

Este contrato define a linguagem comum entre as skills. Na versão 1 ele não autoriza persistência, adaptação automática, criação de agenda nem mudança no formato das respostas. Um registro só pode descrever fatos observáveis na interação atual ou dados explicitamente fornecidos pelo candidato.

## Taxonomia canônica v1

O bloco abaixo é normativo e consumível por testes. Categorias equivalentes, sinônimos ou extensões exigem nova versão do contrato.

<!-- taxonomia-v1 -->
```json
{
  "modalidades": [
    "explicacao",
    "recuperacao",
    "consolidacao",
    "vespera",
    "questao_objetiva",
    "discursiva_curta",
    "prova_oral",
    "leitura_julgado",
    "revisao_julgado"
  ],
  "resultados": [
    "nao_avaliado",
    "correto",
    "parcial",
    "incorreto",
    "questao_invalida"
  ],
  "tipos_de_erro": [
    "conceito",
    "pressuposto",
    "regra",
    "excecao",
    "competencia",
    "legitimidade",
    "prazo",
    "efeito",
    "suporte_fatico",
    "distincao",
    "atualizacao_normativa",
    "atualizacao_jurisprudencial",
    "fundamentacao",
    "expressao_oral",
    "estrutura_discursiva"
  ],
  "evidencias_de_dominio": [
    "evocacao_regra",
    "discriminacao_institutos",
    "aplicacao_fatos_novos",
    "fundamentacao_normativa_jurisprudencial",
    "expressao_objetiva_discursiva_oral",
    "retencao_revisao_posterior"
  ]
}
```

## Regras de registro

- `activity.modality` descreve a atividade efetivamente realizada, não a intenção futura.
- `performance.result` permanece `nao_avaliado` sem tentativa observável do candidato.
- A ausência de resposta, de arquivo ou de contexto não autoriza inferir erro. `error_types` exige tentativa observável e fundamento identificável na resposta.
- Evidência de domínio registra dimensões demonstradas, nunca nota global, personalidade ou aptidão presumida.
- Confiança só pode ser registrada quando declarada pelo candidato; fluência textual não equivale a confiança nem domínio.
- `content_ref` identifica a fonte ou unidade de conteúdo sem copiar resposta integral, anexo ou dado pessoal.
- `routing` registra encaminhamento justificável entre skills; não executa outra skill nem cria prioridade geral.

## Fronteiras entre skills

- `estudar-direito-magistratura` pode produzir tentativa, resultado, erro e evidência quando houver atividade avaliativa observável.
- `planejar-jurisprudencia` pode consumir resultados já registrados e produzir recomendação de revisão, sem inventar desempenho.
- `curar-informativos-stf-stj` referencia conteúdo selecionado; só registra desempenho se houver tentativa posterior e observável do candidato.
- `comparar-materiais-enam` registra atualização documental. Nunca registra domínio, confiança ou erro do candidato.

## Privacidade e governança

Os schemas rejeitam propriedades inesperadas. Nome, CPF, matrícula, e-mail e conteúdo integral de respostas ou anexos não pertencem aos contratos. Objetivos e preferências são opcionais, explícitos e limitados ao estudo. Nesta fase, os artefatos definem formato e invariantes, mas não gravam dados.

