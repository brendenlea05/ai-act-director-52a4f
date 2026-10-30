"""Offline, metadata-only photo-manifest preflight. No image inspection or network."""
import csv
import datetime as dt
import sys
from collections import Counter
from pathlib import Path

REQUIRED = ('property_ref', 'visit_ref', 'room', 'filename', 'captured_at')
ALLOWED = {'.jpg', '.jpeg', '.png', '.heic'}

def inspect(path):
    with open(path, newline='', encoding='utf-8-sig') as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames or any(k not in reader.fieldnames for k in REQUIRED):
            raise ValueError('Manifest must contain columns: ' + ', '.join(REQUIRED))
        rows = list(reader)
    counts = Counter((r['property_ref'].strip(), r['visit_ref'].strip(), r['filename'].strip().casefold()) for r in rows if r['filename'].strip())
    issues = []
    for index, r in enumerate(rows, start=2):
        for field in REQUIRED:
            if not r[field].strip():
                issues.append((index, 'missing_' + field))
        filename = r['filename'].strip()
        if filename and Path(filename).suffix.lower() not in ALLOWED:
            issues.append((index, 'unsupported_extension'))
        if filename and counts[(r['property_ref'].strip(), r['visit_ref'].strip(), filename.casefold())] > 1:
            issues.append((index, 'duplicate_filename_in_visit'))
        stamp = r['captured_at'].strip()
        if stamp:
            try:
                parsed = dt.datetime.fromisoformat(stamp.replace('Z', '+00:00'))
                if parsed.tzinfo is None:
                    issues.append((index, 'timestamp_missing_timezone'))
            except ValueError:
                issues.append((index, 'invalid_timestamp'))
    return len(rows), issues

def main():
    if len(sys.argv) != 2:
        print('Usage: python photo_manifest_qc.py manifest.csv', file=sys.stderr)
        return 2
    try:
        total, issues = inspect(sys.argv[1])
    except (OSError, ValueError) as exc:
        print('ERROR:', exc, file=sys.stderr)
        return 2
    print(f'{total} photo metadata rows; {len(issues)} review flags')
    print('csv_row,flag')
    for row, flag in issues:
        print(f'{row},{flag}')
    return 1 if issues else 0

if __name__ == '__main__':
    sys.exit(main())
