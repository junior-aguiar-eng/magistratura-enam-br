import json
from dataclasses import dataclass
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError


class ConfigError(ValueError):
    """Configuração local inválida ou indisponível."""


@dataclass(frozen=True)
class LibraryConfig:
    library_root: Path
    excluded_directories: tuple[str, ...]
    max_file_bytes: int
    max_result_chunks: int

    @classmethod
    def load(cls, path: Path) -> LibraryConfig:
        config_path = Path(path)
        if not config_path.is_file():
            raise ConfigError(f"Configuração não encontrada: {config_path}")

        try:
            data = json.loads(config_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ConfigError(f"Configuração inválida: {error}") from error

        configured_root = data.get("library_root")
        if isinstance(configured_root, str):
            root = Path(configured_root)
            if not root.is_absolute() or not root.is_dir():
                raise ConfigError("A raiz deve ser um diretório absoluto existente")

        schema_path = Path(__file__).parent / "schemas" / "library-config.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        try:
            Draft202012Validator(schema).validate(data)
        except ValidationError as error:
            if data.get("write_consent") is not True:
                raise ConfigError("A configuração exige consentimento explícito de escrita local") from error
            raise ConfigError(f"Configuração inválida: {error.message}") from error

        limits = data["limits"]
        return cls(
            library_root=root.resolve(strict=True),
            excluded_directories=tuple(data["excluded_directories"]),
            max_file_bytes=limits["max_file_bytes"],
            max_result_chunks=limits["max_result_chunks"],
        )
