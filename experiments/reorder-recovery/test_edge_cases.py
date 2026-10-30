"""Safety/edge-case tests for the offline reorder review prototype.

Only fictional records; no customer data or network requests.
"""
import io
import unittest
from datetime import date

from reorder_review import analyze, parse_orders, safe_csv_value, write_report, read_suppression_csv, exclude_suppressed


HEADER = "account_id,account_name,order_id,order_date,order_total\n"


class ReorderEdgeCases(unittest.TestCase):
    def test_same_order_id_in_different_accounts_is_not_merged(self):
        # Some distributors use account-scoped order numbers.
        rows = parse_orders(io.StringIO(
            HEADER +
            "A,Alpha,100,2026-01-01,10\n"
            "A,Alpha,101,2026-02-01,20\n"
            "B,Beta,100,2026-01-15,30\n"
            "B,Beta,101,2026-02-15,40\n"
        ))
        report = analyze(rows, date(2026, 10, 29))
        self.assertEqual({r["account_id"]: r["order_count"] for r in report}, {"A": 2, "B": 2})

    def test_conflicting_duplicate_within_account_rejected(self):
        with self.assertRaisesRegex(ValueError, "conflicting duplicate"):
            parse_orders(io.StringIO(
                HEADER + "A,Alpha,1,2026-01-01,10\n"
                "A,Alpha,1,2026-01-01,999\n"
            ))

    def test_same_day_orders_are_not_a_repeat_cycle(self):
        rows = parse_orders(io.StringIO(
            HEADER + "A,Alpha,1,2026-01-01,10\n"
            "A,Alpha,2,2026-01-01,20\n"
        ))
        report = analyze(rows, date(2026, 10, 29))
        self.assertEqual(report[0]["status"], "INSUFFICIENT_PATTERN")

    def test_future_order_date_rejected(self):
        rows = parse_orders(io.StringIO(HEADER + "A,Alpha,1,2026-12-01,10\n"))
        with self.assertRaisesRegex(ValueError, "after the as-of date"):
            analyze(rows, date(2026, 10, 29))

    def test_negative_and_nonfinite_amounts_rejected(self):
        for value in ["-1", "nan", "inf", "-inf"]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    parse_orders(io.StringIO(HEADER + f"A,Alpha,1,2026-01-01,{value}\n"))

    def test_missing_required_header_rejected(self):
        with self.assertRaisesRegex(ValueError, "Required columns"):
            parse_orders(io.StringIO("account_id,order_id\nA,1\n"))

    def test_explicit_do_not_contact_accounts_are_excluded(self):
        orders = parse_orders(io.StringIO(
            HEADER + "A,Alpha,1,2026-01-01,100\n"
            "A,Alpha,2,2026-02-01,100\n"
            "B,Beta,1,2026-01-01,100\n"
            "B,Beta,2,2026-02-01,100\n"
        ))
        report = analyze(orders, date(2026, 10, 29))
        suppressed = read_suppression_csv(io.StringIO("account_id\nA\n"))
        remaining = exclude_suppressed(report, suppressed)
        self.assertEqual([r["account_id"] for r in remaining], ["B"])

    def test_suppression_csv_rejects_missing_header(self):
        with self.assertRaisesRegex(ValueError, "account_id header"):
            read_suppression_csv(io.StringIO("name\nAlpha\n"))

    def test_formula_like_text_escaped_in_csv_output(self):
        rows = [{
            "account_id": "=2+2", "account_name": " @SUM(A1)", "order_count": 2,
            "last_order_date": "2026-01-01", "estimated_cycle_days": 30,
            "days_since_last_order": 300, "days_past_cycle": 270,
            "status": "REVIEW_OVERDUE", "historical_order_total": "10.00",
            "review_note": "+RUN",
        }]
        out = io.StringIO()
        write_report(rows, out)
        data = out.getvalue()
        self.assertIn("'=2+2", data)
        self.assertIn("' @SUM(A1)", data)
        self.assertIn("'+RUN", data)
        self.assertEqual(safe_csv_value("safe"), "safe")


if __name__ == "__main__":
    unittest.main()
