# Desenvolvimento

## Ambiente

Na raiz do repositório:

```powershell
uv sync --project plugins/magistratura-enam-br --all-groups
```

## Documentação principal

```powershell
uv run --project plugins/magistratura-enam-br zensical serve --config-file mkdocs.yml
uv run --project plugins/magistratura-enam-br zensical build --clean --config-file mkdocs.yml
```

## Fallback Material for MkDocs

```powershell
uv run --project plugins/magistratura-enam-br mkdocs serve --config-file mkdocs.yml
uv run --project plugins/magistratura-enam-br mkdocs build --strict --config-file mkdocs.yml --site-dir site-material
```

As dependências documentais ficam no grupo `docs` e não integram as dependências de execução do plugin. O `mkdocs.yml` é mantido compatível com os dois geradores.

## Gates dos incrementos 0.8.0

A branch `codex/incrementos-mcp-calibracao` reúne as tasks 1–8 e mantém o
manifesto 0.8.0. A validação local aprova Python, Ruff, lockfile, integração,
widget e os dois builds documentais. Capturas de sessões, ensaio de anexo
no ChatGPT e MCP stdio na CLI são evidências distintas; não aprovam por si
sós mérito jurídico, corpus oficial ou fullscreen em host real.

As 42 capturas e a sessão stdio estão em
`plugins/magistratura-enam-br/evals/pedagogia/task8/`. O relatório canônico
é `docs/superpowers/audits/2026-10-02-validacao-incrementos-mcp-calibracao.md`.
O corpus oficial ENAM 2026.1 foi adquirido e os achados comportamentais
receberam instruções específicas e doze novas capturas. Revisão humana,
classificação aprovada do corpus e conexão/card real continuam gates
separados da publicação. Push/release/reinstalação foram autorizados;
a conclusão operacional exige CI e conferência da árvore/cache.

## Publicação do site documental

A publicação está desabilitada. O workflow privado apenas valida os dois builds e disponibiliza o artefato para usuários autorizados do repositório.
