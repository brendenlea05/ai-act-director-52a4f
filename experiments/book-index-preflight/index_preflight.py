"""Offline preflight of a copyedited book-index CSV (not professional indexing)."""
import argparse
import csv
import re
from collections import Counter

LOCATOR = re.compile(r"^(\d+)(?:-(\d+))?$")
REQUIRED = {"term", "locators", "see", "see_also"}

def check(rows):
    rows = list(rows)
    issues = []
    normalized = [(r.get("term") or "").strip().casefold() for r in rows]
    counts = Counter(normalized)
    known = set(normalized)
    previous = ""
    for line, (row, term) in enumerate(zip(rows, normalized), start=2):
        if not term:
            issues.append((line, "empty_term", "Index heading is empty"))
        elif counts[term] > 1:
            issues.append((line, "duplicate_heading", row["term"]))
        if term and previous and term < previous:
            issues.append((line, "sort_order", "Heading is out of alphabetical order"))
        if term:
            previous = term
        locators = [s.strip() for s in (row.get("locators") or "").split(";") if s.strip()]
        if len(locators) != len(set(locators)):
            issues.append((line, "duplicate_locator", "Repeated page locator"))
        for locator in locators:
            m = LOCATOR.fullmatch(locator)
            if not m:
                issues.append((line, "locator_format", locator))
            elif m.group(2) and int(m.group(2)) < int(m.group(1)):
                issues.append((line, "reversed_range", locator))
        for field in ("see", "see_also"):
            for target in [t.strip().casefold() for t in (row.get(field) or "").split(";") if t.strip()]:
                if target == term:
                    issues.append((line, "self_reference", field))
                elif target not in known:
                    issues.append((line, "missing_target", f"{field}: {target}"))
        if (row.get("see") or "").strip() and locators:
            issues.append((line, "see_with_locators", "See-reference also has page locators; review style"))
    return issues

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("index_csv", help="UTF-8 CSV with term,locators,see,see_also")
    args = p.parse_args()
    with open(args.index_csv, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or not REQUIRED.issubset(reader.fieldnames):
            p.error("Required columns: term,locators,see,see_also")
        issues = check(reader)
    print(f"{len(issues)} potential issue(s) (manual editorial review required)")
    for line, kind, detail in issues:
        print(f"CSV row {line}: {kind}: {detail}")

if __name__ == "__main__":
    main()
