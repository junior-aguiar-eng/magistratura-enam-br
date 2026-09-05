# Inventário de regras pedagógicas da versão 0.5.0

Este inventário vincula cada regra substantiva à sua finalidade e ao destino previsto. `Remover` só é admissível quando a capacidade permanece coberta em fonte canônica e por gate correspondente.

| Regra | Origem | Finalidade | Operação | Destino canônico | Cobertura |
|---|---|---|---|---|---|
| Precisão, atualização e fidelidade jurídica | `AGENTS.md` | Segurança jurídica transversal | preservar | `AGENTS.md` | `test_fontes_por_skill.py`, `test_governanca_fontes.py` |
| Público de bacharéis, Magistratura e ENAM | implícito em `AGENTS.md` e skills | Manter densidade compatível | aprofundar | `AGENTS.md` | `test_despersonificacao_plugin.py` |
| Uso proporcional de fontes oficiais | `AGENTS.md`, política e skills | Rastreabilidade | realocar | `politica-fontes-juridicas.md` | `test_politica_fontes.py` |
| Acervo como base pedagógica sem primazia sobre fonte oficial | `AGENTS.md`, protocolo e estudo | Fidelidade ao material | preservar | `protocolo-uso-do-acervo.md` | `test_contrato_acervo_markdown.py` |
| Fluidez e uma pergunta discriminante | ambientações e skills | Evitar interrogatório | realocar | `contrato-fluxos-conversacionais.md` | `test_ambientacao_estudo.py` |
| Cinco rotas públicas | orquestrador e schemas | Estabilidade de invocação | preservar | `roteamento.md` | `test_roteamento_percurso.py` |
| Continuidade e transições com preservação de estado | contrato e referências | Evitar reinício e perda material | preservar | `contrato-fluxos-conversacionais.md` | `test_transicoes_rota.py` |
| Progressão do estudo dogmático | estudo e `explicacao-e-integracao.md` | Formação conceitual | aprofundar | `explicacao-e-integracao.md` | novo gate dogmático |
| Flashcards proporcionais | estudo e referência própria | Retenção ativa | preservar | `flashcards-de-alto-rendimento.md` | `test_contrato_flashcards.py` |
| Cinco alternativas, chave única e auditoria | estudo e questões | Validade objetiva | preservar | `questoes-fgv-enam.md` | `test_contrato_questoes_fgv.py` |
| Correção objetiva completa por padrão | estudo e questões | Diagnóstico técnico | preservar | `questoes-fgv-enam.md` | `test_correcao_proporcional.py` |
| Discursiva e oral no mesmo arquivo | `discursivas-e-prova-oral.md` | Orientar duas modalidades | realocar | referências separadas | novos gates por modalidade |
| Casos dentro da explicação geral | estudo | Aplicação complexa | aprofundar | `casos-complexos.md` | novo gate de casos |
| Curadoria com campos completos | curadoria | Rastreabilidade jurisprudencial | preservar | `comentario-jurisprudencial.md` | `test_curadoria_estrutura.py` |
| Campos de curadoria sempre extensos | curadoria | Padronização editorial | generalizar | apresentação proporcional | novo gate de frentes maduras |
| Ciclos fixos e modo adaptativo em sombra | planejamento | Segurança da agenda | preservar | `politica-adaptativa-v1.md` | testes da esteira |
| Comparação preserva originais e IDs | comparação | Auditabilidade | preservar | protocolo de comparação | testes de rastreabilidade |
| Eventos append-only | scripts e contrato | Reconstrução local | preservar | scripts e schemas | `test_eventos_aprendizagem.py` |
| Ausência de persistência automática | `AGENTS.md`, contratos e scripts | Consentimento | preservar | `persistencia-pedagogica-local.md` | `test_governanca_persistencia.py` |
| Preferência `completo` criada por default | `perfil_candidato.py` | Completar schema | generalizar | configuração explícita ou ausência | testes de perfil v2 |
| Competência por conteúdo e modalidade | perfil | Separar evidências | aprofundar | perfil v2 | `test_perfil_candidato.py` |
| Acerto encerra remediação | perfil | Fechar ciclo | aprofundar | transferência e assistência no perfil v2 | `test_ciclo_remediacao.py` |
| Testes por marcadores literais | suíte atual | Proteger contratos | realocar | literais somente quando contratuais | evals 0.6.0 |
| Rubrica humana para qualidade aberta | evals | Avaliar semântica jurídica | aprofundar | rubrica 0.6.0 | `test_evals_pedagogicos.py` |

Não há regra classificada como `remover` nesta linha de base. A separação do arquivo combinado de discursiva e oral será uma realocação: o conteúdo útil deverá aparecer integralmente nos dois destinos antes da exclusão do original.
