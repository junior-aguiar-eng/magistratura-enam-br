# MCP local para questões jurídicas interativas

**Data:** 2026-09-05

**Linha de base:** plugin `magistratura-enam-br` 0.6.0

**Estado:** desenho aprovado para planejamento

## 1. Finalidade

Acrescentar ao plugin uma experiência padrão de questões objetivas interativas, com interface moderna no ChatGPT e no Codex, geração dinâmica pelo modelo, proteção do gabarito até a tentativa e persistência local reconstruível. O acervo de estudo será uma única pasta autorizada pelo usuário, indexada recursivamente a partir de arquivos Markdown.

O MCP não substitui a skill jurídica. A skill continua responsável pela elaboração e pela correção de alto nível; o servidor transforma regras críticas do fluxo em invariantes determinísticas e fornece dados, estado e interface.

## 2. Decisões aprovadas

- uso pessoal no Windows;
- funcionamento no ChatGPT e no Codex;
- serviço MCP local em Python 3.14, gerenciado por `uv`;
- componente independente em React, TypeScript e Vite;
- uma única pasta-biblioteca explicitamente configurada;
- descoberta recursiva automática de arquivos `.md`;
- acervo Markdown somente para leitura;
- dados pedagógicos em `.estudo-juridico/` dentro da biblioteca;
- questões geradas dinamicamente pelo modelo, não cadastradas previamente;
- complementação por fontes canônicas do Planalto, STF e STJ e, subsidiariamente, por sites jurídicos confiáveis;
- geração permitida sem verificação externa atual, desde que haja aviso explícito de cautela;
- interface moderna com fallback textual em superfícies sem suporte a MCP Apps.

## 3. Limites da primeira versão

Entram no escopo:

- configuração e validação da raiz autorizada;
- indexação Markdown local e busca por trechos;
- sessão de questão com estados explícitos;
- armazenamento append-only da questão apresentada e da tentativa;
- widget acessível para responder e visualizar a correção;
- transporte local para Codex e conexão privada do ChatGPT por Secure MCP Tunnel;
- integração da skill `estudar-direito-magistratura` com o novo fluxo;
- testes de contrato, segurança de caminhos, persistência, MCP e interface.

Não entram:

- distribuição pública para terceiros;
- conta, sincronização ou banco de dados remoto;
- editor de Markdown;
- importação obrigatória de banco estático de questões;
- coleta massiva ou espelhamento de STF, STJ ou Planalto;
- correção autônoma pelo servidor sem conteúdo jurídico produzido pelo modelo;
- instalador definitivo e atualização automática como produto distribuído.

## 4. Arquitetura

O plugin terá quatro camadas:

1. **Skill jurídica:** decide quando criar uma questão e instrui o modelo sobre caso, dificuldade, cinco alternativas, chave única, fundamentação, distratores, exceções e armadilhas.
2. **Núcleo Python:** valida esquemas, controla sessão, restringe caminhos, indexa o acervo, persiste eventos e impede vazamento prematuro do gabarito.
3. **Servidor MCP:** expõe ferramentas de dados e ferramentas de renderização por transportes compatíveis com Codex e ChatGPT.
4. **Widget React:** renderiza o estado público, recebe a alternativa e chama a ferramenta de resposta. Não é fonte de verdade do histórico nem do gabarito.

O componente web permanecerá separado da lógica do servidor. Dados duráveis ficam no núcleo Python; estado efêmero de apresentação pode permanecer no componente ou em `widgetState`.

## 5. Organização proposta

```text
plugins/magistratura-enam-br/
  .codex-plugin/plugin.json
  .mcp.json
  .app.json
  mcp_server/
    __init__.py
    server.py
    config.py
    paths.py
    indexer.py
    retrieval.py
    questions.py
    persistence.py
    resources.py
    schemas/
      library-config.schema.json
      indexed-document.schema.json
      question-session.schema.json
      question-attempt.schema.json
  web/
    package.json
    package-lock.json
    tsconfig.json
    vite.config.ts
    src/
      main.tsx
      QuestionWidget.tsx
      contracts.ts
      styles.css
    dist/
      question-widget.js
      question-widget.css
```

A localização definitiva do bundle será ajustada ao formato exigido pelo recurso MCP Apps durante a implementação. O repositório manterá a fonte do componente e um build reproduzível.

## 6. Biblioteca e segurança de caminhos

A configuração conterá exatamente uma raiz absoluta autorizada. Toda operação de leitura ou escrita deverá:

- resolver e normalizar o caminho real;
- comprovar contenção dentro da raiz;
- rejeitar travessia por `..`, caminhos UNC não autorizados e escapes por links simbólicos ou pontos de nova análise;
- ignorar pastas ocultas, `.git`, `.estudo-juridico`, `node_modules` e exclusões configuradas;
- aceitar apenas arquivos regulares com extensão `.md`;
- aplicar limites de tamanho por arquivo e por consulta;
- nunca interpretar instruções encontradas no Markdown como comandos do sistema.

