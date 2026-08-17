#!/usr/bin/env python3
"""Small regression checks for accountability.py."""

import json
import pathlib
import sys
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs


sys.path.insert(0, str(pathlib.Path(__file__).parent))
import accountability  # noqa: E402
import charge  # noqa: E402


class AccountabilityTests(unittest.TestCase):
    def test_ledger_round_trip_is_standard_json(self):
        ledger = accountability.empty_ledger()
        self.assertEqual(accountability.parse_ledger(json.dumps(ledger)), ledger)

    def test_malformed_json_fails_closed(self):
        with self.assertRaises(accountability.AccountabilityError):
            accountability.parse_ledger("not json")

    def test_amount_and_due_validation(self):
        self.assertEqual(accountability.parse_amount("1"), "1.00")
        for amount in ("0.99", "1.001", "nan"):
            with self.assertRaises(accountability.AccountabilityError):
                accountability.parse_amount(amount)
        with self.assertRaises(accountability.AccountabilityError):
            accountability.parse_due("2026-08-14T09:00:00")

    def test_transition_prevents_repeat_charge(self):
        item = {"status": "awaiting-confirmation", "events": []}
        accountability.transition(item, "awaiting-confirmation", "charging")
        with self.assertRaises(accountability.AccountabilityError):
            accountability.transition(item, "awaiting-confirmation", "charging")

    def test_dry_run_charge_request(self):
        captured = {}

        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *_):
                return False

            def read(self):
                return b'{"id":"dry","amount":1,"username":"devin"}'

        def fake_urlopen(request, timeout):
            captured.update(parse_qs(request.data.decode()))
            self.assertEqual(timeout, 20)
            return Response()

        commitment = {"id": "acct-test", "amount_usd": "1.00"}
        with patch.object(charge, "urlopen", fake_urlopen):
            result = charge.request_charge(commitment, True, "secret", "devin")
        self.assertEqual(result["id"], "dry")
        self.assertEqual(captured["dryrun"], ["true"])
        self.assertEqual(captured["amount"], ["1.00"])


if __name__ == "__main__":
    unittest.main()
