import json
from pathlib import Path

import eventos_aprendizagem as eventos
import perfil_candidato as perfil
import pytest
from test_eventos_aprendizagem import criar_evento


def test_cli_validate_append_rebuild_e_export_exigem_caminhos_explicitos(tmp_path):
    evento_path = tmp_path / "evento.json"
    log = tmp_path / "eventos.jsonl"
    perfil_path = tmp_path / "perfil.json"
    exportado = tmp_path / "exportado.json"
    evento_path.write_text(json.dumps(criar_evento()), encoding="utf-8")

    assert eventos.main(["validate", "--evento", str(evento_path)]) == 0
    assert eventos.main(["append", "--log", str(log), "--evento", str(evento_path), "--confirmar-gravacao-local"]) == 0
    assert perfil.main(["rebuild", "--log", str(log), "--perfil", str(perfil_path), "--confirmar-gravacao-local"]) == 0
    assert perfil.main(
        ["export", "--log", str(log), "--perfil", str(perfil_path), "--saida", str(exportado), "--confirmar-gravacao-local"]
    ) == 0
    pacote = json.loads(exportado.read_text(encoding="utf-8"))
    assert pacote == {"events": [criar_evento()], "profile": json.loads(perfil_path.read_text(encoding="utf-8"))}

    with pytest.raises(SystemExit):
        eventos.main(["append", "--evento", str(evento_path)])
    with pytest.raises(SystemExit):
        perfil.main(["rebuild", "--log", str(log)])


def test_implementacao_nao_contem_cliente_de_rede():
    fontes = Path(eventos.__file__).read_text(encoding="utf-8") + Path(perfil.__file__).read_text(encoding="utf-8")

    assert all(termo not in fontes for termo in ("requests", "urllib", "http.client", "socket"))


def test_inspect_le_sem_autorizar_nova_escrita(tmp_path, capsys):
    perfil_path = tmp_path / "perfil.json"
    perfil.salvar_perfil_atomico(perfil_path, perfil.reconstruir_perfil([]))
    assert perfil.main(["inspect", "--perfil", str(perfil_path)]) == 0
    assert json.loads(capsys.readouterr().out)["schema_version"] == "2.0.0"


def test_rebuild_exige_confirmacao_de_gravacao_local(tmp_path):
    log = tmp_path / "eventos.jsonl"
    log.write_text("", encoding="utf-8")
    destino = tmp_path / "perfil.json"
    with pytest.raises(SystemExit):
        perfil.main(["rebuild", "--log", str(log), "--perfil", str(destino)])
    assert not destino.exists()


def test_append_exige_confirmacao_de_gravacao_local(tmp_path):
    evento_path = tmp_path / "evento.json"
    log = tmp_path / "eventos.jsonl"
    evento_path.write_text(json.dumps(criar_evento()), encoding="utf-8")
    with pytest.raises(SystemExit):
        eventos.main(["append", "--log", str(log), "--evento", str(evento_path)])
    assert not log.exists()


def test_delete_exige_confirmacao_e_remove_somente_o_alvo(tmp_path):
    perfil_path = tmp_path / "perfil.json"
    log = tmp_path / "eventos.jsonl"
    perfil_path.write_text("{}", encoding="utf-8")
    log.write_text("preservar", encoding="utf-8")
    assert perfil.main(["delete", "--perfil", str(perfil_path), "--confirmar-exclusao-local"]) == 0
    assert not perfil_path.exists()
    assert log.read_text(encoding="utf-8") == "preservar"
