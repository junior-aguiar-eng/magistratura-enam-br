# Persistência pedagógica local

A persistência é opcional, local e acionada apenas por comando com caminho explícito. As skills não gravam histórico durante a conversa nem presumem log ou perfil. Leitura, uso na sessão, gravação e exclusão são autorizações distintas. Carregar um perfil não autoriza nova escrita; escolher usá-lo em uma sessão não autoriza atualizá-lo.

## Operações

```powershell
uv run python scripts/eventos_aprendizagem.py validate --evento evento.json
uv run python scripts/eventos_aprendizagem.py append --log C:\dados\eventos.jsonl --evento evento.json --confirmar-gravacao-local
uv run python scripts/perfil_candidato.py inspect --perfil C:\dados\perfil.json
uv run python scripts/perfil_candidato.py rebuild --log C:\dados\eventos.jsonl --perfil C:\dados\perfil.json --config C:\dados\preferencias.json --confirmar-gravacao-local
uv run python scripts/perfil_candidato.py export --log C:\dados\eventos.jsonl --perfil C:\dados\perfil.json --saida C:\dados\exportacao.json --confirmar-gravacao-local
uv run python scripts/perfil_candidato.py delete --perfil C:\dados\perfil.json --confirmar-exclusao-local
```

`inspect` é somente leitura. `append`, `rebuild` e `export` exigem confirmação de gravação local. `delete` exige confirmação própria e remove apenas o arquivo indicado; apagar perfil derivado não remove o log. O diretório do log só é criado com `--criar-diretorio`, também acompanhado da confirmação de gravação.

O JSONL é a fonte append-only; o perfil pode ser apagado e reconstruído. A configuração opcional contém apenas objetivos e preferências declarados. Sem configuração, o perfil não inventa objetivos, modalidade preferida ou modo de feedback.

Nenhuma operação envia dados pela rede. Não registre nome, CPF, matrícula, e-mail, resposta integral ou conteúdo integral de anexos.
