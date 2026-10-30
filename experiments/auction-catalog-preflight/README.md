# Auction catalog CSV structural preflight — experimental sample

Offline, Python standard-library utility. For a CSV with a lot identifier and title/description, flags missing or duplicate lot numbers, blank titles, blank image references (when an image column exists), and potential spreadsheet formula cells. Outputs JSON with row numbers for **human review**.

Does **not** identify objects, verify photos, estimate values, certify condition, validate a particular auction platform's import schema, or alter original CSVs. Sample data are entirely fictional. No bidder or consignor information, real customer, or paid work is involved.

Run `python test_catalog_preflight.py` and `python catalog_preflight.py sample_auction.csv --output issues.json`. Files stay on the local machine. Agree on field names, handling, and scope before client work; never upload private client data to public GitHub. Some spreadsheet formula flags (e.g., text beginning with a minus sign) may need manual dismissal.
