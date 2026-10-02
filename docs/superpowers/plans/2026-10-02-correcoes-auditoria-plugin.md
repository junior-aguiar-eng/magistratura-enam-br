# Correções da auditoria do plugin

**Objetivo:** corrigir os sete achados da auditoria de 02/10/2026, mantendo a fonte canônica, dados existentes e contratos públicos compatíveis sempre que possível.

**Arquitetura:** evolução incremental do repositório de questões e das projeções pedagógicas; SDK MCP Apps no widget; benchmark com revisão e registro de execução verificáveis.

**Tecnologias:** Python 3.14, JSON Schema, pytest, React/TypeScript, MCP Apps e Vitest.

**Especificação:** os sete achados aceitos pelo usuário nesta conversa e os contratos em `plugins/magistratura-enam-br/AGENTS.md`.

## Restrições e decisões

- Trabalhar na branch existente, preservando as alterações anteriores. Não instalar, publicar, migrar acervo real, commitar ou fazer push nesta execução.
- Testes usam dados sintéticos. Revisão humana e renderização em host real não serão declaradas sem execução.
- Logs de tentativas permanecem append-only; invalidações devem excluir resultados das projeções, sem apagar as tentativas.
- Os eventos novos não inferem tipo de erro, domínio, assistência ou versão da fonte a partir da letra escolhida.
- As fases compartilham o contrato de sessão invalidada e a projeção efetiva de eventos; testes exercitam retries, eventos antigos, erros de transporte e revisão pendente.

## Execução

- [x] 1. Adicionar regressões para eventos sem inferências e retry com eventos legados; corrigir `mcp_server/questions.py` e schema de eventos.
- [x] 2. Testar invalidação antes/depois da resposta, retry e histórico; expor `invalidar_questao`, preservar tentativa e excluir seus efeitos em perfil/relatório.
- [x] 3. Testar inicialização, chamada, retorno e erro do SDK; substituir bridge manual em `web/src/QuestionWidget.tsx`, preservando suporte a `window.openai`.
- [x] 4. Testar reconstrução de índice inválido com consentimento e preservação em falha; corrigir `StudyService.index_library`.
- [x] 5. Testar cobertura dos distratores, fontes verificadas vazias e rastreabilidade; validar semântica de novas sessões sem inutilizar logs antigos.
- [x] 6. Testar e renderizar fontes, exceções, armadilhas e estado invalidado no card após tentativa, sem revelar correção antecipadamente.
- [x] 7. Permitir revisão fundamentada do benchmark e registrar saídas reais com versões, identidade da execução e avaliação; não converter pendência em aprovação fictícia.
- [x] 8. Atualizar documentação, executar suíte Python, Ruff, integração, testes/tipos/build do widget e revisar o diff completo.

Para cada correção: escrever e executar a regressão, confirmar a falha esperada, implementar e executar novamente. Resultados e decisões materiais serão registrados abaixo.

## Registro de execução

- Baseline auditado: 334 testes Python, 4 do widget, TypeScript, Ruff e 42 verificações de integração aprovados. Falhas confirmadas por reproduções adicionais.

- Regressões iniciais: 10 falhas Python reproduzidas antes das correções; 45 testes relacionados aprovados após a primeira implementação.
- Widget: testes com SDK real e host simulado cobrem handshake, tools/call, erro, resultado pendente e correção completa. Nenhuma homologação visual do host foi presumida.
- Benchmark: a revisão humana fornecida é vinculada por hashes ao caso e à saída; metadados, evidência por critério e confirmação de gravação são verificados. As fixtures reais permanecem pendentes; fixtures de teste são identificadas como sintéticas.
- Revisão independente somente leitura encontrou três P2: regressão de estado por notificação atrasada, payload malformado quebrando render e revisão reutilizável após alteração de caso. Todos tiveram reprodução RED e correção GREEN; nenhum achado menor foi adiado.
- Decisão: preservar registros históricos sem migração e manter validação semântica nas novas sessões prontas, para não tornar ilegíveis logs antigos. Eventos antigos podem conservar diagnósticos anteriores; isso está documentado.
- Limites mantidos: autenticação independente do revisor, revisão jurídica material do piloto e homologação visual em host real exigem evidências próprias e não são substituídas pelos testes locais.
- A pasta temporária da auditoria anterior foi preservada e renomeada para `.pytest-audit-initial-20261002`, padrão já excluído da distribuição; não foi excluída nem incorporada ao pacote.
- Validação final: 364 testes Python aprovados em 59,92 s; 15 testes Vitest aprovados; TypeScript e build Vite aprovados; Ruff aprovado; integração 0.7.4 aprovada com 42 verificações, 34 JSON e 96 Python. O build emitiu somente avisos de anotações em comentários da dependência Zod. `git diff --check` passou para fontes; o bundle gerado contém whitespace originado de template interno da dependência.
- Alterações permanecem locais, sem commit, push, instalação ou publicação; documentos e launcher preexistentes foram preservados.
