from pathlib import Path
from tempfile import TemporaryDirectory
from catalog_qa import inspect, main
import csv

sample = Path(__file__).with_name("sample_catalog.csv")
rows, exceptions = inspect(sample)
assert len(rows) == 6
assert len(exceptions) == 3
assert rows[0]["price"] == "29.90"
assert "duplicate_sku" in exceptions[0]["flags"]
assert exceptions[1]["flags"] == "missing_category"
assert exceptions[2]["flags"] == "invalid_price"
with TemporaryDirectory() as d:
    cleaned = Path(d) / "clean.csv"
    errors = Path(d) / "errors.csv"
    main(["catalog_qa.py", str(sample), str(cleaned), str(errors)])
    with cleaned.open(newline="") as f:
        clean = list(csv.DictReader(f))
    assert clean[-1]["product_name"].startswith("'=")
    with errors.open(newline="") as f:
        assert len(list(csv.DictReader(f))) == 3
print("All synthetic catalog QA tests passed")
