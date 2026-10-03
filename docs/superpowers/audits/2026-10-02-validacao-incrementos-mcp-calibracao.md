# Validação dos incrementos MCP e calibração pedagógica

Execução: 2026-10-03. Branch `codex/incrementos-mcp-calibracao`, controle
`8b245f10bce3aa85fa41c2b114a46fcdc9251342`, candidata funcional
`8ac72de1fd0aa2343f1b08bb467a61b8a198eacc`. Task 8 acrescenta evidências
e documentação; não muda dependências ou comportamento do servidor/widget.

## Resultado e gates

Código validado localmente e capturas comparativas entregues. A homologação
integral continua pendente: falta revisão humana, corpus oficial selecionado
e conexão do MCP candidato no ChatGPT. Não há evidência suficiente para
afirmar que a qualidade jurídica melhorou.

| Gate | Resultado | Evidência e limite |
|---|---|---|
| Python completo | 520 aprovados, 66,21 s | Diretórios do plano; repetição final após falha intermitente inicial |
| Ruff | Aprovado | Sem erros |
| `uv lock --check` | Aprovado | 81 pacotes resolvidos; lock sem alteração |
| Integração | Aprovada | 42 verificações; antes das capturas, 53 JSON e 103 Python; evidências novas validadas novamente |
| `npm ci` | Aprovado | 250 pacotes instalados |
| `npm audit --audit-level=moderate` | Aprovado | Zero vulnerabilidades |
| Vitest | 94 aprovados em cinco arquivos | Host simulado; não comprova host ChatGPT |
| Lint TypeScript e build Vite | Aprovados | HTML autocontido de 649,09 kB; avisos PURE de Zod não impeditivos |
| Zensical e MkDocs strict | Aprovados | Builds locais; artefatos não publicados |
| Antes/depois textual | 42 capturas reais | Três sessões por caso/variante; revisão semântica pendente |
| Simulado empírico | Pendente | Nenhum corpus oficial selecionado; seis capturas testam apenas a ressalva sem corpus |
| Revisão humana identificada | Pendente | Nenhum registro com aprovação humana; rubrica posterior preservada |
| Entrega remota | Pendente de autorização específica | Sem push, CI remoto, merge, tag, release ou reinstalação nesta task |

A primeira suíte teve 519 aprovações e uma falha de conexão no teste
`test_transporte_http_local_aceita_cliente_mcp_real`. O mesmo teste passou
isoladamente (5,63 s); nova suíte completa passou (66,21 s). O teste espera
até dez segundos pela abertura da porta e descarta stderr do servidor.
A inicialização concorrente é hipótese, não causa confirmada; não houve
alteração de timeout ou relaxamento da asserção para produzir aprovação.

Comandos executados a partir da raiz, respeitando o cwd de `uv --directory`:

```powershell
uv sync --directory plugins/magistratura-enam-br --all-groups
uv run --directory plugins/magistratura-enam-br python -m pytest tests skills/planejar-jurisprudencia/tests skills/comparar-materiais-enam/tests skills/curar-informativos-stf-stj/tests -q --basetemp=.pytest-task8-final-recheck
uv run --directory plugins/magistratura-enam-br ruff check .
uv lock --directory plugins/magistratura-enam-br --check
uv run --directory plugins/magistratura-enam-br python scripts/verificar_integracao.py
uv run --directory plugins/magistratura-enam-br zensical build --clean --config-file ../../mkdocs.yml
uv run --directory plugins/magistratura-enam-br mkdocs build --strict --config-file ../../mkdocs.yml --site-dir CAMINHO_ABSOLUTO_NO_CHECKOUT
```

No diretório `plugins/magistratura-enam-br/web`, foram executados `npm ci`,
`npm audit --audit-level=moderate`, `npm test -- --run`, `npm run lint` e
`npm run build`. A task não altera dependências Python; nova auditoria do
lockfile Python não foi exigida. Bundle recompilado sem diferença no Git.

## Comparação pedagógica

Evidências em `plugins/magistratura-enam-br/evals/pedagogia/task8/`:
manifesto de proveniência, material autoral, 42 registros de execução e
sessão stdio real. Catálogo contém os sete cenários `task8-*`.

Questão direta, V/F, associação e revisão nova receberam seis capturas
cada. A ausência de corpus recebeu seis controles negativos; correções
após acerto e erro, doze capturas suplementares com questão autoral fixa
e tentativa explicitamente fornecida. Não são follow-ups de uma sessão
persistida nem correções das questões recém-geradas.

CLI 0.148.0, mesmo modelo observado `gpt-5.6-sol`, esforço padrão `none`,
mesmo material e configuração em ambas as variantes. Snapshots foram lidos
por `git show`, sem instalar o controle sobre a instalação ativa. Nome
`gpt-6.1-sol` do desktop foi rejeitado no piloto da CLI e não integra a
amostra. Revisão interna não exposta. Catálogo de skills e orientações
herdadas do ambiente são contexto compartilhado, não isolado; não houve
execução de ferramentas observada no benchmark textual.

Os 42 session IDs são diferentes. Cada combinação de caso/variante produziu
três hashes de saída distintos. O registrador validou schema, datas com
fuso, caso/saída e hashes; avaliação continua `revisao_humana_pendente`.
Rubrica não foi incluída nos prompts de geração. Leitura automatizada de
uma rodada por caso/variante observou que o controle também cumpria formatos,
ancoragem, análise A–E após acerto/erro e recusa de estatísticas sem corpus.
Isso impede atribuir esses resultados exclusivamente aos incrementos.

