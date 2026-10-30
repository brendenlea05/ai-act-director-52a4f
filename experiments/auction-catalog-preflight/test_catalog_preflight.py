import tempfile
from pathlib import Path
from catalog_preflight import analyze

sample = Path(__file__).with_name('sample_auction.csv')
result = analyze(sample)
codes = [x['code'] for x in result['issues']]
assert result['rows'] == 7, result
assert codes.count('DUPLICATE_LOT') == 2, codes
assert codes.count('MISSING_LOT') == 1, codes
assert codes.count('MISSING_TITLE') == 1, codes
assert codes.count('MISSING_IMAGE_REFERENCE') == 1, codes
assert codes.count('SPREADSHEET_FORMULA_RISK') == 1, codes
with tempfile.TemporaryDirectory() as d:
    path = Path(d)/'bad.csv'
    path.write_text('wrong,headers\n1,a\n',encoding='utf-8')
    try: analyze(path)
    except ValueError: pass
    else: raise AssertionError('Expected missing-column error')
print('PASS: 7 fictional lots, 6 expected flags, bad headers rejected')
