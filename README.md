# LineVerity

A practical, browser-based tool for reviewing supplier invoices against purchase orders and goods received.

**[Open the free invoice checker](https://lineverity-invoice-review.deed.page/)** · [Download blank CSV templates](https://lineverity-invoice-review.deed.page/free-invoice-csv-templates.html) · [See the supplier follow-up kit](https://lineverity-invoice-review.deed.page/supplier-recovery-kit.html)

## What it checks

The tool compares three CSV exports at the purchase-order and SKU level:

| Input | Useful columns |
| --- | --- |
| Purchase orders | PO, SKU, ordered quantity, agreed unit price |
| Goods receipts | PO, SKU, quantity actually accepted |
| Vendor invoices | Invoice number, PO, SKU, billed quantity, billed unit price |

It highlights higher billed unit prices, invoiced quantities greater than received or ordered quantities, invoice lines with no matching PO and possible repeated lines. You can download a CSV report and supplier-specific draft review packet.

**Files are processed in the browser.** The free checker has no account requirement, telemetry, application-server uploads or backend account integration. Only use records you are authorized to inspect.

## Try it in a minute

1. Open the [LineVerity checker](https://lineverity-invoice-review.deed.page/#app).
2. Click **Load example data** for an entirely fictional demonstration, or select three CSV exports.
3. Confirm the suggested column mapping and choose a unit-price tolerance.
4. Compare the files and download a report or supplier review packet.

The example is intentionally fictional. Numbers in a generated report are preliminary discrepancies to investigate, not confirmed savings, refunds or fraud.

## What it doesn't do

LineVerity doesn't parse scanned PDFs, read XLSX files directly, automatically reconcile taxes or freight, connect to an ERP or accounting ledger, contact suppliers, or approve or stop payments. Normalize currencies and units of measure before comparing. Verify findings against contracts, receipt dates, credits and original records.

## Beyond the free tool

Two optional digital toolkits are available. Both are **one-time purchases**, not subscriptions. Each ZIP is sent **by email within 24 hours of verified payment**, normally sooner—not an instant download.

| Toolkit | Price | Contents | Checkout |
| --- | ---: | --- | --- |
| [Supplier Recovery Action Kit](https://lineverity-invoice-review.deed.page/supplier-recovery-kit.html) | $19 | Six-tab Excel case tracker, supplier response log, evidence checklist, worked example, five inquiry drafts, CSV templates and 21-step review SOP | [Secure $19 checkout](https://buy.stripe.com/4gMbIU0dobFMdLh6JL7AI00) |
| Supplier Price Variance Control Kit | $49 | Offline Excel price-review workbook for up to 250 invoice lines, dashboard, follow-up log, worked example, five supplier correspondence drafts and blank/example CSVs | [Secure $49 checkout](https://buy.stripe.com/cNibIU5xIcJQ9v13xz7AI01) |

The $49 kit is for reviewing agreed-versus-billed supplier unit prices after normalizing currencies and units. Findings require human verification; neither kit guarantees savings, supplier responses or recoveries. Both are delivered to the email address used at checkout. Support and refund requests: [brendenlea05ai@gmail.com](mailto:brendenlea05ai@gmail.com). The current Stripe merchant on the bank statement is **GROVIABID AI**, the existing authorized merchant account used for LineVerity. The free browser checker and CSV templates remain free.

## Project and contact

This branch contains the source for the public, zero-dependency LineVerity beta at deed.page. The production publishing workflow is `.github/workflows/publish-lineverity.yml`; calculations are in `engine.js`, interface logic in `app.js`, and optional report-packet output in `packet.js`. Source changes are not public until a deployment is separately verified.

Local checks, when Node.js and Python dependencies are available:

```sh
node tests/test.js
node tests/packet.test.js
```

Source files contain no production customer invoices or paid-kit download archive. The private purchased ZIP is not distributed from GitHub.

Support: [brendenlea05ai@gmail.com](mailto:brendenlea05ai@gmail.com). Please don't send confidential supplier invoices or sensitive financial documents by email.

[Privacy](https://lineverity-invoice-review.deed.page/privacy.html) · [Beta terms](https://lineverity-invoice-review.deed.page/terms.html)
