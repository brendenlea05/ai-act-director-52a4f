# Property photo-manifest preflight (experimental)

**What it does:** Checks a CSV index of photo filenames, room labels and capture timestamps for missing required fields, duplicate filenames within a visit, unsupported filename extensions and invalid/ambiguous timestamps. Runs locally with Python standard library; does not open, upload, geolocate, classify or analyze actual photos.

**Why:** Home-watch and property-documentation providers sell reports containing timestamped photos. A missing/duplicate photo reference is an avoidable clerical issue, but this proof of concept has **not** been validated with any provider and is not an inspection product.

Run `python photo_manifest_qc.py sample_manifest.csv` to see five flags across seven **entirely fictional** rows. Run `python test_photo_manifest_qc.py` to verify the sample and a clean case. Exit code 1 means review flags, 2 means malformed input.

No image/content review, no proof that the photos exist, no EXIF verification, no accuracy, insurance, legal, licensing or compliance certification. A person must verify all results before use. Never send tenant/property images or identifying addresses without the property owner's authorization and an agreed secure handling process.

A potential fixed-scope paid **metadata-only** pilot would require separate buyer consent, agreed CSV schema, data handling and acceptance criteria; none has been sold or promised.
