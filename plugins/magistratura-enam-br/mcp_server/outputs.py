"""Contratos de saída publicados pelo SDK, preservando os envelopes existentes."""

import json
from pathlib import Path
from typing import Annotated, Any, Literal, Self, TypedDict

from jsonschema import Draft202012Validator, FormatChecker, ValidationError
from pydantic import ConfigDict, RootModel, WithJsonSchema, model_validator


def _session_schema() -> dict[str, Any]:
    schema = json.loads(
        (Path(__file__).parent / "schemas" / "question-session.schema.json").read_text(
            encoding="utf-8"
        )
    )
    schema.pop("$id")
    schema["title"] = "Projeção de sessão MCP (pública ou corrigida após tentativa)"
    schema["properties"]["projection"]["enum"] = ["public", "corrected"]
    schema["properties"]["state"]["enum"] = ["ready", "answered", "invalidated"]
    schema["oneOf"] = [
        branch
        for branch in schema["oneOf"]
        if branch["properties"]["projection"]["const"] != "private"
    ]
    answer_fields = next(
        branch["required"]
        for branch in schema["oneOf"]
        if branch["properties"]["projection"]["const"] == "corrected"
    )
    for branch in schema["oneOf"]:
        if branch["properties"]["projection"]["const"] == "public":
            branch["not"] = {
                "anyOf": [{"required": [field]} for field in answer_fields]
            }
    definitions = schema.pop("$defs")

    # Pydantic owns its $defs registry. Inline the canonical local references
    # instead of inserting references unknown to that registry.
    def inline(value: Any) -> Any:
        if isinstance(value, list):
            return [inline(item) for item in value]
        if isinstance(value, dict):
            if "$ref" in value:
                name = value["$ref"].removeprefix("#/$defs/")
                return inline(
                    {
                        **definitions[name],
                        **{k: v for k, v in value.items() if k != "$ref"},
                    }
                )
            return {key: inline(item) for key, item in value.items()}
        return value

    return inline(schema)


SESSION_SCHEMA = _session_schema()
SESSION_VALIDATOR = Draft202012Validator(SESSION_SCHEMA, format_checker=FormatChecker())


class SessionOutput(
    RootModel[Annotated[dict[str, Any], WithJsonSchema(SESSION_SCHEMA)]]
):
    model_config = ConfigDict(hide_input_in_errors=True)

    @model_validator(mode="after")
    def validate_projection(self) -> Self:
        try:
            SESSION_VALIDATOR.validate(self.root)
        except ValidationError as error:
            raise ValueError(
                "Saída MCP incompatível com a projeção de sessão"
            ) from error
        return self


class IndexOutput(TypedDict):
    schema_version: Literal["1.0.0"]
    document_count: int
    indexed_count: int
    reused_count: int
    removed_count: int
    ignored_files: list[str]


class SearchHit(TypedDict):
    document_id: str
    chunk_id: str
    relative_path: str
    heading: str | None
    text: str
    score: int


class SearchOutput(TypedDict):
    schema_version: Literal["1.0.0"]
    query: str
    results: list[SearchHit]


class DiagnosticOutput(TypedDict):
    schema_version: Literal["1.0.0"]
    library_root: str
    state_dir: str
    index_path: str
    index_status: Literal["missing", "invalid", "available"]
    document_count: int | None
    generated_at: str | None


class HistoryItem(TypedDict):
    session_id: str
    created_at: str
    subject: str
    topic: str
    state: Literal["draft", "ready", "answered", "invalidated"]
    result: Literal["correct", "incorrect"] | None


class HistoryOutput(TypedDict):
    items: list[HistoryItem]
    next_cursor: int | None
    total: int
