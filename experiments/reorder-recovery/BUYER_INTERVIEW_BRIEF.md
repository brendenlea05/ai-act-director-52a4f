# Reorder Signals — janitorial distributor buyer interview brief (2026-10-30)

**Not a launched SaaS or paid pilot.** Existing offline rule-based CSV prototype only. No private data imported; no distributor buyer has agreed to test or pay. This is a narrow hypothesis for validation, not a claim of product-market fit.

## Segment hypothesis
Independent US janitorial/facility-supply wholesalers with repeat commercial accounts, legacy/manual order exports, and small sales teams. **Buyer:** owner or sales/operations lead. **Job to test:** once a week, identify accounts whose historical ordering has slowed and prepare a **human-reviewed** follow-up queue without requiring ERP integration or emailing customers automatically.

## Competitor / workflow evidence
- Janitorial Superstore exposes order history and a buyer-side **Buy Again** feature: https://www.janitorialsuperstore.com/pages/my-account-center . Shows repeat purchasing is an established workflow, **not** evidence that it needs our service.
- Pacto explicitly markets repeat janitorial supply ordering, saved history, multiple buyers per business, and structured requests: https://pactodistro.com/industries/cleaning-supplies . This solves **buyer ordering friction**, whereas our hypothesis is **seller-side lapsed-account review**.
- Proton.ai CRM explicitly surfaces spending gaps, at-risk accounts, and cross-sell recommendations for distributors: https://www.proton.ai/ . Direct competitor, not a new invention. G2 says a platform fee starts at $15,000/year for first tier, with CRM seats/add-ons; verify actual quotes with vendors: https://www.g2.com/products/proton-ai/pricing .
- No independent distributor interviews or customer willingness-to-pay evidence yet. Public vendor pages are competitive evidence, **not** validated pain.

## 6 discovery questions (ask without requesting private order data)
1. How does your team currently notice a recurring commercial customer has stopped ordering?
2. How often do you review order history, and who is responsible?
3. What ERP or order-export formats can you produce today without IT involvement?
4. What false alarms would make a reorder alert unhelpful (seasonality, contract end, one-time orders, stockouts, opt-outs)?
5. Is a weekly CSV/PDF review queue more useful than your existing CRM reports? What is missing from those reports?
6. If a safe, human-reviewed one-month pilot actually saved your team time, what scope and price would be worth considering? Do not suggest a validated price.

## Bounded opt-in pilot to discuss only after interest
- One synthetic demonstration first. If later authorized, accept **only an anonymized, minimum-necessary order-level CSV** via an agreed secure transfer method, not Gmail attachments by default.
- One local deterministic run; output flagged account IDs, observed cadence, days since last order, reasons to review; manual QA before use.
- No automatic customer outreach, no AI inference claims, no CRM write access, no customer PII, no guarantees of incremental revenue.
- Explicitly reject line-item exports where repeated order IDs carry conflicting amounts; normalize to **one order per row** first.
- No recurring paid commitment or new hosting until explicit case-specific authorization and commercial terms are confirmed.

**Next go/no-go gate:** A distributor confirms current manual review pain, can supply an order-level export, agrees to assess a synthetic example, and states willingness to consider a paid scoped pilot. Otherwise do not build more.
