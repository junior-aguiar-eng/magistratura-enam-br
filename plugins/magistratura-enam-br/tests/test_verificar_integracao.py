from types import SimpleNamespace

import verificar_integracao as verificador

SCHEMAS_PEDAGOGICOS = {
    "modelos/pedagogia/learning-event.schema.json",
    "modelos/pedagogia/candidate-profile.schema.json",
    "modelos/pedagogia/profile-settings.schema.json",
    "modelos/pedagogia/review-recommendation.schema.json",
    "modelos/pedagogia/session-route.schema.json",
    "modelos/pedagogia/transition.schema.json",
    "modelos/pedagogia/source-policy.schema.json",
    "modelos/pedagogia/trusted-source-registry.schema.json",
}


def test_schemas_pedagogicos_sao_artefatos_essenciais():
    assert SCHEMAS_PEDAGOGICOS <= set(verificador.ARQUIVOS_ESSENCIAIS)


def test_validador_rejeita_schema_pedagogico_ausente_ou_invalido(tmp_path):
    modelos = tmp_path / "modelos" / "pedagogia"
    modelos.mkdir(parents=True)
    (modelos / "learning-event.schema.json").write_text("{}", encoding="utf-8")
    (modelos / "candidate-profile.schema.json").write_text("{", encoding="utf-8")
    erros = []

    verificador.validar_schemas_pedagogicos(tmp_path, erros)

    assert erros == [
        "Schema pedagógico inválido em modelos/pedagogia/candidate-profile.schema.json.",
        "Schema pedagógico ausente: modelos/pedagogia/profile-settings.schema.json.",
        "Schema pedagógico ausente: modelos/pedagogia/review-recommendation.schema.json.",
        "Schema pedagógico ausente: modelos/pedagogia/session-route.schema.json.",
        "Schema pedagógico ausente: modelos/pedagogia/transition.schema.json.",
        "Schema pedagógico ausente: modelos/pedagogia/source-policy.schema.json.",
        "Schema pedagógico ausente: modelos/pedagogia/trusted-source-registry.schema.json.",
    ]


def test_validador_exige_contratos_e_registro_de_fontes():
    esperados = {
        "references/contrato-fluxos-conversacionais.md",
        "references/politica-fontes-juridicas.md",
        "references/fontes-confiaveis.json",
        "modelos/pedagogia/session-route.schema.json",
        "modelos/pedagogia/transition.schema.json",
        "modelos/pedagogia/source-policy.schema.json",
        "modelos/pedagogia/trusted-source-registry.schema.json",
    }

    assert esperados <= set(verificador.ARQUIVOS_ESSENCIAIS)


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
            "capabilities": ["Estudo jurídico"],
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


def test_validador_de_contrato_rejeita_capacidades_vazias(tmp_path):
    (tmp_path / "skills" / "exemplo").mkdir(parents=True)
    (tmp_path / "assets").mkdir()
    for nome in ("icone.png", "logo.png", "logo-dark.png"):
        (tmp_path / "assets" / nome).write_bytes(b"imagem")
    (tmp_path / "skills" / "exemplo" / "SKILL.md").write_text(
        "---\nname: exemplo\ndescription: Skill de teste\n---\n", encoding="utf-8"
    )
    manifesto = {
        "name": "magistratura-enam-br",
        "version": "0.3.2",
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

    assert erros == ["Manifesto interface.capabilities deve conter ao menos uma capacidade."]


def test_validador_de_contrato_rejeita_versao_divergente_do_pyproject(tmp_path):
    (tmp_path / "skills" / "exemplo").mkdir(parents=True)
    (tmp_path / "assets").mkdir()
    for nome in ("icone.png", "logo.png", "logo-dark.png"):
        (tmp_path / "assets" / nome).write_bytes(b"imagem")
    (tmp_path / "skills" / "exemplo" / "SKILL.md").write_text(
        "---\nname: exemplo\ndescription: Skill de teste\n---\n", encoding="utf-8"
    )
    (tmp_path / "pyproject.toml").write_text(
        "[project]\nname = 'magistratura-enam-br'\nversion = '0.3.1'\n",
        encoding="utf-8",
    )
    manifesto = {
        "name": "magistratura-enam-br",
        "version": "0.3.2",
        "description": "Plugin de teste",
        "skills": "./skills/",
        "author": {"name": "Boni Jr"},
        "interface": {
            "displayName": "Teste",
            "shortDescription": "Teste",
            "longDescription": "Teste",
            "developerName": "Boni Jr",
            "category": "Education",
            "capabilities": ["Estudo jurídico"],
            "defaultPrompt": "Teste",
            "composerIcon": "./assets/icone.png",
            "logo": "./assets/logo.png",
            "logoDark": "./assets/logo-dark.png",
        },
    }
    erros = []

    verificador.validar_contrato_plugin(tmp_path, manifesto, erros)

    assert erros == [
        "Versão divergente: plugin.json declara 0.3.2 e pyproject.toml declara 0.3.1."
    ]


def criar_plugin_minimo(tmp_path, prompts):
    (tmp_path / "skills" / "exemplo").mkdir(parents=True)
    (tmp_path / "assets").mkdir()
    for nome in ("icone.png", "logo.png", "logo-dark.png"):
        (tmp_path / "assets" / nome).write_bytes(b"imagem")
    (tmp_path / "skills" / "exemplo" / "SKILL.md").write_text(
        "---\nname: exemplo\ndescription: Skill de teste\n---\n", encoding="utf-8"
    )
    return {
        "name": "magistratura-enam-br",
        "version": "0.4.1",
        "description": "Plugin de teste",
        "skills": "./skills/",
        "author": {"name": "Boni Jr"},
        "interface": {
            "displayName": "Teste",
            "shortDescription": "Teste",
            "longDescription": "Teste",
            "developerName": "Boni Jr",
            "category": "Education",
            "capabilities": ["Estudo jurídico"],
            "defaultPrompt": prompts,
            "composerIcon": "./assets/icone.png",
            "logo": "./assets/logo.png",
            "logoDark": "./assets/logo-dark.png",
        },
    }


def test_validador_de_contrato_aceita_lista_de_prompts(tmp_path):
    manifesto = criar_plugin_minimo(tmp_path, ["Jornada guiada", "Estudar tema", "Treinar questão"])
    erros = []

    verificador.validar_contrato_plugin(tmp_path, manifesto, erros)

    assert erros == []


def test_validador_de_contrato_rejeita_mais_de_tres_prompts(tmp_path):
    manifesto = criar_plugin_minimo(tmp_path, ["Um", "Dois", "Três", "Quatro"])
    erros = []

    verificador.validar_contrato_plugin(tmp_path, manifesto, erros)

    assert erros == [
        "Manifesto interface.defaultPrompt deve conter de um a três prompts não vazios de até 128 caracteres."
    ]
