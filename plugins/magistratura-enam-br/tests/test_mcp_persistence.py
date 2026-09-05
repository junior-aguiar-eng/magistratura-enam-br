from concurrent.futures import ThreadPoolExecutor

import pytest

from mcp_server.persistence import JsonlCorruptionError, JsonlStore


def test_jsonl_append_preserva_utf8_e_rejeita_id_duplicado(tmp_path):
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": ["id", "texto"],
        "properties": {"id": {"type": "string"}, "texto": {"type": "string"}},
    }
    store = JsonlStore(tmp_path / "dados.jsonl", schema, id_field="id")
    registro = {"id": "um", "texto": "prescrição"}

    store.append(registro)

    assert store.read_all() == [registro]
    assert "prescrição" in store.path.read_text(encoding="utf-8")
    with pytest.raises(ValueError, match="duplicado"):
        store.append(registro)


def test_jsonl_corrompido_bloqueia_nova_escrita_sem_alteracao(tmp_path):
    schema = {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object"}
    path = tmp_path / "dados.jsonl"
    path.write_text('{"id":"um"}\n{\n', encoding="utf-8")
    original = path.read_bytes()
    store = JsonlStore(path, schema, id_field="id")

    with pytest.raises(JsonlCorruptionError, match="linha 2"):
        store.append({"id": "dois"})

    assert path.read_bytes() == original


def test_lock_impede_duas_gravacoes_concorrentes_do_mesmo_id(tmp_path):
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": ["id"],
        "properties": {"id": {"type": "string"}},
    }
    store = JsonlStore(tmp_path / "dados.jsonl", schema, id_field="id")

    def gravar():
        try:
            store.append({"id": "unico"})
            return "ok"
        except ValueError:
            return "duplicado"

    with ThreadPoolExecutor(max_workers=2) as executor:
        resultados = list(executor.map(lambda _: gravar(), range(2)))

    assert sorted(resultados) == ["duplicado", "ok"]
    assert store.read_all() == [{"id": "unico"}]


def test_store_nao_cria_diretorio_pai_implicitamente(tmp_path):
    store = JsonlStore(
        tmp_path / "ausente" / "dados.jsonl",
        {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object"},
        id_field="id",
    )

    with pytest.raises(FileNotFoundError, match="não existe"):
        store.append({"id": "um"})


def test_store_rejeita_registro_fora_do_schema(tmp_path):
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": ["id"],
        "properties": {"id": {"type": "string"}},
    }
    store = JsonlStore(tmp_path / "dados.jsonl", schema, id_field="id")

    with pytest.raises(ValueError, match="Registro inválido"):
        store.append({"id": 1})
    assert not store.path.exists()

