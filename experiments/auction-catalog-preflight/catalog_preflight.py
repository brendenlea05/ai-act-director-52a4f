#!/usr/bin/env python3
"""Offline structural checks of auction catalog CSV; no pricing/condition appraisal."""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ALIASES = {
    'lot': ('lot', 'lot number', 'lot_number', 'lot #', 'lot no'),
    'title': ('title', 'item title', 'description', 'lot title'),
    'image': ('image', 'image filename', 'image url', 'photo', 'photo filename'),
}

def analyze(path):
    with open(path, encoding='utf-8-sig', newline='') as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames:
            raise ValueError('CSV must have a header')
        names = {n.strip().lower(): n for n in reader.fieldnames if n}
        fields = {k: next((names[a] for a in alts if a in names), None) for k, alts in ALIASES.items()}
        if not fields['lot'] or not fields['title']:
            raise ValueError('CSV needs a lot-number and title/description column')
        rows = list(reader)
    counts = Counter((r.get(fields['lot']) or '').strip().casefold() for r in rows)
    problems = []
    for line, row in enumerate(rows, start=2):
        lot = (row.get(fields['lot']) or '').strip()
        title = (row.get(fields['title']) or '').strip()
        def flag(code, field, detail):
            problems.append({'csv_line': line, 'lot': lot, 'code': code, 'field': field, 'detail': detail})
        if not lot:
            flag('MISSING_LOT', fields['lot'], 'Lot identifier is empty')
        elif counts[lot.casefold()] > 1:
            flag('DUPLICATE_LOT', fields['lot'], 'Identifier appears in more than one row')
        if not title:
            flag('MISSING_TITLE', fields['title'], 'Title/description is empty')
        if fields['image'] and not (row.get(fields['image']) or '').strip():
            flag('MISSING_IMAGE_REFERENCE', fields['image'], 'Image reference field is blank; check if intended')
        for field, raw in row.items():
            if field is None or not isinstance(raw, str):
                continue
            if raw.lstrip().startswith(('=', '+', '-', '@')) and field != fields['lot']:
                flag('SPREADSHEET_FORMULA_RISK', field, 'Text may execute as formula if opened/exported in spreadsheet')
    return {'rows': len(rows), 'issues': problems, 'fields': fields}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('input_csv')
    p.add_argument('--output', default='issues.json')
    a = p.parse_args()
    result = analyze(a.input_csv)
    Path(a.output).write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(f"Checked {result['rows']} rows, flagged {len(result['issues'])} review items; saved {a.output}")

if __name__ == '__main__':
    main()
