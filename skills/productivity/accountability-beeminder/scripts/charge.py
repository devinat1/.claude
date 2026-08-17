#!/usr/bin/env python3
"""Charge one fairness-confirmed accountability commitment through BeeMinder."""

from __future__ import annotations

import argparse
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import accountability


def request_charge(commitment: dict, dry_run: bool, token: str, username: str) -> dict:
    form = {
        "auth_token": token,
        "user_id": username,
        "amount": commitment["amount_usd"],
        "note": f"Accountability commitment {commitment['id']}",
    }
    if dry_run:
        form["dryrun"] = "true"
    request = Request(
        "https://www.beeminder.com/api/v1/charges.json",
        data=urlencode(form).encode(),
        method="POST",
    )
    try:
        with urlopen(request, timeout=20) as response:
            return json.loads(response.read())
    except HTTPError as error:
        detail = error.read().decode(errors="replace")[:500]
        raise accountability.AccountabilityError(
            f"BeeMinder HTTP {error.code}: {detail}"
        ) from error
    except (URLError, TimeoutError, json.JSONDecodeError) as error:
        raise accountability.AccountabilityError(
            f"BeeMinder request failed: {error}"
        ) from error


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", required=True)
    parser.add_argument("--fair-confirmed", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--ledger", type=accountability.Path, default=accountability.DEFAULT_LEDGER)
    args = parser.parse_args()

    if not args.fair_confirmed:
        raise accountability.AccountabilityError("--fair-confirmed is required")
    token = os.environ.get("BEEMINDER_AUTH_TOKEN")
    username = os.environ.get("BEEMINDER_USERNAME")
    if not token or not username:
        raise accountability.AccountabilityError(
            "BEEMINDER_AUTH_TOKEN and BEEMINDER_USERNAME must be set"
        )

    store = accountability.Store(args.ledger)
    commitment = accountability.find(store.load(), args.id)
    if commitment.get("status") != "awaiting-confirmation":
        raise accountability.AccountabilityError(
            f"commitment is {commitment.get('status')}, expected awaiting-confirmation"
        )
    if args.dry_run:
        accountability.output(request_charge(commitment, True, token, username))
        return 0

    accountability.mutate(
        store, args.id, "awaiting-confirmation", "charging",
        fairness_confirmed_at=accountability.now_iso(),
    )
    charge = request_charge(commitment, False, token, username)
    accountability.output(accountability.mutate(
        store, args.id, "charging", "charged",
        charge={
            "id": charge.get("id"),
            "amount": charge.get("amount"),
            "charged_at": accountability.now_iso(),
        },
        settled_at=accountability.now_iso(),
    ))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except accountability.AccountabilityError as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