A revisão humana posterior deverá verificar suporte, unicidade, plausibilidade
dos distratores, correções após acerto/erro, ancoragem e ausência de solução
antecipada, com identidade/data/hashes. Contagem, diversidade textual e fonte
oficial consultada não substituem essa revisão.

O material é síntese autoral do [CPC, art. 64, §§ 2º–4º](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm),
conferido em 2026-10-03. Não foi selecionado/coletado caderno oficial, nem
foi criado perfil empírico a partir de fixture sintética.

## Matriz de clientes e apresentação

| Cliente/cenário | Situação | Escopo demonstrado |
|---|---|---|
| Codex CLI 0.148.0, texto sem MCP | Executado | 42 sessões, material legível fornecido no prompt; versão instalada da variante não testada |
| Codex CLI 0.148.0, MCP stdio | Executado | Override efêmero da definição bundled; biblioteca sintética; diagnóstico/criação/renderização/tentativa/consulta/invalidação reais |
| Codex desktop | Pendente para candidata instalada | Runtime desta tarefa não expôs ferramentas magistratura; CLI stdio não demonstra UI no desktop |
| ChatGPT web, anexo sem MCP | Executado como ensaio manual | Anexos `material.md` e instruções candidatas, chat temporário; resposta citou o arquivo e fez pergunta sem resposta antecipada |
| ChatGPT web, busca STF/STJ | Executada com problema pedagógico observado | Identificadores/datas conferidos nas fontes; tese exposta antes da questão; proteção da tentativa não aprovada |
| ChatGPT MCP-only | Pendente | Não encontrada conexão instalada do MCP candidato; plugin visível `estudo-juridico-magistratura-br` 1.0.0 é skill do Claude |
| Card com resposta/invalidação/pós-resposta/restauração/tema | Pendente em host real | Regressões SDK/bridge e widget cobertas pelos 94 testes; não equivalem à interface do ChatGPT |
| Fullscreen/retorno, recusa, conteúdo longo, mobile e permissão negada | Pendente em host real | QA sintético da task 4 e testes atuais; modo concedido pelo host é autoridade |

ChatGPT web autenticado foi acessado via Edge/CUA. Build do aplicativo e
modelo interno não estão expostos; seletor exibiu `Média`. A conexão
candidata, túnel e permissões não foram criados nem ampliados. A presença
da skill na nuvem não comprova conexão com o servidor local. Chat temporário
também pode herdar memória/instruções; o pedido restringiu explicitamente
o ensaio a material sintético e vedou gravação de memória/dados pessoais.

No stdio, a primeira criação foi rejeitada por cinco análises de distratores,
quando o schema exige quatro. O modelo corrigiu o payload, e só então a
sessão foi persistida. Resultados observaram `ready/public`,
`answered/corrected` e `invalidated/public`, sem campos privados antes da
tentativa e após invalidação. CLI não abriu card; `renderizar_questao`
bem-sucedido confirma retorno do protocolo, não apresentação visual.

Dois controles suplementares, uma sessão candidata por caso, trataram
anexo ilegível e notícia sem fundamentos. O modelo reconheceu a falta
de conteúdo recuperável/regra e solicitou material apto, sem fabricar
questão. São registros reais com rubrica pendente, não comparação repetida.

A busca nativa do ChatGPT produziu referências ao STF RE 1.362.742/Tema
1.258 e ao STJ REsp 2.222.626/Tema 1.419. A conferência direta no navegador
confirmou a sessão STF de 28/8 a 4/9/2026, registro de julgamento em 8/9,
e, no STJ, julgamento em 20/8/2026 e publicação em 27/8. A leitura automática
externa retornou 403/indisponibilidade; o navegador permitiu conferir o STF
e, após verificação automática e pesquisa na própria UI, o STJ. Não houve
solução manual de CAPTCHA. Links/estado estão em `chatgpt-host.json`.

**Achado comportamental:** a resposta de pesquisa expôs a tese do STF antes
da questão, antecipando seu fundamento decisivo. Ausência de letra explícita
não elimina esse vazamento indireto. O ensaio manual de busca/questão não
recebe aprovação da proteção pré-tentativa. Não foi alterada a instrução
para alegar correção sem uma nova avaliação limpa; esse fluxo permanece
gate de homologação pedagógica. Revisão humana e reprodução com candidata
instalada, isolando a pesquisa da apresentação ao estudante, são necessárias.

Na amostra de associação lida após geração, controle e candidata também
não explicitaram a regra de reutilização dos vínculos. Formato reconhecível
não comprova cumprimento integral da orientação de autoria. Registrar esse
ponto na rubrica, sem inferir melhoria pelo nome do formato.

## Entrega proposta e rollback

Proposta: **0.8.0** para o conjunto MCP + pedagogia, sujeita ao diff final
e aos gates acima. O manifesto permanece 0.7.5; esta proposta não cria
release nem certifica revisão jurídica ou simulado empírico.

Após autorização específica, a cadeia é: versionar manifesto/metadados,
commit/push, CI, integração, tag/release e reinstalação. Conferir árvore
publicada versus cache instalado e abrir tarefa nova. Retomar os cenários
visuais no ChatGPT com conexão da candidata identificada e registrar build,
capacidades e resultado concedido; SDK ou estado persistido não fecham esse gate.

Rollback: voltar ao snapshot/tag `v0.7.5` do marketplace e reinstalar;
preservar acervo, configuração e registros. Comparar cache com a tag e
usar nova tarefa. Nenhuma operação de rollback foi necessária/executada.
MCP Events, upload dentro do card, OCR e monitoramento continuam fora do escopo.

## Revisão integral da branch

Revisão independente do intervalo `8b245f1..HEAD` será registrada após
conclusão dos gates e documentação. Os achados e decisões finais serão
incluídos neste relatório antes do encerramento da task.
