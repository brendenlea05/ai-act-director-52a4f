# Film / TV receipt wrap-out cover sheet — zero-dependency sample

**Status:** Experimental offline prototype, not a client contract, not a live hosted app, and not an accounting, tax, reimbursement, OCR, or receipt-verification service. Uses fictional example data.

A film/TV production designer publicly described needing date-sorted receipts, receipt numbering, and a petty-cash cover sheet for reimbursement wrap-outs (Reddit r/bookkeepingjobs, October 25, 2026): https://www.reddit.com/r/bookkeepingjobs/comments/1xf2u8d/i_think_i_need_a_bookkeeper_or_adjacent/ . This prototype addresses only the **spreadsheet/cover-sheet preparation** portion, not scanning, bookkeeping, or physical receipt handling.

## Run (Python 3, no pip installs or API calls)

    python wrapout.py sample_receipts.csv --project "Fictional Commercial Shoot" --out-prefix demo
    python test_wrapout.py

Outputs demo_numbered.csv and demo_cover.html (open the HTML locally and print to PDF/paper). Sorts by ISO date, numbers receipts R001..., calculates total, checks dates/amounts, HTML-escapes content and protects text against spreadsheet-formula injection. Does **not** inspect receipts, detect duplicate charges, validate expenses against company policy, connect bank accounts, or submit reimbursements. Manual review is required.

## Optional paid fixed-scope service validation

A prospective client could request **manual CSV formatting and customized printable cover-sheet layout** for a defined number of rows and projects, subject to a written quote and secure handling agreement. No buyer has accepted or paid for this work. Contact: brendenlea05ai@gmail.com. No receipt photos or financial data should be emailed unsolicited.

**Source/competitive context:** Saturation offers production expense software (free tier and $32/month Pro), https://saturation.io/ . Periscope advertises production accounting at $49/month, https://periscopeapps.com/accounting/ . These are competitors, not endorsements or partners.
