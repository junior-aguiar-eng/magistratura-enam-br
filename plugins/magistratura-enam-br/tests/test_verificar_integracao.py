from types import SimpleNamespace

import verificar_integracao as verificador


def preparar_ambiente(tmp_path):
    (tmp_path / "pyproject.toml").write_text(
        "[project]\nname = 'magistratura-enam-br'\nrequires-python = '>=3.14,<3.15'\n",
        encoding="utf-8",
    )
    (tmp_path / ".python-version").write_text("3.14\n", encoding="utf-8")
    (tmp_path / "uv.lock").write_text("requires-python = '==3.14.*'\n", encoding="utf-8")


def test_validador_uv_rejeita_lock_dessincronizado(tmp_path, monkeypatch):
    preparar_ambiente(tmp_path)
    monkeypatch.setattr(verificador.shutil, "which", lambda _: "uv")
    monkeypatch.setattr(
        verificador.subprocess,
        "run",
        lambda *args, **kwargs: SimpleNamespace(returncode=1, stderr="lock needs update", stdout=""),
    )
    erros = []

    verificador.validar_ambiente_uv(tmp_path, erros)

    assert erros == ["uv.lock não está sincronizado com pyproject.toml: lock needs update"]


def test_validador_uv_rejeita_versao_de_python_incoerente(tmp_path, monkeypatch):
    preparar_ambiente(tmp_path)
    (tmp_path / ".python-version").write_text("3.13\n", encoding="utf-8")
    monkeypatch.setattr(verificador.shutil, "which", lambda _: "uv")
    monkeypatch.setattr(
        verificador.subprocess,
        "run",
        lambda *args, **kwargs: SimpleNamespace(returncode=0, stderr="", stdout=""),
    )
    erros = []

    verificador.validar_ambiente_uv(tmp_path, erros)

    assert erros == [".python-version deve fixar Python 3.14."]


def test_validador_de_contrato_rejeita_skill_sem_descricao(tmp_path):
    (tmp_path / ".codex-plugin").mkdir()
    (tmp_path / "skills" / "exemplo").mkdir(parents=True)
    (tmp_path / "assets").mkdir()
    for nome in ("icone.png", "logo.png", "logo-dark.png"):
        (tmp_path / "assets" / nome).write_bytes(b"imagem")
    (tmp_path / "skills" / "exemplo" / "SKILL.md").write_text(
        "---\nname: exemplo\n---\n", encoding="utf-8"
    )
    manifesto = {
        "name": "magistratura-enam-br",
        "version": "0.2.3",
        "description": "Plugin de teste",
        "skills": "./skills/",
        "author": {"name": "Boni Jr"},
        "interface": {
            "displayName": "Teste",
            "shortDescription": "Teste",
            "longDescription": "Teste",
            "developerName": "Boni Jr",
            "category": "Education",
            "capabilities": [],
            "defaultPrompt": "Teste",
            "composerIcon": "./assets/icone.png",
            "logo": "./assets/logo.png",
            "logoDark": "./assets/logo-dark.png",
        },
    }
    erros = []

    verificador.validar_contrato_plugin(tmp_path, manifesto, erros)

    assert erros == [
        f"{tmp_path / 'skills' / 'exemplo' / 'SKILL.md'}: frontmatter sem description não vazio."
    ]
