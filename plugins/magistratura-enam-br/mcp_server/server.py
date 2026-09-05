import argparse
from pathlib import Path
from typing import Any, Literal

from mcp.server import MCPServer
from mcp.types import ToolAnnotations
from pydantic import BaseModel, ConfigDict, Field

from .config import LibraryConfig
from .resources import UI_MIME_TYPE, UI_URI, load_question_widget
from .tools import StudyService

Option = Literal["A", "B", "C", "D", "E"]


class _StrictInput(BaseModel):
    model_config = ConfigDict(extra="forbid")


class AlternativeInput(_StrictInput):
    id: Option
    text: str = Field(min_length=1)


class SourceInput(_StrictInput):
    source_id: str = Field(pattern=r"^src_[0-9A-Za-z_-]{3,120}$")
    kind: Literal["local_markdown", "planalto", "stf", "stj", "legal_site"]
    title: str = Field(min_length=1, max_length=500)
    accessed_at: str
    role: Literal["regra", "precedente", "contexto", "complemento"]
    relative_path: str | None = None
    url: str | None = None
    excerpt: str | None = Field(default=None, min_length=1, max_length=4000)


class DistractorInput(_StrictInput):
    option: Option
    analysis: str = Field(min_length=1)


class CorrectionInput(_StrictInput):
    correct_rationale: str = Field(min_length=1)
    distractor_analysis: list[DistractorInput] = Field(min_length=4, max_length=4)
    exceptions: list[str]
    traps: list[str]


class QuestionInput(_StrictInput):
    subject: str = Field(min_length=1, max_length=200)
    topic: str = Field(min_length=1, max_length=300)
    mode: Literal["training", "simulation", "remediation"] = "training"
    prompt: str = Field(min_length=1)
    alternatives: list[AlternativeInput] = Field(min_length=5, max_length=5)
    correct_option: Option
    correction: CorrectionInput
    sources: list[SourceInput]
    source_status: Literal["verified", "partial", "caution"]
    caution_notice: str | None = Field(default=None, min_length=1)


def build_server(config: LibraryConfig) -> MCPServer:
    service = StudyService(config)
    server = MCPServer(
        "estudo-juridico-avancado",
        title="Estudo Jurídico Avançado",
        description="Acervo Markdown local e sessões jurídicas interativas.",
        version="0.1.0",
    )

    @server.tool(
        structured_output=True,
        annotations=ToolAnnotations(
            readOnlyHint=False, destructiveHint=False, idempotentHint=True, openWorldHint=False
        ),
    )
    def indexar_acervo(confirmar_gravacao_local: bool = False) -> dict[str, Any]:
        """Indexa recursivamente a biblioteca Markdown local autorizada."""
        return service.index_library(confirmed=confirmar_gravacao_local)

    @server.tool(
        structured_output=True,
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=False),
    )
    def buscar_acervo(
        consulta: str, limite: int = 8, prefixo: str | None = None
    ) -> dict[str, Any]:
        """Busca trechos rastreáveis no índice Markdown local."""
        return service.search(consulta, limit=limite, path_prefix=prefixo)

    @server.tool(
        structured_output=True,
        annotations=ToolAnnotations(
            readOnlyHint=False, destructiveHint=False, idempotentHint=False, openWorldHint=False
        ),
    )
    def criar_sessao_questao(questao: QuestionInput) -> dict[str, Any]:
        """Valida e guarda uma questão privada, devolvendo somente sua projeção pública."""
        return service.create_question(questao.model_dump(mode="json", exclude_none=True))

    @server.tool(
        structured_output=True,
        annotations=ToolAnnotations(
            readOnlyHint=False, destructiveHint=False, idempotentHint=True, openWorldHint=False
        ),
    )
    def responder_questao(session_id: str, alternativa: str) -> dict[str, Any]:
        """Registra a primeira tentativa e somente então libera a correção completa."""
        return service.answer_question(session_id, alternativa)

    @server.tool(
        structured_output=True,
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=False),
    )
    def consultar_historico_questoes(limite: int = 20, cursor: int = 0) -> dict[str, Any]:
        """Lista sessões locais resumidas e paginadas."""
        return service.history(limit=limite, cursor=cursor)

    @server.tool(
        description="Use quando uma sessão pronta deve ser exibida na interface interativa.",
        meta={"ui": {"resourceUri": UI_URI}},
        structured_output=True,
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=False),
    )
    def renderizar_questao(session_id: str) -> dict[str, Any]:
        """Carrega a projeção pública atual de uma sessão para o widget."""
        return service.questions.get_session(session_id)

    @server.resource(
        UI_URI,
        name="questao-juridica-interativa",
        title="Questão jurídica interativa",
        description="Widget acessível para responder e corrigir questões jurídicas.",
        mime_type=UI_MIME_TYPE,
        meta={
            "ui": {
                "prefersBorder": True,
                "csp": {"connectDomains": [], "resourceDomains": []},
            },
            "openai/widgetDescription": "Questão jurídica objetiva com correção após a tentativa.",
        },
    )
    def question_widget() -> str:
        return load_question_widget()

    return server


def _port(value: str) -> int:
    port = int(value)
    if port < 1 or port > 65535:
        raise argparse.ArgumentTypeError("porta deve estar entre 1 e 65535")
    return port


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Servidor MCP local do Estudo Jurídico Avançado")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--transport", choices=("stdio", "streamable-http"), default="stdio")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=_port, default=8765)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    server = build_server(LibraryConfig.load(args.config))
    if args.transport == "stdio":
        server.run("stdio")
    else:
        server.run(
            "streamable-http",
            host=args.host,
            port=args.port,
            streamable_http_path="/mcp",
            json_response=True,
            stateless_http=False,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
