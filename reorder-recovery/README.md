# Reorder Signals — independent distributor revenue-recovery pilot

**Status (2026-10-29): functional static, browser-only CSV prototype; not commercially launched, not AI-integrated, no paid customers or validated ROI.**

This is a separate proposed B2B venture, not LineVerity or Lea Farms. Source is intentionally isolated under `reorder-recovery/` on branch `distributor-recovery-mvp` so other project deployments are untouched.

## Current tested capabilities
- Load a CSV in-browser (required columns: `customer,email,order_date,sku,amount`; optional `order_id`).
- Group account + SKU line histories; require 3+ distinct order dates; find typical cadence by median day interval.
- Flag when the latest interval exceeds both 1.35× median cadence and 7 days beyond it.
- Rank by relative lateness and display explainable facts (last date, cadence, current gap, average historical line amount).
- Export the review queue to CSV and copy a suggested follow-up draft **for human approval**.
- Demo data is synthetic and generated relative to browser date. No external libraries, server, network requests, telemetry or file persistence.

## Run
Open `index.html` locally in a browser. Click **Run synthetic demo** or upload your own CSV. Opening local files does not require hosting; the Clipboard API may require HTTPS depending on browser restrictions. No actual customer data should be shared with the venture without documented permission.

## Important limitations
- This is rule-based analysis and **not an operating AI employee** yet. Do not advertise fully automated AI email, live ERP integration, compliance controls, attributed recovered revenue or AI predictions.
- Historical reorder timing alone does not prove customer intent; seasonality, contracts, stockouts and cancellations can produce false positives.
- CSV ingestion is capped at 3 MB; dates must be YYYY-MM-DD, amounts nonnegative, and future dates are rejected.
- Sends **no outreach** to distributor customers. Human reviewers must verify email contact legitimacy, account-specific preferences, opt-outs, available inventory and pricing.
- No security or multi-tenant customer data infrastructure exists; this is a strictly local pilot.

## One-year thesis and first market experiment
**Buyer:** independently owned specialty packaging, janitorial/industrial or irrigation distributors with repeat B2B purchasers, manual CSV/ERP order-history exports, and busy inside-sales teams. Pick ONE subvertical after talking to real buyers.

**Pain hypothesis:** missed/overdue routine repeat orders are difficult to monitor across a long-tail account base.

**Candidate commercial offer:** a low-integration managed/assisted account-health report and sales follow-up queue. Hypothesized pilot pricing around $500–$1,000/month, **not validated**.

**Validation milestones (in order):**
1. Interview 15–30 qualified distributor owners, GMs or inside-sales managers; avoid mass spam. Learn current tools, data export friction, lost revenue signals, human approval rules, budget and procurement cycle.
2. Get opt-in agreement for a narrowly scoped *paid* pilot (or evidence the niche is not viable). Do not misrepresent the demo as production-ready.
3. Pilot using properly authorized exports or approved anonymized datasets. Track both recovered orders and an honest counterfactual/control to avoid false attribution.
4. Add hardened ingestion, audit logs, explicit reviewer approvals, unsubscribes, security and integrations as demand requires. Only then consider paid API-based language generation and controlled outbound automations financed by actual revenue.
5. Develop reliable onboarding, support and documentation so a hired operator can eventually manage the product.

## Competitive reality
Proton.ai's October 8, 2026 guide explicitly covers ranking late reorders: https://www.proton.ai/blog/which-accounts-should-reps-call-this-week

NAW also discusses these buyer needs: https://www.naw.org/mdm/posts/ai-that-makes-sales-more-human/

**Differentiation hypothesis (not proven):** far narrower, low-integration, upload-first tool for smaller distributors that do not want a comprehensive CRM implementation.

## Zero-dollar / deployment rule
Existing Vercel Hobby terms prohibit commercial SaaS. GitHub Pages also prohibits using Pages as free hosting for a commercial SaaS site. Render free static sites include outbound bandwidth; excess use **can incur metered charges** when a payment method is attached. Do not deploy without verifying billing safeguards and zero-dollar safe usage. Code hosted in this repo is **not** a published live web app.

## Actual evidence ledger
- 2026-10-29: Independent opportunity added to ongoing hourly zero-upfront operator.
- 2026-10-29: Prototype source pushed to branch `distributor-recovery-mvp`, verified with synthetic dataset: 20 valid lines across 5 accounts and 4 overdue account–product signals.
- 2026-10-29: No verified customers, buyer interviews, live public app, payment links or paid pilots. These must not be claimed without evidence.
