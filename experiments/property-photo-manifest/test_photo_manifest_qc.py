from pathlib import Path
from tempfile import TemporaryDirectory
from photo_manifest_qc import inspect

sample = Path(__file__).with_name('sample_manifest.csv')
total, issues = inspect(sample)
assert total == 7
assert len(issues) == 5, issues
assert [flag for _, flag in issues].count('duplicate_filename_in_visit') == 2
assert {flag for _, flag in issues} >= {'missing_room', 'unsupported_extension', 'timestamp_missing_timezone'}
with TemporaryDirectory() as temp:
    f = Path(temp) / 'good.csv'
    f.write_text('property_ref,visit_ref,room,filename,captured_at\nA,1,Kitchen,k.jpg,2026-10-30T10:00:00+00:00\n')
    assert inspect(f) == (1, [])
print('PASS: 7 synthetic rows, 5 expected flags, clean case')
