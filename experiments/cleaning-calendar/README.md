# Cleaning visit calendar pilot (offline, free)

A **single HTML file** that converts a cleaning-business visit CSV to an importable .ics calendar file. It is an experiment, not a hosted CRM, calendar service, reminder guarantee, or paid product.

## How to use

1. Download `index.html` and open it locally in a modern browser (phone or desktop). It does not load external scripts, upload data, or make network calls.
2. Choose a CSV with the exact header `client,next_date,interval_days,start_time,duration_minutes,notes`. See `fictional_sample.csv`. Use **consented data only**; do not post real client lists to GitHub.
3. Review the preview, download the .ics file, and import it into your preferred calendar.
4. **Verify** five test events, timezone behavior, recurrence, and whether your calendar app honors the requested 1-day alarms before using it operationally.

Each row creates a repeating event for 12 occurrences at a fixed interval in days. Use 7/14/28 for weekly/biweekly/four-week schedules. A calendar month is **not** the same as 28 or 30 days. The app does not send messages or automatic notifications itself. Re-importing may create duplicates; the tool does not synchronize changes, cancel visits, book time slots, handle multiple crews, or collect payment.

## Why explore this?

A [public Oct 26, 2026 discussion](https://www.reddit.com/r/smallbusiness/comments/1xgdcy5/crm_for_a_small_business_40_clients_and_a/) describes a solo cleaning operator with ~40 recurring clients struggling with a broken spreadsheet and seeking simple mobile reminders under $20/month. This is **market evidence, not a customer** or consent to contact that poster. [2026 competitor pricing](https://mikevidan.com/cleaning-company-scheduling-software-2026/) shows paid recurring-schedule products, but the offline pilot deliberately offers far fewer features.

An independent second niche considered in the same sweep was [nonprofit board packet automation](https://ritewaydev.com/nonprofits/board-reporting/) with published service pricing, but it requires specialist data access, compliance review and buyer discovery. We did not build or pitch that service.

## Paid-service hypothesis (not validated)

A **one-time, manually reviewed CSV migration / calendar setup** for an operator who explicitly requests it might support a small fixed fee. No customer, price acceptance, payment, subscription or guarantee exists. To request a scoped quote, contact brendenlea05ai@gmail.com. The Stripe merchant descriptor currently displays GROVIABID AI and must be disclosed before any eventual checkout. No public paid checkout exists for this pilot.

## Test record

The browser-side parser and calendar generation were exercised in an isolated JavaScript harness on Oct 30, 2026: quoted comma field, rejection of impossible date, 14-day recurrence, midnight rollover, alarm request, and absence of network APIs all passed. These are basic deterministic checks, **not** end-to-end tests of calendar import on real phones.
