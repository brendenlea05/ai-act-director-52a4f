"""Offline, auditable catalog CSV QA for authorized/anonymized input only.

Usage: python catalog_qa.py input.csv clean.csv exceptions.csv
No network, no guessing missing attributes, no API calls.
"""
import csv
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

REQUIRED = ("sku", "product_name", "category", "price")

def norm(text):
    return re.sub(r"\s+", " ", (text or "").strip())

def safe_csv(text):
    """Avoid spreadsheet formula execution when CSV is opened in Excel."""
    s = str(text)
    return "'" + s if s.lstrip().startswith(("=", "+", "-", "@")) else s

def inspect(source):
    rows, exceptions = [], []
    seen = {}
    with open(source, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV is empty or lacks headers")
        missing = [name for name in REQUIRED if name not in reader.fieldnames]
        if missing:
            raise ValueError("Missing required columns: " + ", ".join(missing))
        for line, row in enumerate(reader, start=2):
            if None in row:
                raise ValueError(f"Row {line} has more values than the header")
            data = {key: norm(row.get(key)) for key in REQUIRED}
            flags = []
            if not data["sku"]:
                flags.append("missing_sku")
            else:
                key = data["sku"].casefold()
                if key in seen:
                    flags.append(f"duplicate_sku_first_seen_row_{seen[key]}")
                else:
                    seen[key] = line
            if not data["product_name"]:
                flags.append("missing_product_name")
            if not data["category"]:
                flags.append("missing_category")
            if not data["price"]:
                flags.append("missing_price")
            else:
                try:
                    price = Decimal(data["price"].replace(",", ""))
                    if not price.is_finite() or price < 0:
                        raise InvalidOperation()
                    data["price"] = str(price.quantize(Decimal("0.01")))
                except (InvalidOperation, ValueError):
                    flags.append("invalid_price")
            data["source_row"] = line
            data["review_status"] = "REVIEW" if flags else "OK"
            rows.append(data)
            if flags:
                exceptions.append({"source_row": line, "sku": data["sku"], "flags": ";".join(flags)})
    return rows, exceptions

def write_csv(path, fieldnames, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: safe_csv(row.get(k, "")) for k in fieldnames})

def main(argv):
    if len(argv) != 4:
        raise SystemExit("Usage: python catalog_qa.py input.csv clean.csv exceptions.csv")
    source, clean, exception_file = argv[1:]
    if len({str(Path(p).resolve()) for p in (source, clean, exception_file)}) != 3:
        raise SystemExit("Input and output paths must be distinct")
    rows, exceptions = inspect(source)
    write_csv(clean, (*REQUIRED, "source_row", "review_status"), rows)
    write_csv(exception_file, ("source_row", "sku", "flags"), exceptions)
    print(f"Reviewed {len(rows)} rows; {len(exceptions)} rows require human review")

if __name__ == "__main__":
    main(sys.argv)
