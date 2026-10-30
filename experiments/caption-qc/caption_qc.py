#!/usr/bin/env python3
"""Offline SRT structural and readability preflight; not a transcription or compliance audit."""
import argparse
import json
import re
from pathlib import Path

TIMESTAMP = re.compile(r'^(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})$')

def milliseconds(parts):
    h, m, s, ms = map(int, parts)
    if m >= 60 or s >= 60 or ms >= 1000:
        raise ValueError('out-of-range timestamp component')
    return ((h * 60 + m) * 60 + s) * 1000 + ms

def inspect_srt(source, max_cps=20.0, max_chars=42):
    text = source.lstrip('\ufeff').replace('\r\n', '\n').replace('\r', '\n').strip()
    blocks = re.split(r'\n\s*\n', text) if text else []
    findings = []
    prev_end = None
    for position, block in enumerate(blocks, 1):
        lines = block.split('\n')
        def issue(code, detail):
            findings.append({'cue': position, 'code': code, 'detail': detail})
        if len(lines) < 2:
            issue('invalid_cue', 'Missing timestamp line')
            continue
        if lines[0].strip() != str(position):
            issue('sequence', f'Expected cue number {position}')
        match = TIMESTAMP.fullmatch(lines[1].strip())
        if not match:
            issue('timestamp', 'Expected HH:MM:SS,mmm --> HH:MM:SS,mmm')
            continue
        try:
            start, end = milliseconds(match.groups()[:4]), milliseconds(match.groups()[4:])
        except ValueError as exc:
            issue('timestamp', str(exc))
            continue
        if end <= start:
            issue('duration', 'End must be after start')
        if prev_end is not None and start < prev_end:
            issue('overlap', 'Cue starts before previous cue ends')
        prev_end = end
        caption = lines[2:]
        if not any(line.strip() for line in caption):
            issue('empty_text', 'Caption has no visible text')
        if len(caption) > 2:
            issue('line_count', f'{len(caption)} text lines; suggested maximum 2')
        for idx, line in enumerate(caption, 1):
            if len(line) > max_chars:
                issue('line_length', f'Line {idx}: {len(line)} characters; threshold {max_chars}')
        if end > start:
            chars = sum(len(line.strip()) for line in caption)
            cps = chars / ((end - start) / 1000)
            if cps > max_cps:
                issue('reading_speed', f'{cps:.1f} characters/second; threshold {max_cps:g}')
    return {'cue_count': len(blocks), 'finding_count': len(findings), 'findings': findings,
            'note': 'Heuristic structural/readability preflight only; verify against source audio/video and platform style guide.'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('--max-cps', type=float, default=20)
    parser.add_argument('--max-chars', type=int, default=42)
    args = parser.parse_args()
    if args.max_cps <= 0 or args.max_chars <= 0:
        parser.error('thresholds must be positive')
    print(json.dumps(inspect_srt(args.file.read_text(encoding='utf-8'), args.max_cps, args.max_chars), indent=2))

if __name__ == '__main__':
    main()
