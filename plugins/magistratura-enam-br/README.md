# Estudos Jurídicos de Alto Nível

Plugin profissional para bacharéis em Direito voltado ao estudo de alta complexidade para Magistratura e Exame Nacional da Magistratura (ENAM). Ele reúne estudo dogmático integrado, casos, questões, curadoria de informativos, comparação de materiais e planejamento de revisão de jurisprudência.

## Skills disponíveis

| Skill | Finalidade |
| --- | --- |
| `comparar-materiais-enam` | Compara versões de materiais do ENAM por tema e subtema, com quadro de deltas rastreáveis. |
| `curar-informativos-stf-stj` | Seleciona e comenta julgados de informativos do STF e do STJ. |
| `estudar-direito-magistratura` | Integra dogmática, legislação e jurisprudência e conduz casos, objetiva, discursiva, oral e revisão. |
| `planejar-jurisprudencia` | Organiza a revisão espaçada de julgados já selecionados. |

Cada skill lê `AGENTS.md` antes de atuar. As diretrizes preservam rigor jurídico, uso proporcional de fontes oficiais, estudo ativo e fronteiras claras entre curadoria, estudo, comparação e planejamento.

## Questões interativas locais

O plugin inclui um servidor MCP local e um widget moderno para questões objetivas. O modelo continua criando cada questão dinamicamente; a skill `estudar-direito-magistratura` define substância jurídica, dificuldade, cinco alternativas, gabarito único e correção integral. O MCP indexa Markdown autorizado, mantém o gabarito fora do navegador, renderiza a atividade e grava questões e tentativas na biblioteca local.

O Codex inicia o servidor empacotado por `stdio`. O ChatGPT usa o mesmo servidor por conexão privada do Secure MCP Tunnel. Consulte [docs/chatgpt-local.md](docs/chatgpt-local.md) para configuração, inicialização automática opcional e limites de segurança.

## Ambiente de desenvolvimento

O projeto usa `uv` e Python 3.14. Instale as dependências de desenvolvimento com:

```powershell
uv sync --all-groups
```

Não crie ambiente virtual manualmente nem use `pip install` para os scripts internos. O ambiente, caches e arquivos temporários não fazem parte da distribuição.

## Validação

Execute, a partir desta pasta:

```powershell
uv lock --check
uv run python -m pytest tests skills/planejar-jurisprudencia/tests skills/comparar-materiais-enam/tests skills/curar-informativos-stf-stj/tests
uv run ruff check .
uv run python scripts/verificar_integracao.py
```

O verificador interno é somente leitura: ele valida arquivos distribuíveis, contrato do manifesto e das skills, JSON, sintaxe Python, coerência de versão e o lockfile, sem criar artefatos no código-fonte.

O workflow de raiz `.github/workflows/validar.yml` executa essa mesma sequência, no diretório do plugin, em cada `push` e pull request.

## Estrutura relevante

- `.codex-plugin/plugin.json`: manifesto canônico do plugin.
- `AGENTS.md`: diretrizes obrigatórias para manutenção e execução das skills.
- `CHANGELOG.md`: histórico de alterações publicáveis.
- `CONTINUACAO.md`: estado técnico e roteiro de manutenção.
- `mcp_server/`: indexação recursiva de Markdown, sessões privadas, histórico e transporte MCP.
- `web/`: código e artefato compilado do widget de questões.
- `modelos/pedagogia/`: schemas versionados de evento, perfil reconstruível e recomendação de revisão.
- `references/contrato-pedagogico.md`: taxonomia comum e limites de inferência entre as cinco skills.
- `references/persistencia-pedagogica-local.md`: comandos explícitos, reconstrução, exportação e exclusão dos dados locais.
- `scripts/eventos_aprendizagem.py` e `scripts/perfil_candidato.py`: log append-only e perfil reconstruível, sem rede ou caminho oculto.
- `skills/`: instruções, referências, modelos, scripts e testes de cada skill.

Consulte o [changelog](CHANGELOG.md) antes de atualizar ou publicar o plugin.
## Ambiente pedagógico profissional 0.6

A instalação funciona sem perfil e sem histórico: as cinco skills podem ser usadas diretamente, e a ausência de dados prévios é tratada como ausência de evidência. Persistência é opcional, local e acionada somente por pedido expresso, confirmação e caminho indicado pelo candidato. Leitura, uso na sessão, gravação e exclusão são autorizações distintas.

No estudo dogmático, legislação e jurisprudência entram no ponto em que instituem, delimitam, excepcionam, atualizam ou aplicam o conceito. Referências legais permanecem cirúrgicas; fontes jurisprudenciais oficiais consultadas são reunidas ao final da resposta, sem transformar a exposição em glossário ou boletim.

O acompanhamento unificado recomenda a skill adequada, mas não executa escrita nem promete memória automática. Relatórios locais são gerados apenas mediante formato explícito:

```powershell
uv run python scripts/relatorio_aprendizagem.py --entrada eventos.jsonl --inicio 2026-09-01 --fim 2026-09-30 --formato markdown
```

Planilhas antigas continuam usando a política fixa como padrão. A política adaptativa permanece em modo sombra e não substitui datas sem opt-in. O fechamento de remediação exige evento validado e confirmação explícita.