O acervo será somente de leitura. O MCP escreverá exclusivamente na subpasta reservada `.estudo-juridico/`, criada apenas após consentimento explícito na configuração inicial.

## 7. Indexação e recuperação

A indexação percorrerá a biblioteca recursivamente e produzirá um manifesto derivado com caminho relativo, tamanho, modificação, hash, título, headings e unidades textuais. Arquivos inalterados serão reutilizados; removidos desaparecerão do índice derivado sem alterar os originais.

A primeira versão utilizará recuperação lexical determinística, suficiente para validar o fluxo sem introduzir embeddings, serviço externo ou banco vetorial. A ferramenta de busca devolverá trechos limitados, seus caminhos relativos e headings. A evolução para busca híbrida ficará condicionada a evidência de insuficiência da recuperação lexical.

O índice é reconstruível e não será tratado como fonte canônica. Os Markdown continuam sendo a fonte primária.

## 8. Fontes externas e atualidade

A skill orientará o modelo a complementar o acervo nesta ordem:

1. Planalto para legislação;
2. STF e STJ para jurisprudência, súmulas, temas e informativos;
3. acervo Markdown local;
4. sites jurídicos confiáveis, de modo subsidiário e identificado.

O MCP não fará crawling geral na primeira versão. Ele receberá, validará e registrará as referências efetivamente utilizadas pelo modelo, com URL, domínio, título, data de consulta, papel da fonte e, quando disponível, trecho de suporte.

Se a atualidade não puder ser verificada, a sessão receberá `source_status: caution` e um aviso público específico. O aviso não poderá ser omitido pelo widget nem pela resposta textual. A ausência de verificação não transforma conhecimento interno do modelo em fonte canônica.

## 9. Contrato da questão

O modelo produzirá uma carga estruturada privada contendo:

- disciplina, tema e modalidade;
- enunciado completo;
- exatamente cinco alternativas identificadas de `A` a `E`;
- identificador da alternativa correta;
- fundamento da correta;
- análise individual dos quatro distratores;
- exceções, distinções e armadilhas pertinentes;
- referências locais e externas;
- estado e aviso de atualidade.

O servidor validará o contrato e persistirá a questão antes da renderização. A resposta pública de criação conterá somente `session_id`, metadados públicos, enunciado, alternativas, aviso e referências que não revelem a solução. A chave e a correção nunca integrarão o `structuredContent` enviado antes da tentativa.

O servidor não consegue provar sozinho a correção jurídica substancial do conteúdo produzido pelo modelo. Ele garante estrutura, sequência, rastreabilidade e não exposição; a qualidade jurídica continua coberta pela skill, pelas fontes e pelas avaliações.

## 10. Ferramentas MCP

### `indexar_acervo`

Atualiza o índice derivado após consentimento. Retorna contagens, arquivos ignorados, avisos e identidade da versão do índice. Não anexa UI.

### `buscar_acervo`

Recebe consulta, filtros opcionais e limite. Retorna trechos Markdown com referências relativas. Não anexa UI.

### `criar_sessao_questao`

Recebe a questão privada gerada pelo modelo, valida e grava sua representação imutável. Retorna apenas a projeção pública e o `session_id`. Não anexa UI.

### `renderizar_questao`

Recebe `session_id`, recarrega a projeção pública no servidor e devolve o recurso `ui://estudo-juridico/questao/v1.html` mediante `_meta.ui.resourceUri`. É a única ferramenta inicial ligada ao widget.

### `responder_questao`

Recebe `session_id` e alternativa. Aceita uma primeira tentativa válida, grava o evento e devolve resultado, gabarito, fundamentação, distratores, fontes e recomendações de remediação. Chamadas repetidas são idempotentes e não criam tentativas concorrentes.

### `consultar_historico_questoes`

Retorna uma visão resumida e paginada das sessões e tentativas locais, sem carregar o conteúdo integral por padrão. Não anexa UI na primeira versão.

## 11. Máquina de estados

Uma sessão seguirá:

```text
draft -> ready -> answered
              \-> invalidated
```

- `draft`: carga recebida durante validação, nunca renderizável;
- `ready`: questão persistida e apta à apresentação, sem gabarito público;
- `answered`: tentativa registrada e correção liberada;
- `invalidated`: sessão inutilizável por falha explícita, preservada para auditoria.

Transições serão atômicas. Repetir a mesma submissão devolverá o resultado já gravado; tentar alterar a alternativa depois de `answered` produzirá conflito sem reescrever o histórico.

