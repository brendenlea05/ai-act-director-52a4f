# Distributor Reorder Recovery — exploratory pilot (not a commercial launch)

**Status:** Offline prototype; no paying clients, no automatic outreach, no AI model or integration. Built to validate a hypothesis with packaging and consumables distributors. Do not advertise as a production SaaS.

## What it does

Reads an opt-in, preferably anonymized order-history CSV and groups orders by `account_id`. Estimates each account's historical reorder interval using the median gap between distinct order dates. Flags accounts that are past their observed interval for **human review**. Does not predict demand, identify purchase intent, verify opt-outs, or prove lost revenue.

- `REVIEW_OVERDUE`: days since latest order at least 1.5 times estimated cycle **and** at least seven days past cycle.
- `REVIEW_DUE`: at least 85% of estimated cycle elapsed, but not overdue.
- `ON_CADENCE`: below due threshold.
- `INSUFFICIENT_PATTERN`: one distinct order date or median cycle under seven days.

This intentionally conservative heuristic is NOT a trained AI model. Seasonal demand, account churn, contracts, new order channels, closed quotes and customer contact preferences must be reviewed manually.

## Test it (Python 3.9+; no packages or accounts)

```bash
python3 experiments/reorder-recovery/reorder_review.py --self-test
python3 experiments/reorder-recovery/reorder_review.py experiments/reorder-recovery/sample_orders.csv --as-of 2026-10-29 --output review.csv
# For a real consented pilot, provide a separate suppression file:
# printf 'account_id\nA101\n' > suppress.csv
# python3 experiments/reorder-recovery/reorder_review.py experiments/reorder-recovery/sample_orders.csv --as-of 2026-10-29 --suppress-csv suppress.csv --output review_filtered.csv
```

Required CSV columns: `account_id,account_name,order_id,order_date,order_total`. Date format is `YYYY-MM-DD`; `order_total` must be a nonnegative numeric amount in a consistent currency. All names in the sample file are fictional.

Outputs an Excel-safe review CSV with order counts, historical total (NOT recoverable revenue), last order date, median cadence, days elapsed and review notes. Duplicate identical order IDs are ignored; conflicting duplicates and future-dated orders are rejected.

## Data safety and next validation

No network or email code is present. Do not commit actual client order histories, customer contact information, or confidential prices to this public repository. Obtain explicit permission before handling real exports; remove identifying details, and avoid customer-facing emails until the business approves each message. The output is an internal triage list only. Optional `--suppress-csv` takes a separate CSV with an `account_id` header and excludes matching account IDs entirely from the review report. This is a *manual* do-not-contact/opt-out exclusion aid, not proof that consent has been checked. A distributor must supply and maintain the authoritative suppression list; absent that list, the program cannot know customer contact preferences. Never use the review output to auto-send messages.

**Commercial validation needed:** A distributor must confirm that manual reorder-lag review is painful enough to pay for, which exports are available, how seasonality and account exclusions work, and whether a limited, paid pilot can be scoped without recurring vendor costs. No customer revenue has been collected for this concept.
