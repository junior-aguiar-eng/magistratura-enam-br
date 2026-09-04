# Instalação

## Requisitos

- Codex com suporte a plugins;
- Git e acesso autenticado ao repositório privado;
- autorização de leitura no GitHub;
- uma nova tarefa do Codex após a instalação.

## Versão estável

```powershell
codex plugin marketplace add junior-aguiar-eng/magistratura-enam-br --ref v0.4.0
codex plugin add magistratura-enam-br@magistratura-enam-br
```

A instalação é local por computador. Ela não é sincronizada automaticamente entre máquinas ou usuários.

## Atualização

Cada release deve ser consumida por tag explícita. Atualize o snapshot do marketplace para a nova tag, reinstale o plugin e abra uma nova tarefa para carregar a nova versão.

!!! warning "Acesso privado"
    Uma GitHub Release não torna público um repositório privado. Somente contas autorizadas conseguem obter o marketplace e instalar o plugin.