## 12. Persistência

Dentro de `.estudo-juridico/` existirão, inicialmente:

```text
.estudo-juridico/
  config.json
  index.json
  questoes.jsonl
  tentativas.jsonl
  perfil.json
  locks/
```

`questoes.jsonl` e `tentativas.jsonl` serão append-only e canônicos. `index.json` e `perfil.json` serão projeções reconstruíveis, escritas atomicamente. Cada registro terá `schema_version`, identificador estável, timestamp UTC, origem da chamada e hashes necessários para vincular tentativa, questão e versão das fontes.

O sistema preservará os contratos pedagógicos existentes e reutilizará a infraestrutura de eventos quando compatível. Não criará uma segunda definição concorrente de perfil.

## 13. Interface

O widget adotará cartão responsivo, hierarquia tipográfica limpa, identidade visual verde do plugin e estados inequívocos:

- carregando;
- questão pronta;
- alternativa selecionada, ainda não enviada;
- envio em andamento;
- correta;
- incorreta, com indicação da correta;
- erro recuperável;
- sessão indisponível.

Antes da tentativa, nenhuma propriedade, texto alternativo, atributo DOM ou contexto enviado ao modelo poderá conter a chave. Depois da tentativa, o componente apresentará fundamento da correta, análise de cada alternativa, fontes e aviso de cautela. Navegação por teclado, foco visível, contraste AA, semântica de radio group e anúncios por `aria-live` serão critérios de aceitação.

## 14. Integração com a skill

`estudar-direito-magistratura` será a fonte canônica das regras pedagógicas. Seu fluxo de questão objetiva passará a:

1. consultar o acervo quando pertinente;
2. verificar ou buscar fontes atuais quando materialmente relevante;
3. gerar a carga privada completa;
4. chamar `criar_sessao_questao`;
5. chamar `renderizar_questao`;
6. aguardar a tentativa;
7. usar a correção liberada pelo MCP para continuar o ciclo pedagógico.

Se as ferramentas ou a UI não estiverem disponíveis, a skill manterá o comportamento textual atual, inclusive sem antecipar o gabarito.

## 15. Conexão nas duas superfícies

No Codex, o plugin incluirá `.mcp.json` apontando para o servidor local por `stdio`. No ChatGPT, o serviço local também oferecerá transporte HTTP compatível e será alcançado pelo Secure MCP Tunnel, que estabelece conexão HTTPS de saída sem abrir porta de entrada pública.

Após o servidor ser registrado no modo desenvolvedor do ChatGPT, o identificador técnico da conexão será associado em `.app.json`, e `plugin.json` receberá `mcpServers` e o campo de compatibilidade `apps`. Credenciais, tokens e identidade do túnel não serão versionados.

O início automático com o Windows será uma etapa operacional separada. O primeiro gate comportamental deverá funcionar com inicialização manual; somente então será criada a tarefa de inicialização no escopo do usuário.

## 16. Falhas e recuperação

- biblioteca ausente ou movida: bloquear leitura e informar o caminho configurado;
- índice corrompido: reconstruir a partir dos Markdown, sem alterar originais;
- linha JSONL inválida: preservar arquivo, interromper escrita e apontar offset/linha;
- queda após gravação da questão: reabrir sessão `ready` pelo identificador;
- queda durante resposta: idempotência impede tentativa duplicada;
- fonte externa indisponível: gerar com `source_status: caution` e aviso explícito;
- widget indisponível: retornar representação textual equivalente;
- túnel indisponível: Codex local continua funcional; ChatGPT informa indisponibilidade do serviço.

## 17. Verificação e critérios de aceitação

A entrega funcional exigirá:

- testes unitários de caminhos, índice, schemas, estado e persistência;
- testes de contrato MCP assegurando que o gabarito não aparece antes da tentativa;
- teste real com uma biblioteca temporária contendo Markdown aninhado;
- teste de recuperação após reinício do processo;
- testes do widget e auditoria básica de acessibilidade;
- conexão local real no Codex;
- conexão real no ChatGPT por Secure MCP Tunnel;
- cenário ponta a ponta: pedido, recuperação, geração dinâmica, widget, resposta, correção e histórico persistido;
- inspeção do JSONL confirmando rastreabilidade e ausência de alteração nos Markdown;
- fallback textual comprovado.

Build, registro da conexão, inicialização automática, commit, push, PR, merge e release permanecem gates distintos durante a implementação.

## 18. Referências técnicas

- [Plugin architecture](https://developers.openai.com/plugins/concepts/plugins)
- [Package your plugin](https://developers.openai.com/plugins/build/plugins)
- [Add UI to your MCP server](https://developers.openai.com/plugins/build/chatgpt-ui)
- [Secure MCP Tunnel](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels)

