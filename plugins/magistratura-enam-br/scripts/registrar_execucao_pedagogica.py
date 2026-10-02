#!/usr/bin/env python3
"""Registra uma saída capturada e sua avaliação, sem executar modelo nem inventar revisão."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path

from avaliar_saida_pedagogica import avaliar_saida
from jsonschema import Draft202012Validator, FormatChecker

SCHEMAS = Path(__file__).resolve().parents[1] / 'evals' / 'pedagogia' / 'schema'


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def registrar_execucao(caso: dict, texto: str, metadata: dict, destino: Path, *, revisao: dict | None = None) -> dict:
    evaluation = avaliar_saida(caso, texto)
    record = {
        'schema_version': '1.0.0', 'metadata': metadata,
        'case_snapshot': caso,
        'case_sha256': _sha(json.dumps(caso, ensure_ascii=False, sort_keys=True, separators=(',', ':'))),
        'output': texto, 'output_sha256': _sha(texto), 'evaluation': evaluation,
    }
    if revisao is not None:
        record['human_review'] = revisao
    schema = json.loads((SCHEMAS / 'execution.schema.json').read_text(encoding='utf-8'))
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(record))
    if errors:
        raise ValueError(f'Registro de execução inválido: {errors[0].message}')
    # jsonschema's optional RFC3339 checker is not installed in every runtime.
    executed_at = datetime.fromisoformat(metadata['executed_at'])
    if executed_at.utcoffset() is None:
        raise ValueError('A data da execução deve incluir fuso horário')
    if revisao is not None:
        if revisao['output_sha256'] != record['output_sha256']:
            raise ValueError('O hash da revisão não corresponde à saída capturada')
        if revisao['case_sha256'] != record['case_sha256']:
            raise ValueError('O hash da revisão não corresponde ao caso avaliado')
        criteria = revisao['criteria']
        ids = [item['id'] for item in criteria]
        if len(ids) != len(set(ids)) or set(ids) != set(evaluation['human_review_required']):
            raise ValueError('A revisão deve cobrir exatamente todos os critérios humanos da saída')
        fixture_status = caso.get('legal_grounding', {}).get('human_review', {}).get('review_status')
        if evaluation['status'] == 'reprovado' or any(not item['passed'] for item in criteria):
            evaluation['status'] = 'reprovado'
        elif fixture_status != 'pending':
            evaluation['status'] = 'aprovado_com_revisao_humana'
        # A revisão da saída não pode aprovar uma fixture jurídica pendente.
    serialized = json.dumps(record, ensure_ascii=False, indent=2) + '\n'
    with Path(destino).open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(serialized)
    return record


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalogo', type=Path, required=True)
    parser.add_argument('--caso', required=True)
    parser.add_argument('--saida', type=Path, required=True)
    parser.add_argument('--metadados', type=Path, required=True)
    parser.add_argument('--revisao', type=Path)
    parser.add_argument('--destino', type=Path, required=True)
    parser.add_argument('--confirmar-gravacao-local', action='store_true', required=True)
    args = parser.parse_args(argv)
    catalog = json.loads(args.catalogo.read_text(encoding='utf-8'))
    schema = json.loads((SCHEMAS / 'evals.schema.json').read_text(encoding='utf-8'))
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(catalog)
    case = next((item for item in catalog['evals'] if item['id'] == args.caso), None)
    if case is None:
        raise ValueError(f'Caso não encontrado: {args.caso}')
    record = registrar_execucao(
        case, args.saida.read_text(encoding='utf-8'),
        json.loads(args.metadados.read_text(encoding='utf-8')), args.destino,
        revisao=json.loads(args.revisao.read_text(encoding='utf-8')) if args.revisao else None,
    )
    print(json.dumps({'run_id': record['metadata']['run_id'], 'status': record['evaluation']['status']}, ensure_ascii=False))
    return 2 if record['evaluation']['status'] == 'reprovado' else 0


if __name__ == '__main__':
    raise SystemExit(main())
