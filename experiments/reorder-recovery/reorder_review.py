#!/usr/bin/env python3
"""Reorder Recovery Pilot: deterministic, offline reorder-lag review.

Uses only Python's standard library. No network calls, email sending, AI API,
customer database access, or third-party dependencies. Human review required.
"""
from __future__ import annotations

import argparse
import csv
import io
import statistics
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

REQUIRED = {"account_id", "account_name", "order_id", "order_date", "order_total"}
OUTPUT_FIELDS = [
    "account_id", "account_name", "order_count", "last_order_date",
    "estimated_cycle_days", "days_since_last_order", "days_past_cycle",
    "status", "historical_order_total", "review_note",
]


def parse_orders(source):
    """Return deduplicated order rows; reject invalid or ambiguous input."""
    reader = csv.DictReader(source)
    if not reader.fieldnames or not REQUIRED.issubset(set(reader.fieldnames)):
        raise ValueError("Required columns: " + ", ".join(sorted(REQUIRED)))
    orders = {}
    names = {}
    for line, row in enumerate(reader, start=2):
        if not any(str(v or "").strip() for v in row.values()):
            continue
        if None in row:
            raise ValueError(f"Row {line}: too many columns")
        account = (row["account_id"] or "").strip()
        name = (row["account_name"] or "").strip()
        order_id = (row["order_id"] or "").strip()
        raw_date = (row["order_date"] or "").strip()
        if not account or not name or not order_id:
            raise ValueError(f"Row {line}: account, name and order_id are required")
        try:
            ordered = date.fromisoformat(raw_date)
        except ValueError as exc:
            raise ValueError(f"Row {line}: order_date must be YYYY-MM-DD") from exc
        try:
            total = float((row["order_total"] or "").strip())
        except ValueError as exc:
            raise ValueError(f"Row {line}: order_total must be numeric") from exc
        if not (0 <= total < 1e12):
            raise ValueError(f"Row {line}: invalid nonnegative order_total")
        key = (account, order_id)
        if key in orders:
            if orders[key] != (name, ordered, total):
                raise ValueError(f"Row {line}: conflicting duplicate order_id {order_id}")
            continue
        if account in names and names[account] != name:
            raise ValueError(f"Row {line}: inconsistent account_name for {account}")
        names[account] = name
        orders[key] = (name, ordered, total)
    if not orders:
        raise ValueError("No valid orders found")
    return [(account, order_id, *values) for (account, order_id), values in orders.items()]


def analyze(orders, as_of: date, minimum_orders: int = 2, lag_multiplier: float = 1.5):
    """Return explainable flags, never claims of recovered revenue."""
    by_account = defaultdict(list)
    for account, order_id, name, ordered, total in orders:
        if ordered > as_of:
            raise ValueError(f"Order {order_id} is dated after the as-of date")
        by_account[account].append((ordered, order_id, name, total))
    result = []
    for account, entries in by_account.items():
        entries.sort(key=lambda x: (x[0], x[1]))
        unique_dates = sorted({e[0] for e in entries})
        last = unique_dates[-1]
        elapsed = (as_of - last).days
        count = len(entries)
        historical = sum(e[3] for e in entries)
        cycle = None
        if count >= minimum_orders and len(unique_dates) >= 2:
            gaps = [(b - a).days for a, b in zip(unique_dates, unique_dates[1:])]
            cycle = round(statistics.median(gaps), 1)
        if cycle is None or cycle < 7:
            status = "INSUFFICIENT_PATTERN"
            note = "Too few distinct order dates or cycle shorter than seven days; review manually"
            past = ""
        else:
            past = round(elapsed - cycle, 1)
            if elapsed >= max(cycle * lag_multiplier, cycle + 7):
                status = "REVIEW_OVERDUE"
                note = "Past observed cadence; check seasonality, contracts, opt-outs and open quotes"
            elif elapsed >= cycle * 0.85:
                status = "REVIEW_DUE"
                note = "Near observed cadence; human review before any outreach"
            else:
                status = "ON_CADENCE"
                note = "No follow-up recommended by timing alone"
        result.append({
            "account_id": account, "account_name": entries[-1][2],
            "order_count": count, "last_order_date": last.isoformat(),
            "estimated_cycle_days": cycle if cycle is not None else "",
            "days_since_last_order": elapsed, "days_past_cycle": past,
            "status": status, "historical_order_total": f"{historical:.2f}",
            "review_note": note,
        })
    rank = {"REVIEW_OVERDUE": 0, "REVIEW_DUE": 1, "INSUFFICIENT_PATTERN": 2, "ON_CADENCE": 3}
    return sorted(result, key=lambda x: (rank[x["status"]], x["account_id"]))


def safe_csv_value(value):
    """Neutralize Excel formula injection in CSV text fields."""
    s = str(value)
    if s and (s[0] in "=+-@" or s.lstrip().startswith(("=", "+", "-", "@"))):
        return "'" + s
    return s


def write_report(rows, output):
    writer = csv.DictWriter(output, fieldnames=OUTPUT_FIELDS)
    writer.writeheader()
    for row in rows:
        writer.writerow({k: safe_csv_value(row[k]) for k in OUTPUT_FIELDS})


def self_test():
    sample = io.StringIO(
        "account_id,account_name,order_id,order_date,order_total\n"
        "A,Sample Co,A1,2026-01-01,100\n"
        "A,Sample Co,A2,2026-02-01,100\n"
        "A,Sample Co,A3,2026-03-01,100\n"
        "B,New Buyer,B1,2026-10-25,20\n"
        "C,Regular Buyer,C1,2026-09-01,10\n"
        "C,Regular Buyer,C2,2026-10-01,10\n"
        "C,Regular Buyer,C2,2026-10-01,10\n"
    )
    rows = analyze(parse_orders(sample), date(2026, 10, 29))
    by_id = {r["account_id"]: r for r in rows}
    assert by_id["A"]["status"] == "REVIEW_OVERDUE"
    assert by_id["A"]["estimated_cycle_days"] == 29.5
    assert by_id["B"]["status"] == "INSUFFICIENT_PATTERN"
    assert by_id["C"]["status"] == "REVIEW_DUE"
    assert by_id["C"]["order_count"] == 2
    assert safe_csv_value("=2+2") == "'=2+2"
    assert safe_csv_value(" @SUM(A1)") == "' @SUM(A1)"
    try:
        parse_orders(io.StringIO("account_id,account_name,order_id,order_date,order_total\nA,X,1,wrong,10\n"))
        raise AssertionError("invalid date accepted")
    except ValueError:
        pass
    print("PASS: cadence, overdue, due, duplicates, insufficient history, CSV safety, invalid dates")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv", nargs="?", help="Order-history CSV, no customer PII needed")
    parser.add_argument("--as-of", default=date.today().isoformat(), help="YYYY-MM-DD reference date")
    parser.add_argument("--output", default="reorder_review.csv", help="Output CSV path")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if not args.input_csv:
        parser.error("Provide input_csv or --self-test")
    try:
        as_of = date.fromisoformat(args.as_of)
        with open(args.input_csv, encoding="utf-8-sig", newline="") as source:
            rows = analyze(parse_orders(source), as_of)
        with open(args.output, "w", encoding="utf-8", newline="") as out:
            write_report(rows, out)
        print(f"Wrote {len(rows)} account review rows to {args.output}; no messages sent")
    except (ValueError, OSError) as exc:
        parser.exit(2, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
