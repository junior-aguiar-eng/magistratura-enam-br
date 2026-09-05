#!/usr/bin/env python3
"""Verifica a integridade estrutural do plugin sem escrever na árvore auditada."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import tomllib
from pathlib import Path
from urllib.parse import urlsplit

ARQUIVOS_ESSENCIAIS = (
    ".codex-plugin/plugin.json",
    "AGENTS.md",
    "pyproject.toml",
    ".python-version",
    "uv.lock",
    "requirements.txt",
    "references/contrato-pedagogico.md",
    "references/contrato-fluxos-conversacionais.md",
    "references/politica-fontes-juridicas.md",
    "references/fontes-confiaveis.json",
    "references/persistencia-pedagogica-local.md",
    "references/protocolo-uso-do-acervo.md",
    "modelos/pedagogia/learning-event.schema.json",
    "modelos/pedagogia/candidate-profile.schema.json",
    "modelos/pedagogia/review-recommendation.schema.json",
    "modelos/pedagogia/session-route.schema.json",
    "modelos/pedagogia/transition.schema.json",
    "modelos/pedagogia/source-policy.schema.json",
    "modelos/pedagogia/trusted-source-registry.schema.json",
    "scripts/eventos_aprendizagem.py",
    "scripts/perfil_candidato.py",
    "scripts/relatorio_aprendizagem.py",
    "skills/acompanhar-percurso-magistratura/SKILL.md",
    "skills/acompanhar-percurso-magistratura/agents/openai.yaml",
    "skills/acompanhar-percurso-magistratura/references/roteamento.md",
    "skills/curar-informativos-stf-stj/SKILL.md",
    "skills/curar-informativos-stf-stj/references/cenarios-avaliacao.md",
    "skills/curar-informativos-stf-stj/modelos/precedentes.schema.json",
    "skills/curar-informativos-stf-stj/scripts/atualizar_planilha_precedentes.py",
    "skills/estudar-direito-magistratura/SKILL.md",
    "skills/estudar-direito-magistratura/references/cenarios-avaliacao.md",
    "skills/planejar-jurisprudencia/SKILL.md",
    "skills/planejar-jurisprudencia/references/politica-adaptativa-v1.md",
    "skills/planejar-jurisprudencia/scripts/recomendar_revisao.py",
    "skills/planejar-jurisprudencia/scripts/atualizar_esteira.py",
    "skills/planejar-jurisprudencia/scripts/preparar_itens_esteira.py",
    "skills/comparar-materiais-enam/SKILL.md",
    "skills/comparar-materiais-enam/references/formato-entrega-comparativo.md",
    "skills/comparar-materiais-enam/scripts/auditar_rastreabilidade.py",
    "skills/comparar-materiais-enam/modelos/manifesto-execucao.schema.json",
)

SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")

DIRETORIOS_GERADOS = frozenset({
    ".git",
    ".pytest_cache",
    ".test-deps",
    ".test-tmp",
    ".venv",
    ".venv-test-curadoria",
    "__pycache__",
    "build",
    "dist",
})

SCHEMAS_PEDAGOGICOS = (
    "modelos/pedagogia/candidate-profile.schema.json",
    "modelos/pedagogia/learning-event.schema.json",
    "modelos/pedagogia/review-recommendation.schema.json",
    "modelos/pedagogia/session-route.schema.json",
    "modelos/pedagogia/transition.schema.json",
    "modelos/pedagogia/source-policy.schema.json",
    "modelos/pedagogia/trusted-source-registry.schema.json",
)

SKILLS_CANONICAS = frozenset({
    "acompanhar-percurso-magistratura",
    "comparar-materiais-enam",
    "curar-informativos-stf-stj",
    "estudar-direito-magistratura",
    "planejar-jurisprudencia",
})

MODALIDADES_CANONICAS = frozenset({
    "roteamento",
    "explicacao",
    "recuperacao",
    "consolidacao",
    "vespera",
    "questao_objetiva",
    "discursiva_curta",
    "prova_oral",
    "curadoria_informativo",
    "comparacao_material",
    "leitura_julgado",
    "revisao_julgado",
    "planejamento_revisao",
})

FONTES_CONFIAVEIS = frozenset({
    "stf",
    "stj",
    "planalto",
    "dizer-o-direito",
    "jota",
    "thomson-reuters-rt",
})

PADRAO_DOMINIO = re.compile(r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$")


def arquivos_fonte(raiz: Path, padrao: str):
    """Percorre somente arquivos distribuíveis, sem caches ou ambientes locais."""
    for caminho in raiz.rglob(padrao):
        relativo = caminho.relative_to(raiz)
        if not any(
            parte in DIRETORIOS_GERADOS or parte.startswith(".pytest-")
            for parte in relativo.parts
        ):
            yield caminho


def validar_schemas_pedagogicos(raiz: Path, erros: list[str]) -> None:
    """Exige os contratos pedagógicos versionados e JSON sintaticamente válido."""
    for relativo in SCHEMAS_PEDAGOGICOS:
        caminho = raiz / relativo
        if not caminho.is_file():
            erros.append(f"Schema pedagógico ausente: {relativo}.")
            continue
        try:
            schema = json.loads(caminho.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            erros.append(f"Schema pedagógico inválido em {relativo}.")
            continue
        if not isinstance(schema, dict):
            erros.append(f"Schema pedagógico inválido em {relativo}.")


def dominio_registrado(url: str, dominios: set[str] | frozenset[str]) -> bool:
    """Compara o hostname normalizado por igualdade exata, nunca por substring."""
    try:
        hostname = urlsplit(url).hostname
    except ValueError:
        return False
    return isinstance(hostname, str) and hostname.casefold() in {item.casefold() for item in dominios}


def validar_contratos_fluxos_fontes(raiz: Path, erros: list[str]) -> None:
    """Valida vocabulário fechado de rotas, modalidades e fontes confiáveis."""
    rota_path = raiz / "modelos" / "pedagogia" / "session-route.schema.json"
    registro_path = raiz / "references" / "fontes-confiaveis.json"
    try:
        rota = json.loads(rota_path.read_text(encoding="utf-8"))
        skills = frozenset(rota["properties"]["skill_ativa"]["enum"])
        modalidades = frozenset(rota["$defs"]["modalidade"]["enum"])
        if skills != SKILLS_CANONICAS:
            erros.append("session-route deve declarar exatamente as cinco skills canônicas.")
        if modalidades != MODALIDADES_CANONICAS:
            erros.append("session-route contém modalidades ausentes ou não canônicas.")
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError):
        erros.append("Não foi possível validar o vocabulário de session-route.")

    try:
        registro = json.loads(registro_path.read_text(encoding="utf-8"))
        fontes = registro["sources"]
        ids = [fonte["id"] for fonte in fontes]
        if len(ids) != len(set(ids)):
            erros.append("Registro de fontes contém identificadores duplicados.")
        if frozenset(ids) != FONTES_CONFIAVEIS:
            erros.append("Registro de fontes diverge da inclusão explícita autorizada.")
        for fonte in fontes:
            dominios = fonte.get("canonical_domains", [])
            if not dominios or any(
                not isinstance(dominio, str)
                or dominio != dominio.casefold()
                or PADRAO_DOMINIO.fullmatch(dominio) is None
                for dominio in dominios
            ):
                erros.append(f"Fonte {fonte.get('id', '<sem-id>')} possui domínio canônico inválido.")
            if fonte.get("tier") == "primaria" and not fonte.get("authoritative_for"):
                erros.append(f"Fonte primária {fonte.get('id', '<sem-id>')} sem authoritative_for.")
            if fonte.get("tier") == "secundaria" and not fonte.get("limitations"):
                erros.append(f"Fonte secundária {fonte.get('id', '<sem-id>')} sem limitations.")
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError):
        erros.append("Não foi possível validar o registro fechado de fontes.")


def validar_ambiente_uv(raiz: Path, erros: list[str]) -> None:
    """Confirma o contrato do ambiente sem sincronizar ou alterar arquivos."""
    pyproject = raiz / "pyproject.toml"
    python_version = raiz / ".python-version"
    lock = raiz / "uv.lock"
    if pyproject.is_file():
        try:
            projeto = tomllib.loads(pyproject.read_text(encoding="utf-8")).get("project", {})
            if projeto.get("name") != "magistratura-enam-br":
                erros.append("pyproject.toml com nome de projeto inesperado.")
            if projeto.get("requires-python") != ">=3.14,<3.15":
                erros.append("pyproject.toml deve fixar compatibilidade em Python 3.14.")
        except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
            erros.append(f"pyproject.toml inválido: {exc}")
    if python_version.is_file() and python_version.read_text(encoding="utf-8").strip() != "3.14":
        erros.append(".python-version deve fixar Python 3.14.")
    if lock.is_file():
        try:
            dados_lock = tomllib.loads(lock.read_text(encoding="utf-8"))
            if dados_lock.get("requires-python") != "==3.14.*":
                erros.append("uv.lock deve estar resolvido para Python 3.14.")
        except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
            erros.append(f"uv.lock inválido: {exc}")

    uv = shutil.which("uv")
    if not uv:
        erros.append("uv não encontrado para validar uv.lock.")
        return
    resultado = subprocess.run(
        [uv, "lock", "--check"],
        cwd=raiz,
        capture_output=True,
        text=True,
        check=False,
    )
    if resultado.returncode:
        detalhe = (resultado.stderr or resultado.stdout).strip()
        erros.append(f"uv.lock não está sincronizado com pyproject.toml: {detalhe or 'uv lock --check falhou.'}")


def validar_caminho_do_plugin(raiz: Path, valor: object, campo: str, erros: list[str]) -> None:
    """Garante que um recurso declarado permaneça dentro do plugin e exista."""
    if not isinstance(valor, str) or not valor.strip():
        erros.append(f"{campo} deve ser um caminho relativo não vazio.")
        return
    caminho = Path(valor.replace("\\", "/"))
    if caminho.is_absolute() or ".." in caminho.parts:
        erros.append(f"{campo} deve permanecer dentro do plugin.")
        return
    resolvido = (raiz / caminho).resolve()
    if not resolvido.is_relative_to(raiz.resolve()) or not resolvido.is_file():
        erros.append(f"{campo} aponta para recurso inexistente dentro do plugin.")


def validar_frontmatter_skill(caminho: Path, erros: list[str]) -> None:
    """Confere o contrato mínimo que torna uma skill descobrível pelo Codex."""
    try:
        conteudo = caminho.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        erros.append(f"Não foi possível ler {caminho}: {exc}")
        return
    if not conteudo.startswith("---\n"):
        erros.append(f"{caminho}: frontmatter YAML inicial ausente.")
        return
    fim = conteudo.find("\n---", 4)
    if fim == -1:
        erros.append(f"{caminho}: frontmatter YAML não encerrado.")
        return
    campos = {
        chave.strip(): valor.strip()
        for linha in conteudo[4:fim].splitlines()
        if ":" in linha
        for chave, valor in [linha.split(":", 1)]
    }
    for campo in ("name", "description"):
        if not campos.get(campo):
            erros.append(f"{caminho}: frontmatter sem {campo} não vazio.")


def validar_contrato_plugin(raiz: Path, manifesto: object, erros: list[str]) -> None:
    """Valida o contrato distribuível que a árvore canônica controla localmente."""
    if not isinstance(manifesto, dict):
        return
    for campo in ("name", "description"):
        if not isinstance(manifesto.get(campo), str) or not manifesto[campo].strip():
            erros.append(f"Manifesto sem {campo} não vazio.")
    versao = manifesto.get("version")
    if not isinstance(versao, str) or SEMVER.fullmatch(versao) is None:
        erros.append("Manifesto deve conter versão SemVer válida.")
    pyproject = raiz / "pyproject.toml"
    if isinstance(versao, str) and pyproject.is_file():
        try:
            versao_projeto = tomllib.loads(pyproject.read_text(encoding="utf-8")).get("project", {}).get("version")
            if isinstance(versao_projeto, str) and versao_projeto != versao:
                erros.append(
                    f"Versão divergente: plugin.json declara {versao} e pyproject.toml declara {versao_projeto}."
                )
        except (OSError, UnicodeError, tomllib.TOMLDecodeError):
            pass
    if Path(str(manifesto.get("skills", ""))).as_posix().rstrip("/") != "skills":
        erros.append("Manifesto deve declarar skills como ./skills/.")
    autor = manifesto.get("author")
    if not isinstance(autor, dict) or not isinstance(autor.get("name"), str) or not autor["name"].strip():
        erros.append("Manifesto deve conter author.name não vazio.")
    interface = manifesto.get("interface")
    if not isinstance(interface, dict):
        erros.append("Manifesto deve conter interface como objeto.")
    else:
        for campo in ("displayName", "shortDescription", "longDescription", "developerName", "category", "defaultPrompt"):
            if not isinstance(interface.get(campo), str) or not interface[campo].strip():
                erros.append(f"Manifesto interface sem {campo} não vazio.")
        capacidades = interface.get("capabilities")
        if not isinstance(capacidades, list) or not capacidades or not all(
            isinstance(item, str) and item.strip() for item in capacidades
        ):
            erros.append("Manifesto interface.capabilities deve conter ao menos uma capacidade.")
        for campo in ("composerIcon", "logo", "logoDark"):
            validar_caminho_do_plugin(raiz, interface.get(campo), f"interface.{campo}", erros)

    diretorio_skills = raiz / "skills"
    if not diretorio_skills.is_dir():
        erros.append("Diretório skills ausente.")
        return
    for diretorio_skill in sorted(caminho for caminho in diretorio_skills.iterdir() if caminho.is_dir()):
        skill = diretorio_skill / "SKILL.md"
        if not skill.is_file():
            erros.append(f"Skill sem SKILL.md: {diretorio_skill.name}.")
            continue
        validar_frontmatter_skill(skill, erros)


def main() -> None:
    parser = argparse.ArgumentParser(description="Verifica a integração do plugin Magistratura e ENAM Brasil.")
    parser.add_argument("--plugin", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    raiz = args.plugin.resolve()
    erros: list[str] = []
    for relativo in ARQUIVOS_ESSENCIAIS:
        if not (raiz / relativo).is_file():
            erros.append(f"Arquivo essencial ausente: {relativo}")

    validar_ambiente_uv(raiz, erros)
    validar_schemas_pedagogicos(raiz, erros)
    validar_contratos_fluxos_fontes(raiz, erros)

    manifesto = raiz / ".codex-plugin" / "plugin.json"
    dados_manifesto: object = None
    versao = None
    if manifesto.is_file():
        try:
            dados_manifesto = json.loads(manifesto.read_text(encoding="utf-8"))
            if not isinstance(dados_manifesto, dict):
                erros.append("Manifesto JSON deve conter um objeto.")
            elif dados_manifesto.get("name") != "magistratura-enam-br":
                erros.append("Manifesto com nome de plugin inesperado.")
            versao = dados_manifesto.get("version") if isinstance(dados_manifesto, dict) else None
            if not isinstance(versao, str) or not versao.strip():
                erros.append("Manifesto sem versão não vazia.")
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            erros.append(f"Manifesto JSON inválido: {exc}")
    validar_contrato_plugin(raiz, dados_manifesto, erros)

    total_json = 0
    for caminho in arquivos_fonte(raiz, "*.json"):
        total_json += 1
        try:
            json.loads(caminho.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            erros.append(f"JSON inválido em {caminho.relative_to(raiz)}: {exc}")
    total_python = 0
    for caminho in arquivos_fonte(raiz, "*.py"):
        total_python += 1
        try:
            compile(caminho.read_text(encoding="utf-8"), str(caminho), "exec")
        except (OSError, UnicodeError, SyntaxError) as exc:
            erros.append(f"Python inválido em {caminho.relative_to(raiz)}: {exc}")

    resultado = {
        "status": "aprovado" if not erros else "reprovado",
        "versao": versao,
        "checks": len(ARQUIVOS_ESSENCIAIS),
        "arquivos_json": total_json,
        "arquivos_python": total_python,
        "erros": erros,
    }
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    if erros:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
