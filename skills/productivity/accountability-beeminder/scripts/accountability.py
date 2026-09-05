#!/usr/bin/env python3
"""Manage accountability commitments in a JSON ledger."""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path


DEFAULT_LEDGER = Path(os.environ.get("AGENTIC_HOME", Path.home() / ".agentic")).expanduser() / "state" / "accountability-beeminder.json"


class AccountabilityError(Exception):
    pass


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def empty_ledger() -> dict:
    return {"version": 1, "commitments": []}


def parse_ledger(content: str) -> dict:
    try:
        ledger = json.loads(content)
    except json.JSONDecodeError as error:
        raise AccountabilityError(f"invalid ledger JSON: {error}") from error
    if ledger.get("version") != 1 or not isinstance(ledger.get("commitments"), list):
        raise AccountabilityError("unsupported ledger schema")
    return ledger


class Store:
    def __init__(self, path: Path):
        self.path = path

    def load(self) -> dict:
        if not self.path.exists():
            return empty_ledger()
        try:
            return parse_ledger(self.path.read_text())
        except OSError as error:
            raise AccountabilityError(f"cannot read ledger: {error}") from error

    def save(self, ledger: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(".tmp")
        try:
            temporary.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n")
            os.replace(temporary, self.path)
        except OSError as error:
            raise AccountabilityError(f"cannot save ledger: {error}") from error


def parse_due(value: str) -> datetime:
    try:
        due = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise AccountabilityError("due must be ISO-8601") from error
    if due.tzinfo is None or due.utcoffset() is None:
        raise AccountabilityError("due must include a timezone offset")
    return due


def parse_amount(value: str) -> str:
    try:
        amount = Decimal(value)
    except InvalidOperation as error:
        raise AccountabilityError("amount must be a number") from error
    if not amount.is_finite() or amount < Decimal("1"):
        raise AccountabilityError("amount must be at least $1")
    if amount.as_tuple().exponent < -2:
        raise AccountabilityError("amount may have at most two decimal places")
    return f"{amount:.2f}"


def find(ledger: dict, commitment_id: str) -> dict:
    matches = [item for item in ledger["commitments"] if item.get("id") == commitment_id]
    if len(matches) != 1:
        raise AccountabilityError(f"commitment {commitment_id!r} not found or duplicated")
    return matches[0]


def event(commitment: dict, action: str, **details: object) -> None:
    commitment.setdefault("events", []).append({"at": now_iso(), "action": action, **details})


def transition(commitment: dict, expected: str, target: str, **fields: object) -> None:
    if commitment.get("status") != expected:
        raise AccountabilityError(
            f"commitment is {commitment.get('status')}, expected {expected}"
        )
    commitment.update(status=target, **fields)
    event(commitment, target)


def output(value: object) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False))


def mutate(store: Store, commitment_id: str, expected: str, target: str, **fields: object) -> dict:
    ledger = store.load()
    commitment = find(ledger, commitment_id)
    transition(commitment, expected, target, **fields)
    store.save(ledger)
    return commitment


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("init")

    add = commands.add_parser("add")
    add.add_argument("--goal", required=True)
    add.add_argument("--due", required=True)
    add.add_argument("--amount", required=True)
    add.add_argument("--verifier-type", choices=("objective", "subjective"), required=True)
    add.add_argument("--verification", required=True)
    add.add_argument("--id")

    due = commands.add_parser("due")
    due.add_argument("--now", default=now_iso())

    show = commands.add_parser("show")
    show.add_argument("--id")

    complete = commands.add_parser("complete")
    complete.add_argument("--id", required=True)
    complete.add_argument("--evidence", required=True)

    miss = commands.add_parser("miss")
    miss.add_argument("--id", required=True)
    miss.add_argument("--evidence", required=True)

    dispute = commands.add_parser("dispute")
    dispute.add_argument("--id", required=True)
    dispute.add_argument("--reason", required=True)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    store = Store(args.ledger)

    if args.command == "init":
        ledger = store.load()
        store.save(ledger)
        output({"initialized": str(args.ledger)})
    elif args.command == "add":
        due = parse_due(args.due)
        amount = parse_amount(args.amount)
        ledger = store.load()
        commitment_id = args.id or f"acct-{datetime.now():%Y%m%d}-{uuid.uuid4().hex[:8]}"
        if any(item.get("id") == commitment_id for item in ledger["commitments"]):
            raise AccountabilityError(f"commitment {commitment_id!r} already exists")
        commitment = {
            "id": commitment_id,
            "created_at": now_iso(),
            "due_at": due.isoformat(),
            "goal": args.goal,
            "amount_usd": amount,
            "verifier": {"type": args.verifier_type, "rule": args.verification},
            "status": "pending",
            "events": [],
        }
        event(commitment, "created")
        ledger["commitments"].append(commitment)
        store.save(ledger)
        output(commitment)
    elif args.command == "due":
        cutoff = parse_due(args.now)
        output([
            item for item in store.load()["commitments"]
            if item.get("status") == "pending" and parse_due(item["due_at"]) <= cutoff
        ])
    elif args.command == "show":
        ledger = store.load()
        output(find(ledger, args.id) if args.id else ledger)
    elif args.command == "complete":
        output(mutate(
            store, args.id, "pending", "completed",
            evidence=args.evidence, assessed_at=now_iso(),
        ))
    elif args.command == "miss":
        output(mutate(
            store, args.id, "pending", "awaiting-confirmation",
            evidence=args.evidence, assessed_at=now_iso(),
        ))
    elif args.command == "dispute":
        output(mutate(
            store, args.id, "awaiting-confirmation", "disputed",
            dispute_reason=args.reason, settled_at=now_iso(),
        ))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AccountabilityError as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
