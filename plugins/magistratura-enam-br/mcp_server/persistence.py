import json
import os
from pathlib import Path

from filelock import FileLock
from jsonschema import Draft202012Validator, FormatChecker


class JsonlCorruptionError(ValueError):
    """Log JSONL contém uma linha ilegível ou incompatível com seu contrato."""


class JsonlStore:
    def __init__(self, path: Path, schema: dict, *, id_field: str | None = None):
        self.path = Path(path)
        self.schema = schema
        self.id_field = id_field
        self.validator = Draft202012Validator(schema, format_checker=FormatChecker())
        self.lock = FileLock(f"{self.path}.lock")

    def _validate(self, record: dict) -> None:
        errors = sorted(self.validator.iter_errors(record), key=lambda error: list(error.path))
        if errors:
            raise ValueError(f"Registro inválido: {errors[0].message}")

    def read_all(self) -> list[dict]:
        if not self.path.exists():
            return []
        records: list[dict] = []
        identifiers: set[str] = set()
        with self.path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                try:
                    record = json.loads(line)
                    self._validate(record)
                except (json.JSONDecodeError, ValueError) as error:
                    raise JsonlCorruptionError(f"JSONL inválido na linha {line_number}: {error}") from error
                if self.id_field is not None:
                    identifier = record[self.id_field]
                    if identifier in identifiers:
                        raise JsonlCorruptionError(
                            f"Identificador duplicado na linha {line_number}: {identifier}"
                        )
                    identifiers.add(identifier)
                records.append(record)
        return records

    def append(self, record: dict) -> None:
        self._validate(record)
        if not self.path.parent.is_dir():
            raise FileNotFoundError(f"Diretório do log não existe: {self.path.parent}")
        with self.lock:
            existing = self.read_all()
            if self.id_field is not None:
                identifier = record[self.id_field]
                if any(item[self.id_field] == identifier for item in existing):
                    raise ValueError(f"Identificador duplicado: {identifier}")
            with self.path.open("a", encoding="utf-8", newline="\n") as stream:
                stream.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
                stream.flush()
                os.fsync(stream.fileno())

