"""Conversores determinísticos para referências pedagógicas compartilhadas."""

from __future__ import annotations

from typing import Any


def _texto(valor: Any, campo: str) -> str:
    texto = str(valor or "").strip()
    if not texto:
        raise ValueError(f"{campo} é obrigatório")
    return texto


def content_ref_from_precedente(
    precedente: dict[str, Any], *, subtema: str = "Não especificado"
) -> dict[str, Any]:
    """Converte um precedente sem perder seu identificador ou suas fontes."""
    identificador = precedente.get("id_decisao") or precedente.get("processo")
    fontes = [
        str(fonte).strip()
        for fonte in precedente.get("fontes_essenciais", [])
        if str(fonte).strip()
    ]
    return {
        "kind": "precedente",
        "id": _texto(identificador, "id_decisao ou processo"),
        "disciplina": _texto(precedente.get("disciplina"), "disciplina"),
        "tema": _texto(precedente.get("tema"), "tema"),
        "subtema": _texto(subtema, "subtema"),
        "source_refs": fontes,
        "source_state": _texto(
            precedente.get("estado_jurisprudencial"), "estado_jurisprudencial"
        ),
    }


def content_ref_from_delta(item: dict[str, Any]) -> dict[str, Any]:
    """Converte um delta documental, sem inferir desempenho do candidato."""
    tema_subtema = _texto(item.get("tema_subtema"), "tema_subtema")
    partes = [parte.strip() for parte in tema_subtema.split("/", 1)]
    tema = partes[0]
    subtema = partes[1] if len(partes) == 2 else "Não especificado"
    fontes = []
    for referencia in item.get("referencias_atuais", []):
        documento = _texto(referencia.get("documento"), "documento")
        pagina = _texto(referencia.get("pagina"), "pagina")
        localizacao = _texto(referencia.get("localizacao"), "localizacao")
        fontes.append(f"{documento} | p. {pagina} | {localizacao}")
    return {
        "kind": "delta_documental",
        "id": _texto(item.get("id_item"), "id_item"),
        "disciplina": _texto(item.get("disciplina"), "disciplina"),
        "tema": tema,
        "subtema": subtema,
        "source_refs": fontes,
        "source_state": (
            "documental_confirmado" if fontes else "documental_pendente"
        ),
    }
