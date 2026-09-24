import json
import os
import tempfile
import uuid
from datetime import UTC, datetime
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from .config import LibraryConfig
from .indexer import index_library
from .questions import QuestionRepository
from .retrieval import search_index


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _write_json_atomic(path: Path, payload: dict) -> None:
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(payload, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


class StudyService:
    def __init__(self, config: LibraryConfig):
        self.config = config
        self.state_dir = config.library_root / ".estudo-juridico"
        if not self.state_dir.is_dir():
            raise FileNotFoundError(f"Subpasta local não existe: {self.state_dir}")
        self.index_path = self.state_dir / "index.json"
        self.questions = QuestionRepository(self.state_dir)

    def diagnose_library(self) -> dict:
        result = {
            "schema_version": "1.0.0",
            "library_root": str(self.config.library_root),
            "state_dir": str(self.state_dir),
            "index_path": str(self.index_path),
            "index_status": "missing",
            "document_count": None,
            "generated_at": None,
        }
        if not self.index_path.exists() and not self.index_path.is_symlink():
            return result
        if not self.index_path.is_file():
            result["index_status"] = "invalid"
            return result
        try:
            manifest = json.loads(self.index_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            result["index_status"] = "invalid"
            return result
        if (
            not isinstance(manifest, dict)
            or manifest.get("schema_version") != "1.0.0"
            or not isinstance(manifest.get("generated_at"), str)
            or not isinstance(manifest.get("documents"), list)
            or any(not isinstance(item, dict) for item in manifest["documents"])
        ):
            result["index_status"] = "invalid"
            return result
        try:
            generated_at = datetime.fromisoformat(manifest["generated_at"])
        except ValueError:
            result["index_status"] = "invalid"
            return result
        if generated_at.utcoffset() is None:
            result["index_status"] = "invalid"
            return result
        document_schema = json.loads(
            (Path(__file__).parent / "schemas" / "indexed-document.schema.json").read_text(encoding="utf-8")
        )
        validator = Draft202012Validator(document_schema, format_checker=FormatChecker())
        if any(not validator.is_valid(document) for document in manifest["documents"]):
            result["index_status"] = "invalid"
            return result
        result["index_status"] = "available"
        result["document_count"] = len(manifest["documents"])
        result["generated_at"] = manifest["generated_at"]
        return result

    def index_library(self, *, confirmed: bool) -> dict:
        if not confirmed:
            raise PermissionError("A indexação exige confirmação explícita de gravação local")
        previous = None
        if self.index_path.exists():
            previous = json.loads(self.index_path.read_text(encoding="utf-8"))
        result = index_library(self.config, previous_manifest=previous)
        _write_json_atomic(self.index_path, result.manifest)
        return {
            "schema_version": "1.0.0",
            "document_count": len(result.manifest["documents"]),
            "indexed_count": result.indexed_count,
            "reused_count": result.reused_count,
            "removed_count": result.removed_count,
            "ignored_files": list(result.ignored_files),
        }

    def search(self, query: str, *, limit: int, path_prefix: str | None) -> dict:
        if not self.index_path.is_file():
            raise FileNotFoundError("Índice local ainda não foi criado")
        manifest = json.loads(self.index_path.read_text(encoding="utf-8"))
        return {
            "schema_version": "1.0.0",
            "query": query,
            "results": search_index(
                manifest,
                query,
                limit=min(max(limit, 0), self.config.max_result_chunks),
                config=self.config,
                path_prefix=path_prefix,
            ),
        }

    def create_question(self, question: dict) -> dict:
        private = {
            **question,
            "schema_version": "1.0.0",
            "projection": "private",
            "session_id": f"qsn_{uuid.uuid4().hex}",
            "state": "ready",
            "created_at": _utc_now(),
        }
        return self.questions.create_session(private)

    def answer_question(self, session_id: str, option: str) -> dict:
        return self.questions.answer(session_id, option, answered_at=_utc_now())

    def history(self, *, limit: int, cursor: int) -> dict:
        if limit < 1 or limit > 100:
            raise ValueError("limite deve estar entre 1 e 100")
        if cursor < 0:
            raise ValueError("cursor não pode ser negativo")
        latest: dict[str, dict] = {}
        for question in self.questions.questions_store.read_all():
            latest[question["session_id"]] = question
        attempts = {
            attempt["session_id"]: attempt for attempt in self.questions.attempts_store.read_all()
        }
        items = []
        for session_id, question in latest.items():
            attempt = attempts.get(session_id)
            items.append(
                {
                    "session_id": session_id,
                    "created_at": question["created_at"],
                    "subject": question["subject"],
                    "topic": question["topic"],
                    "state": "answered" if attempt else question["state"],
                    "result": attempt["result"] if attempt else None,
                }
            )
        items.sort(key=lambda item: (item["created_at"], item["session_id"]), reverse=True)
        page = items[cursor : cursor + limit]
        next_cursor = cursor + len(page) if cursor + len(page) < len(items) else None
        return {"items": page, "next_cursor": next_cursor, "total": len(items)}
