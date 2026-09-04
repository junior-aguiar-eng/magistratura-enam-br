# Ambientação pedagógica integrada do plugin Magistratura ENAM BR

## Propósito

Evoluir o plugin de um conjunto de quatro skills juridicamente especializadas para um ambiente pedagógico integrado, mensurável e adaptativo, sem retirar do candidato o controle sobre tema, agenda, fontes ou profundidade do estudo.

## Princípios invariantes

1. As quatro skills atuais continuam sendo as autoridades de domínio:
   - `curar-informativos-stf-stj`: seleção e comentário jurisprudencial;
   - `estudar-direito-magistratura`: explicação, revisão ativa e treino;
   - `planejar-jurisprudencia`: agenda e capacidade de revisão de julgados;
   - `comparar-materiais-enam`: comparação documental e atualização de materiais.
2. A integração ocorre por contratos de dados compartilhados, não por duplicação de instruções.
3. Persistência é local, explícita, opcional e controlada pelo candidato. Nenhuma skill presume acesso a arquivo de perfil ou histórico não fornecido na tarefa.
4. O log de eventos pedagógicos é append-only e canônico. O perfil do candidato é uma projeção reconstruível desse log.
5. Respostas completas continuam disponíveis. Qualquer redução adaptativa de feedback depende de opção expressa e de evidência suficiente.
6. O planejamento de tempo permanece sob decisão do candidato. O sistema pode calcular carga, risco e alternativas, mas não cria agenda silenciosamente.
7. Material do candidato, mapa curricular, análise estratégica, fonte oficial e complemento geral permanecem categorias distintas.
8. Nenhuma métrica pedagógica substitui precisão jurídica ou confirmação em fonte oficial.
9. Mudanças de comportamento exigem avaliações com saídas reais do modelo; testes de presença textual não bastam.
10. Python 3.14, `uv`, operação local e formatos portáveis permanecem o ambiente canônico.

## Arquitetura-alvo

### Camada 1: contratos pedagógicos compartilhados

Dois artefatos estruturados sustentam a integração:

- `learning-event.schema.json`: registra uma interação pedagogicamente relevante sem armazenar necessariamente a resposta integral do candidato.
- `candidate-profile.schema.json`: representa objetivos, preferências explícitas e estado agregado por competência.

O evento é a fonte de verdade. O perfil pode ser apagado e reconstruído deterministicamente.

### Camada 2: serviços locais determinísticos

Scripts Python validam eventos, acrescentam registros ao JSONL, recompõem o perfil e calculam sugestões de revisão. Eles não chamam modelos, não pesquisam conteúdo jurídico e não escolhem a agenda do candidato.

Interfaces planejadas:

```python
def validate_learning_event(event: dict) -> list[str]: ...
def append_learning_event(log_path: Path, event: dict) -> None: ...
def rebuild_candidate_profile(events: Iterable[dict]) -> dict: ...
def recommend_review(event: dict, policy: dict) -> dict: ...
```

As gravações usam arquivo temporário no mesmo diretório, `flush`, `fsync` e substituição atômica quando houver projeção mutável. O log JSONL nunca é reescrito por atualização ordinária.

### Camada 3: adaptação dentro das skills

Cada skill produz ou consome apenas os eventos que pertencem ao seu domínio:

| Skill | Consome | Produz |
|---|---|---|
| Curadoria | documentos oficiais e recorte expresso | referência de conteúdo e sugestão de entrada na esteira |
| Estudo | referência de conteúdo, perfil opcional e remediação | evento de tentativa, erro, confiança e transferência |
| Planejamento | julgados curados e eventos de revisão | próxima revisão sugerida e remediação |
| Comparação | pares documentais publicados | evento de atualização do material, sem inferir domínio do candidato |

### Camada 4: orquestração fina

Somente após os contratos e fluxos estarem estabilizados, uma quinta skill de acompanhamento poderá orientar qual skill deve atuar. Ela não explica Direito, não cura julgados, não compara materiais e não agenda autonomamente. Sua função é ler objetivo expresso, perfil disponibilizado e pendências para encaminhar a atividade à skill responsável.

## Taxonomia pedagógica v1

### Modalidades

- `explicacao`
- `recuperacao`
- `consolidacao`
- `vespera`
- `questao_objetiva`
- `discursiva_curta`
- `prova_oral`
- `leitura_julgado`
- `revisao_julgado`

