# Questões interativas

Cada questão é gerada dinamicamente pelo modelo, conforme o pedido e o material pertinente. Não existe banco estático de enunciados enviados previamente. A skill `estudar-direito-magistratura` governa a substância: caso concreto, dificuldade elevada, cinco alternativas, gabarito único, fundamento determinante e análise completa dos distratores.

O servidor MCP fornece capacidades operacionais: indexa Markdown autorizado, localiza trechos, cria a sessão, conserva o gabarito fora do navegador, renderiza o widget, corrige a alternativa e registra o histórico. A interface nunca substitui a verificação jurídica.

## Fontes e cautela

A geração pode combinar a biblioteca local com fontes atuais. A ordem de autoridade é Planalto para legislação, STF e STJ para jurisprudência, seguida do acervo autorizado e de fontes jurídicas editoriais confiáveis como apoio. Fonte editorial não substitui a confirmação canônica.

Quando a atualização determinante não puder ser confirmada, a questão ainda pode ser apresentada com `source_status: caution` e aviso explícito de cuidado. O usuário consegue distinguir esse caso de uma questão apoiada em fontes atuais verificadas.

## Funcionamento nas duas superfícies

- **Codex:** o plugin inicia o MCP local por `stdio`; se o componente não estiver disponível, a skill mantém o fluxo textual sem antecipar o gabarito.
- **ChatGPT:** um app privado acessa o mesmo MCP por Secure MCP Tunnel. O túnel deve estar em execução no Windows.

As respostas ficam em `.estudo-juridico/tentativas.jsonl`, e as questões em `.estudo-juridico/questoes.jsonl`. O índice e os eventos ficam na mesma subpasta. O servidor só grava quando `write_consent` está habilitado na configuração da biblioteca; os Markdown originais permanecem intactos.

## Inicialização no Windows

Após o teste manual, `scripts/install_local_service.ps1 ... -Confirm` registra o runner em `HKCU`, sem direitos administrativos. `scripts/uninstall_local_service.ps1 -Confirm` remove apenas a inicialização e os auxiliares operacionais, preservando toda a biblioteca e o histórico.
