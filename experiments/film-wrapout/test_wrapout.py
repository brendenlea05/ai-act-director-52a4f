import csv
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from wrapout import parse_receipts, export_csv, export_html

with TemporaryDirectory() as td:
    d = Path(td)
    src = d / 'in.csv'
    src.write_text('date,vendor,amount,description\n2026-10-25,Alpha,12.50,Notes\n2026-10-24,=DANGEROUS,3.00,<script>alert(1)</script>\n', encoding='utf-8')
    rows = parse_receipts(src)
    assert [r['receipt_no'] for r in rows] == ['R001','R002']
    assert rows[0]['vendor'] == '=DANGEROUS'
    assert sum((r['amount'] for r in rows), Decimal('0')) == Decimal('15.50')
    export_csv(rows, d / 'out.csv')
    out = list(csv.DictReader((d / 'out.csv').open()))
    assert out[0]['vendor'].startswith("'=")
    export_html(rows, 'Project <test>', d / 'out.html')
    html = (d / 'out.html').read_text()
    assert 'Project &lt;test&gt;' in html and '&lt;script&gt;' in html
    for value, problem in [('oops','amount'), ('1.123','amount')]:
        src.write_text('date,vendor,amount,description\n2026-10-25,A,'+value+',x\n')
        try: parse_receipts(src)
        except ValueError as e: assert problem in str(e)
        else: raise AssertionError('expected invalid amount')
    src.write_text('date,vendor,amount,description\n2026-02-30,A,1.00,x\n')
    try: parse_receipts(src)
    except ValueError as e: assert 'date' in str(e)
    else: raise AssertionError('expected invalid date')
print('All wrapout tests passed')