### Resultados

- `nao_avaliado`
- `correto`
- `parcial`
- `incorreto`
- `questao_invalida`

### Tipos de erro

- `conceito`
- `pressuposto`
- `regra`
- `excecao`
- `competencia`
- `legitimidade`
- `prazo`
- `efeito`
- `suporte_fatico`
- `distincao`
- `atualizacao_normativa`
- `atualizacao_jurisprudencial`
- `fundamentacao`
- `expressao_oral`
- `estrutura_discursiva`

### Evidência de domínio

O perfil não reduz aprendizagem a uma nota única. Cada competência registra separadamente:

- evocação da regra;
- discriminação entre institutos próximos;
- aplicação a fatos novos;
- fundamentação normativa ou jurisprudencial;
- expressão objetiva, discursiva ou oral;
- retenção observada em revisão posterior.

## Política adaptativa v1

A política adaptativa será opt-in. A política fixa atual continuará sendo o padrão durante a migração.

| Evidência | Sugestão v1 |
|---|---|
| Incorreto | remediação obrigatória antes de ampliar intervalo; nova revisão em 1 dia |
| Parcial | remediação focal; próxima revisão no menor valor entre 3 dias e o intervalo fixo seguinte |
| Correto sem confiança ou justificativa | manter intervalo fixo |
| Correto com baixa confiança | manter intervalo fixo e sugerir contraste breve |
| Correto com alta confiança, sem transferência | multiplicar o intervalo fixo por 1,25, arredondando para baixo |
| Correto com alta confiança e transferência válida | multiplicar por 1,5, limitado a 90 dias |
| Reincidência do mesmo erro | reiniciar em 1 dia e manter remediação aberta |

Esses coeficientes são heurísticos e devem operar inicialmente em modo sombra: o sistema calcula e registra a sugestão, mas mantém a data fixa até comparação suficiente entre as duas políticas.

## Feedback adaptativo

O comportamento atual de correção completa permanece como padrão. O candidato poderá optar por `feedback_adaptativo`, com estas regras:

- erro, resposta parcial, baixa confiança ou fundamentação ausente: correção completa;
- acerto com alta confiança e justificativa juridicamente correta: resultado, fundamento determinante, principal distinção e apenas os distratores materialmente perigosos;
- auditoria de questão ou pedido expresso: correção forense completa;
- qualquer ambiguidade: reconhecer invalidade da questão antes de avaliar o candidato.

## Privacidade e governança

- Não registrar nome, CPF, matrícula, e-mail ou conteúdo integral de anexos.
- Não registrar resposta integral por padrão; armazenar síntese da evidência e códigos de erro.
- Exigir caminho de arquivo fornecido ou confirmado pelo candidato para toda persistência.
- Permitir exportar, reconstruir e excluir perfil sem apagar o log original, salvo comando expresso para excluir ambos.
- Versionar schemas e fornecer migrações explícitas, reversíveis e testadas.

## Estratégia de avaliação

A eficácia será avaliada em quatro níveis:

1. contrato: schemas, roteamento, formatos e invariantes;
2. comportamento da IA: saídas reais em casos sintéticos versionados;
3. qualidade jurídica: rubrica humana cega para precisão, fontes e defensabilidade;
4. aprendizagem: retenção, transferência, reincidência de erros e calibração de confiança.

Cada cenário comportamental deve ter ao menos três execuções por configuração para revelar variância. O baseline é a versão `0.3.3`. Resultados brutos com conteúdo pessoal não serão versionados.

## Limites desta evolução

- Não criar plataforma web, conta, nuvem, telemetria ou banco remoto.
- Não substituir a decisão do candidato por algoritmo de prioridade geral.
- Não criar cronograma completo de todas as disciplinas dentro de `planejar-jurisprudencia`.
- Não afirmar eficácia educacional apenas porque testes estruturais passaram.
- Não introduzir gamificação, pontos ou sequências artificiais sem hipótese pedagógica e avaliação própria.

## Critério global de conclusão

O ambiente será considerado pedagogicamente integrado quando uma remediação puder percorrer, com dados locais e rastreáveis, o ciclo `julgado/material → atividade → tentativa → feedback → evento → perfil → sugestão de revisão`, sem que nenhuma skill ultrapasse sua autoridade de domínio e sem alegação de memória não disponibilizada pelo candidato.
