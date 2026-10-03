# Regressões de preparação da release 0.8.0

Execução em 2026-10-03 após autorização para resolver pendências e publicar.
Controle `c6dbd85`; candidata congelada por conteúdo/hash no `manifest.json`.
Versão dos manifestos durante a captura: 0.7.5; esses ensaios antecedem o bump.

Doze sessões reais da CLI 0.148.0: dois casos, duas variantes, três sessões
novas por combinação. Modelo observado gpt-5.6-sol, esforço none, revisão
interna não exposta. Instruções congeladas no prompt; catálogo compartilhado
não isolado; sem chamadas de ferramentas observadas. Fonte jurídica fornecida
após conferência oficial anterior, sem busca ao vivo nessas sessões.
Pedido de geração não contém resultados esperados nem rubrica.

Leitura automatizada das doze saídas observou:

- Pesquisa com fonte fornecida: controle e candidata entregaram somente
  enunciado/alternativas nas três sessões, sem síntese prévia da regra.
  O controle também passou; não é prova de ganho ou reprodução da falha web.
- Associação: candidata declarou uso único das opções nas três sessões;
  controle omitiu a regra em uma e declarou nas duas restantes. Na terceira
  saída do controle, a ordem declarada e os vetores também exigem revisão.

As instruções candidatas eliminam o conflito entre `Base consultada` e
proteção pré-tentativa e exigem regra de reutilização no prompt público.
O comportamento observado não garante obediência universal ou validade jurídica.
Todos os registros continuam `revisao_humana_pendente`.

A captura inicial produziu as doze saídas, mas o registrador encontrou o
diretório `runs` ausente. Os registros foram recuperados dos arquivos UTF-8
inalterados e respectivos cabeçalhos da CLI, sem repetir geração. `executed_at`
registra o mtime observado da saída, como término, não início presumido.
Diagnósticos originais de registro permanecem no manifesto.

[Pacote concreto de revisão humana](revisao-humana.md), separado da
homologação de instalação/MCP e da aquisição do corpus oficial.
