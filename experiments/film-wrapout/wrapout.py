#!/usr/bin/env python3
"""Offline film-production petty-cash receipt ledger/cover-sheet generator.

Not accounting, tax, reimbursement approval, or OCR software.
"""
import argparse
import csv
from datetime import date
from decimal import Decimal, InvalidOperation
from html import escape
from pathlib import Path

REQUIRED = ("date", "vendor", "amount", "description")


def safe_csv_text(value):
    """Prevent spreadsheet formula execution on opening exported CSV files."""
    value = str(value)
    if value.lstrip().startswith(("=", "+", "-", "@")) or value.startswith(("\t", "\r", "\n")):
        return "'" + value
    return value


def parse_receipts(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or any(c not in reader.fieldnames for c in REQUIRED):
            raise ValueError("CSV must include: " + ", ".join(REQUIRED))
        rows = []
        for line, row in enumerate(reader, start=2):
            if not any((v or "").strip() for v in row.values() if isinstance(v, str)):
                continue
            try:
                date.fromisoformat((row["date"] or "").strip())
            except ValueError:
                raise ValueError(f"Row {line}: date must be YYYY-MM-DD") from None
            try:
                amount = Decimal((row["amount"] or "").strip())
                if not amount.is_finite() or amount.as_tuple().exponent < -2:
                    raise ValueError()
            except (InvalidOperation, ValueError):
                raise ValueError(f"Row {line}: amount must be a finite number with at most 2 decimals") from None
            vendor = (row["vendor"] or "").strip()
            if not vendor:
                raise ValueError(f"Row {line}: vendor required")
            rows.append({"date": row["date"].strip(), "vendor": vendor,
                         "amount": amount, "description": (row["description"] or "").strip(),
                         "source_line": line})
    rows.sort(key=lambda x: (x["date"], x["source_line"]))
    for i, row in enumerate(rows, start=1):
        row["receipt_no"] = f"R{i:03d}"
    return rows


def export_csv(rows, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(("receipt_no",) + REQUIRED)
        for r in rows:
            w.writerow((r["receipt_no"], r["date"], safe_csv_text(r["vendor"]),
                        f"{r['amount']:.2f}", safe_csv_text(r["description"])))


def export_html(rows, project, path):
    total = sum((r["amount"] for r in rows), Decimal("0"))
    body = "\n".join(
        "<tr>" + "".join(f"<td>{escape(str(v))}</td>" for v in
        (r["receipt_no"], r["date"], r["vendor"], r["description"], f"${r['amount']:,.2f}")) + "</tr>"
        for r in rows
    )
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Petty Cash Cover Sheet</title>
<style>body{{font:14px system-ui,Arial,sans-serif;margin:36px;color:#222}}h1{{font-size:22px}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #999;padding:8px;text-align:left}}th{{background:#eee}}tfoot{{font-weight:bold}}p.note{{color:#555}}@media print{{body{{margin:10mm}}}}</style></head>
<body><h1>Petty Cash / Reimbursement Cover Sheet</h1><p><strong>Project:</strong> {escape(project)}</p>
<p><strong>Receipts:</strong> {len(rows)} | <strong>Total:</strong> ${total:,.2f}</p>
<table><thead><tr><th>#</th><th>Date</th><th>Vendor</th><th>Description</th><th>Amount</th></tr></thead>
<tbody>{body}</tbody><tfoot><tr><td colspan="4">Total</td><td>${total:,.2f}</td></tr></tfoot></table>
<p class="note">Match printed receipt labels to the numbered rows. Review amounts, reimbursement rules, and supporting receipts manually. This tool does not verify receipts or approve expenses.</p></body></html>'''
    Path(path).write_text(html, encoding="utf-8")


def main():
    p = argparse.ArgumentParser(description="Generate a sorted, numbered receipt CSV and printable HTML cover sheet (offline)")
    p.add_argument("input_csv", help="CSV with date,vendor,amount,description")
    p.add_argument("--project", required=True, help="Project name for cover sheet")
    p.add_argument("--out-prefix", default="wrapout", help="Output file prefix")
    a = p.parse_args()
    rows = parse_receipts(a.input_csv)
    export_csv(rows, a.out_prefix + "_numbered.csv")
    export_html(rows, a.project, a.out_prefix + "_cover.html")
    print(f"Generated {len(rows)} receipt rows; total ${sum((r['amount'] for r in rows), Decimal('0')):,.2f}")


if __name__ == "__main__":
    main()
