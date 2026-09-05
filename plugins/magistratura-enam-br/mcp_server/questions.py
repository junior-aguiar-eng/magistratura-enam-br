import copy
import hashlib
import json
from pathlib import Path

from filelock import FileLock

from .persistence import JsonlStore

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = Path(__file__).parent / "schemas"
LEARNING_EVENT_SCHEMA = ROOT / "modelos" / "pedagogia" / "learning-event.schema.json"

STATE_EVENT_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": False,
    "required": ["transition_id", "session_id", "state", "reason", "occurred_at"],
    "properties": {
        "transition_id": {"type": "string", "pattern": "^qtr_[0-9a-f]{16,64}$"},
        "session_id": {"type": "string", "pattern": "^qsn_[0-9a-f]{16,64}$"},
        "state": {"const": "invalidated"},
        "reason": {"type": "string", "minLength": 1},
        "occurred_at": {"type": "string", "format": "date-time"},
    },
}


class QuestionConflictError(ValueError):
    """Operação incompatível com o estado atual da sessão."""


def _load_schema(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _digest(value: object) -> str:
    serialized = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


class QuestionRepository:
    def __init__(self, state_dir: Path):
        self.state_dir = Path(state_dir).resolve(strict=True)
        self.questions_path = self.state_dir / "questoes.jsonl"
        self.questions_store = JsonlStore(
            self.questions_path, _load_schema(SCHEMAS / "question-session.schema.json")
        )
        self.attempts_store = JsonlStore(
            self.state_dir / "tentativas.jsonl",
            _load_schema(SCHEMAS / "question-attempt.schema.json"),
            id_field="attempt_id",
        )
        self.learning_events_store = JsonlStore(
            self.state_dir / "eventos.jsonl",
            _load_schema(LEARNING_EVENT_SCHEMA),
            id_field="event_id",
        )
        self.state_events_store = JsonlStore(
            self.state_dir / "session-states.jsonl", STATE_EVENT_SCHEMA, id_field="transition_id"
        )
        self._lock = FileLock(str(self.state_dir / ".question-repository.lock"))

    def _question_records(self, session_id: str) -> list[dict]:
        return [
            item for item in self.questions_store.read_all() if item["session_id"] == session_id
        ]

    def _private(self, session_id: str) -> dict:
        records = self._question_records(session_id)
        if not records:
            raise KeyError(f"Sessão não encontrada: {session_id}")
        return records[-1]

    def _attempt(self, session_id: str) -> dict | None:
        return next(
            (
                item
                for item in self.attempts_store.read_all()
                if item["session_id"] == session_id
            ),
            None,
        )

    def _is_invalidated(self, session_id: str) -> bool:
        return any(
            item["session_id"] == session_id for item in self.state_events_store.read_all()
        )

    @staticmethod
    def _public(private: dict) -> dict:
        public = {
            key: copy.deepcopy(value)
            for key, value in private.items()
            if key not in {"correct_option", "correction"}
        }
        public["projection"] = "public"
        public["state"] = "ready"
        return public

    def create_draft(self, private: dict) -> dict:
        if private.get("state") != "draft":
            raise ValueError("Rascunho deve usar state=draft")
        with self._lock:
            if self._question_records(private["session_id"]):
                raise QuestionConflictError("Sessão já existe")
            self.questions_store.append(private)
        return copy.deepcopy(private)

    def create_session(self, private: dict) -> dict:
        if private.get("state") != "ready":
            raise ValueError("Sessão apresentável deve usar state=ready")
        with self._lock:
            if self._question_records(private["session_id"]):
                raise QuestionConflictError("Sessão já existe")
            self.questions_store.append(private)
        return self._public(private)

    def mark_ready(self, session_id: str) -> dict:
        with self._lock:
            if self._is_invalidated(session_id):
                raise QuestionConflictError("Sessão invalidada não pode voltar a ready")
            private = self._private(session_id)
            if private["state"] != "draft":
                raise QuestionConflictError("Somente sessão draft pode avançar para ready")
            ready = copy.deepcopy(private)
            ready["state"] = "ready"
            self.questions_store.append(ready)
        return self._public(ready)

    def invalidate(self, session_id: str, *, reason: str, invalidated_at: str) -> dict:
        with self._lock:
            if self._attempt(session_id) is not None:
                raise QuestionConflictError("Sessão respondida não pode ser invalidada")
            private = self._private(session_id)
            if self._is_invalidated(session_id):
                raise QuestionConflictError("Sessão já invalidada")
            event = {
                "transition_id": f"qtr_{_digest([session_id, reason, invalidated_at])[:24]}",
                "session_id": session_id,
                "state": "invalidated",
                "reason": reason,
                "occurred_at": invalidated_at,
            }
            self.state_events_store.append(event)
        result = self._public(private)
        result["state"] = "invalidated"
        result["invalidation_reason"] = reason
        return result

    def _learning_event(self, private: dict, attempt: dict) -> dict:
        correct = attempt["result"] == "correct"
        source_state = {
            "verified": "verificada",
            "partial": "parcial",
            "caution": "cautela",
        }[private["source_status"]]
        content_id = private["session_id"].replace("_", "-")
        return {
            "schema_version": "2.0.0",
            "event_id": f"evt_{_digest(attempt)[:32]}",
            "occurred_at": attempt["answered_at"],
            "skill": "estudar-direito-magistratura",
            "content_ref": {
                "kind": "questao",
                "id": content_id,
                "disciplina": private["subject"],
                "tema": private["topic"],
                "subtema": private["topic"],
                "source_refs": attempt["source_refs"],
                "source_state": source_state,
                "source_version": attempt["answered_at"][:10],
            },
            "activity": {
                "activity_id": f"atividade-{content_id}",
                "modality": "questao_objetiva",
                "attempt_observed": True,
                "assistance_level": "nenhuma",
            },
            "performance": {
                "result": "correto" if correct else "incorreto",
                "error_types": [] if correct else ["distincao"],
                "domain_evidence": ["evocacao_regra"],
                "confidence": None,
            },
            "routing": {
                "target_skill": None if correct else "estudar-direito-magistratura",
                "reason_codes": [] if correct else ["erro_questao_objetiva"],
            },
        }

    def answer(self, session_id: str, selected_option: str, *, answered_at: str) -> dict:
        if selected_option not in {"A", "B", "C", "D", "E"}:
            raise ValueError("Alternativa inválida")
        with self._lock:
            if self._is_invalidated(session_id):
                raise QuestionConflictError("Sessão invalidada não pode ser respondida")
            private = self._private(session_id)
            if private["state"] != "ready":
                raise QuestionConflictError("Sessão ainda não está pronta")
            existing = self._attempt(session_id)
            if existing is not None:
                if existing["selected_option"] != selected_option:
                    raise QuestionConflictError("Sessão já respondida com outra alternativa")
                return self._corrected(private, existing)

            result = "correct" if selected_option == private["correct_option"] else "incorrect"
            source_refs = [item["source_id"] for item in private["sources"]]
            attempt = {
                "schema_version": "1.0.0",
                "attempt_id": f"qat_{_digest([session_id, selected_option])[:24]}",
                "session_id": session_id,
                "question_hash": _digest(private),
                "answered_at": answered_at,
                "selected_option": selected_option,
                "correct_option": private["correct_option"],
                "result": result,
                "source_refs": source_refs,
            }
            self.attempts_store.append(attempt)
            self.learning_events_store.append(self._learning_event(private, attempt))
        return self._corrected(private, attempt)

    @staticmethod
    def _corrected(private: dict, attempt: dict) -> dict:
        corrected = copy.deepcopy(private)
        corrected["projection"] = "corrected"
        corrected["state"] = "answered"
        corrected["selected_option"] = attempt["selected_option"]
        corrected["result"] = attempt["result"]
        corrected["answered_at"] = attempt["answered_at"]
        return corrected

    def get_session(self, session_id: str) -> dict:
        private = self._private(session_id)
        if self._is_invalidated(session_id):
            result = self._public(private)
            result["state"] = "invalidated"
            return result
        attempt = self._attempt(session_id)
        if attempt is not None:
            return self._corrected(private, attempt)
        if private["state"] == "ready":
            return self._public(private)
        return copy.deepcopy(private)
