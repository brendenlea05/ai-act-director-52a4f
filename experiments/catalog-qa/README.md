# Catalog CSV quality-control pilot (fictional data)

A narrow, auditable offline sample for e-commerce catalog operations. It is **not** an automated enrichment service and does not guess product attributes. It flags rows requiring a human decision rather than inventing missing values.

Run with Python 3 standard library only:

```bash
python catalog_qa.py sample_catalog.csv cleaned.csv exceptions.csv
python test_catalog_qa.py
```

**Input columns:** `sku`, `product_name`, `category`, `price`. **Outputs:** normalized copy with source row numbers and `REVIEW` status; separate exception report with reasons. Checks include blank fields, duplicate SKU (case-insensitive), invalid prices and potentially unsafe spreadsheet formula prefixes. The fictional six-row sample contains three review cases; synthetic test passes locally.

**Scope/limitations:** This demonstration does not determine correct categories, fetch missing attributes, infer brands or perform human review. No client data is included. Before accepting a paid batch, agree on exact input schema, mapping rules, review/acceptance checks, data handling and delivery date. Do not upload private customer files to public GitHub. The sample is a proof of capability, not evidence of paid work or guaranteed accuracy.
