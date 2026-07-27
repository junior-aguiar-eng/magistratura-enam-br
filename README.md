# Magistratura e ENAM Brasil

Marketplace local e compartilhável do plugin **Magistratura e ENAM Brasil** (versão 0.2.1).

## Instalação por ZIP no Windows

1. Descompacte esta pasta em um local permanente.
2. Abra o PowerShell dentro da pasta descompactada.
3. Execute `./INSTALAR.ps1`.
4. Abra uma nova tarefa no Codex.

Para também instalar as dependências usadas pelos scripts de PDF e planilha, execute `./INSTALAR.ps1 -InstalarDependencias`.

O instalador registra somente esta marketplace local e instala o plugin. Não envia arquivos, dados de estudo ou credenciais.

## Uso em GitHub

Publique o conteúdo desta pasta como a raiz de um repositório Git. Depois, cada usuário poderá executar:

```powershell
codex plugin marketplace add proprietario/repositorio --ref main
codex plugin add magistratura-enam-br@magistratura-enam-br
```

Para manter o material restrito a um grupo, utilize um repositório privado e conceda acesso apenas às pessoas autorizadas.
