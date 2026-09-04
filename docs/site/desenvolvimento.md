# Desenvolvimento

## Ambiente

```powershell
cd plugins/magistratura-enam-br
uv sync --all-groups
```

## Documentação principal

```powershell
uv run zensical serve
uv run zensical build --clean
```

## Fallback Material for MkDocs

```powershell
uv run mkdocs serve
uv run mkdocs build --strict --site-dir site-material
```

As dependências documentais ficam no grupo `docs` e não integram as dependências de execução do plugin. O `mkdocs.yml` é mantido compatível com os dois geradores.

## Publicação

A publicação está desabilitada. O workflow privado apenas valida os dois builds e disponibiliza o artefato para usuários autorizados do repositório.
