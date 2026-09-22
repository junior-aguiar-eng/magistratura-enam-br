<p align="center">
  <img src="plugins/magistratura-enam-br/assets/magistratura-enam-br.png" width="156" alt="Monograma NJ do Estudo Jurídico Avançado">
</p>

<h1 align="center">Estudo Jurídico Avançado</h1>

<p align="center">
  Ambiente privado de aprendizagem jurídica para Magistratura e ENAM, integrado ao Codex.
</p>

<p align="center">
  <a href="plugins/magistratura-enam-br/.codex-plugin/plugin.json"><img alt="Versão 0.7.2" src="https://img.shields.io/badge/vers%C3%A3o-0.7.2-006B4F"></a>
  <a href="plugins/magistratura-enam-br/pyproject.toml"><img alt="Python 3.14" src="https://img.shields.io/badge/Python-3.14-1F6F54"></a>
  <a href="https://github.com/junior-aguiar-eng/magistratura-enam-br/actions/workflows/validar.yml"><img alt="Validação" src="https://github.com/junior-aguiar-eng/magistratura-enam-br/actions/workflows/validar.yml/badge.svg"></a>
  <a href="https://github.com/junior-aguiar-eng/magistratura-enam-br/actions/workflows/docs.yml"><img alt="Documentação" src="https://github.com/junior-aguiar-eng/magistratura-enam-br/actions/workflows/docs.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="Licença proprietária" src="https://img.shields.io/badge/licen%C3%A7a-propriet%C3%A1ria-B08A3E"></a>
</p>

<p align="center">
  <a href="#instalação-no-windows">Instalação</a> ·
  <a href="docs/site/index.md">Documentação completa</a> ·
  <a href="docs/site/arquitetura-pedagogica.md">Arquitetura pedagógica</a> ·
  <a href="plugins/magistratura-enam-br/CHANGELOG.md">Changelog</a>
</p>

---

## Visão geral

O **Estudo Jurídico Avançado** reúne cinco skills especializadas para estudo, curadoria, comparação de materiais, revisão de jurisprudência e acompanhamento pedagógico. O identificador técnico permanece `magistratura-enam-br` para preservar compatibilidade com instalações e marketplaces existentes.

O plugin prioriza rigor jurídico, prática deliberada, feedback explicativo, recuperação espaçada e rastreabilidade. Não presume memória automática, não cria perfil sem autorização e não interpreta ausência de dados como desempenho insuficiente.

As questões objetivas também podem usar um servidor MCP local e um widget interativo. O modelo gera o conteúdo jurídico; o servidor mantém o gabarito fora do navegador até a tentativa e registra questões e respostas somente na biblioteca local autorizada. No Codex, a conexão é por `stdio`; no ChatGPT, depende de um túnel privado configurado separadamente. Consulte [Questões interativas](docs/site/questoes-interativas.md) e [Conexão privada com o ChatGPT](plugins/magistratura-enam-br/docs/chatgpt-local.md).

## Capacidades

| Skill | Finalidade | Limite principal |
|---|---|---|
| `estudar-direito-magistratura` | Explicações, questões e correções de alto nível | Não substitui curadoria integral de informativos |
| `curar-informativos-stf-stj` | Seleção e comentário de julgados do STF e STJ | Exige documento ou identificação oficial suficiente |
| `comparar-materiais-enam` | Identificação de alterações jurídicas e editoriais | Não inventa versões, páginas ou supressões |
| `planejar-jurisprudencia` | Esteira de julgados e revisão espaçada | Preserva a política fixa sem adaptação silenciosa |
| `acompanhar-percurso-magistratura` | Roteamento e consolidação do percurso | Não executa automaticamente a skill indicada |

## Seis entradas naturais

Os gatilhos do Codex representam seis intenções: jornada guiada, estudo de tema, treino por questão, curadoria de informativo, comparação de materiais e revisão de julgados. Somente a jornada guiada apresenta o ambiente; pedidos diretos seguem para a rota correspondente sem repetir introdução.

