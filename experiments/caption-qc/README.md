# Caption QC preflight — experimental, offline

A small Python standard-library SRT **structural/readability preflight** for caption editors and creators. It flags timestamp format/range errors, reversed durations, overlaps, numbering errors, empty text, long lines, excess lines, and high estimated characters-per-second. It does **not** check speech accuracy, translation, accessibility compliance, speaker labels, sound descriptions, or platform acceptance.

```bash
python3 caption_qc.py sample.srt
python3 test_caption_qc.py
```

All sample captions are fictional. No uploads, API keys, external libraries, or data collection. Input stays on the user's computer. Default heuristic thresholds (20 characters/second, 42 characters/line) are adjustable and not official compliance standards. An editor must review against the actual audio/video and delivery style guide. Not a paid client project.
