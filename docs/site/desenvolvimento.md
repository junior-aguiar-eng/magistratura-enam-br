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

## Publicação

A publicação está desabilitada. O workflow privado apenas valida os dois builds e disponibiliza o artefato para usuários autorizados do repositório.