| Intenção | Entrada natural |
|---|---|
| Jornada guiada | “Apresente o ambiente e ajude-me a escolher um percurso.” |
| Estudo | “Quero estudar um tema jurídico em profundidade.” |
| Treino | “Quero treinar com uma questão jurídica difícil.” |
| Informativos | “Quero curar um informativo oficial do STF ou STJ.” |
| Comparação | “Quero comparar duas versões de material do ENAM.” |
| Revisão | “Quero organizar a revisão dos julgados que já selecionei.” |

## Instalação no Windows

O plugin não é um aplicativo `.exe`. A instalação registra este repositório como marketplace local no perfil do Codex e coloca a versão selecionada no cache do usuário Windows.

É necessário ter o Codex CLI. Para usar o servidor MCP de questões, `uv` deve estar disponível no `PATH`; a versão do Python é fixada em `plugins/magistratura-enam-br/.python-version` e as dependências em `plugins/magistratura-enam-br/uv.lock`. O túnel privado do ChatGPT é opcional e exige configuração própria.

### Por ZIP

1. Baixe e descompacte o repositório em uma pasta permanente.
2. Abra o PowerShell nessa pasta.
3. Execute:

```powershell
.\INSTALAR.ps1
```

Para preparar as dependências Python do plugin, inclusive as usadas pelo MCP e pelos scripts de PDF e planilha:

```powershell
.\INSTALAR.ps1 -InstalarDependencias
```

Depois da instalação, abra uma nova tarefa no Codex. O instalador não envia arquivos, credenciais ou dados de estudo.

### Pelo marketplace Git

```powershell
codex plugin marketplace add junior-aguiar-eng/magistratura-enam-br --ref v0.7.2
codex plugin add magistratura-enam-br@magistratura-enam-br
```

Esse comando instala a tag `v0.7.2`. Como o repositório é privado, esse método exige autenticação no GitHub e permissão de leitura. A instalação é local por computador e não é sincronizada automaticamente.

## Arquitetura do repositório

```text
.
├── .agents/plugins/marketplace.json       # catálogo reconhecido pelo Codex
├── .github/workflows/                     # validação do plugin e da documentação
├── docs/
│   ├── README.md                          # índice documental do repositório
│   ├── site/                              # conteúdo do site privado
│   └── superpowers/                       # especificações e planos internos
├── plugins/magistratura-enam-br/
│   ├── .codex-plugin/plugin.json          # manifesto canônico
│   ├── skills/                            # cinco skills distribuídas
│   ├── references/                        # contratos e governança pedagógica
│   ├── scripts/                           # utilitários locais
│   ├── tests/                             # contratos automatizados
│   └── evals/                             # avaliações comportamentais
├── INSTALAR.ps1                           # instalação local no Windows
└── mkdocs.yml                             # Zensical e fallback Material
```

## Documentação

- [Apresentação e navegação](docs/site/index.md)
- [Primeiros passos](docs/site/primeiros-passos.md)
- [Arquitetura pedagógica](docs/site/arquitetura-pedagogica.md)
- [Catálogo das skills](docs/site/skills/index.md)
- [Privacidade e persistência](docs/site/privacidade-e-persistencia.md)
- [Desenvolvimento](docs/site/desenvolvimento.md)

O site é construído prioritariamente com Zensical e validado também com Material for MkDocs. A publicação pública está desabilitada; o CI disponibiliza o artefato apenas no workflow privado do repositório.

## Desenvolvimento e qualidade

O ambiente usa Python 3.14 e `uv`. As dependências de documentação ficam no grupo `docs`, sem ampliar as dependências de execução do plugin.

```powershell
uv sync --project plugins/magistratura-enam-br --all-groups
uv run --project plugins/magistratura-enam-br python -m pytest
uv run --project plugins/magistratura-enam-br ruff check plugins/magistratura-enam-br
```

Os contratos automatizados não substituem a avaliação comportamental das skills nem a revisão humana dos gates pedagógicos.

## Privacidade e licença

Perfil, eventos e relatórios locais só podem ser persistidos mediante pedido expresso, destino definido e confirmação correspondente. Materiais do candidato e registros de aprendizagem não integram o site documental.

Copyright © 2026 Boni Jr. Todos os direitos reservados. Consulte a [licença](LICENSE) antes de copiar, redistribuir ou criar trabalhos derivados.
