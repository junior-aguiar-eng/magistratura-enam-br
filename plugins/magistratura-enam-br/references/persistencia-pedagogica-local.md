# Persistência pedagógica local

A persistência é opcional, local e acionada apenas por comando com caminho explícito. As skills não gravam histórico durante a conversa nem presumem log ou perfil.

```powershell
uv run python scripts/eventos_aprendizagem.py validate --evento evento.json
uv run python scripts/eventos_aprendizagem.py append --log C:\dados\eventos.jsonl --evento evento.json
uv run python scripts/perfil_candidato.py rebuild --log C:\dados\eventos.jsonl --perfil C:\dados\perfil.json
uv run python scripts/perfil_candidato.py export --log C:\dados\eventos.jsonl --perfil C:\dados\perfil.json --saida C:\dados\exportacao.json
```

O diretório do log só é criado com `--criar-diretorio`. O JSONL é a fonte append-only; o perfil pode ser apagado e reconstruído. Apagar o perfil não remove o histórico, enquanto apagar o log elimina a fonte de reconstrução. A exclusão é feita separadamente pelo candidato.

Nenhuma operação envia dados pela rede. Não registre nome, CPF, matrícula, e-mail, resposta integral ou conteúdo integral de anexos.
