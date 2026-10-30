import csv
from pathlib import Path
from index_preflight import check

rows = list(csv.DictReader((Path(__file__).parent / "sample_index.csv").open()))
issues = check(rows)
kinds = {x[1] for x in issues}
assert {"duplicate_heading","duplicate_locator","reversed_range","sort_order","missing_target","self_reference"}.issubset(kinds), issues
clean = [dict(term="Alpha",locators="1;3-5",see="",see_also="Beta"), dict(term="Beta",locators="9",see="",see_also="")]
assert not check(clean), check(clean)
print(f"PASS: clean example has zero issues; synthetic bad example flagged {len(issues)} review items")
