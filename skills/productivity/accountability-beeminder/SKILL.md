---
name: accountability-beeminder
description: Create and settle evidence-backed accountability commitments with user-chosen BeeMinder charges. Use when a user commits to a measurable or subjective outcome, asks to be held accountable, wants a due commitment checked, answers whether a proposed miss is fair, or when a scheduled task checks accountability commitments.
---

# Accountability BeeMinder

Keep the workflow generic. Domain-specific tasks supply their own evidence source and verification rule; this skill owns commitment intake, the JSON ledger, fairness confirmation, and charging.

Use `scripts/accountability.py` for every ledger transition. Its default ledger is `~/.codex/accountability-beeminder.json`, a standard JSON file.

## Create a commitment

1. Gather, one question at a time when missing:
   - exact outcome;
   - timezone-aware due date and time;
   - charge amount in USD (minimum $1);
   - objective evidence source and pass rule, or subjective evidence the model should assess.
2. Restate the binding terms and ask for explicit confirmation.
3. After confirmation, run:

```bash
python3 scripts/accountability.py add \
  --goal "<outcome>" \
  --due "<ISO-8601 with offset>" \
  --amount "<USD>" \
  --verifier-type objective \
  --verification "<source and exact pass rule>"
```

Use `--verifier-type subjective` when machine evidence cannot decide completion. Never store credentials in the goal, rule, evidence, or ledger.

4. After `add` returns the commitment ID, create exactly one active, one-shot Codex heartbeat with `automation_update` for five minutes after its timezone-aware deadline. Name it with the commitment ID. Its prompt must tell the future task to:
   - run `accountability.py due`, then inspect only that commitment;
   - collect evidence using its original verification rule;
   - record `complete` or `miss` as supported by that evidence;
   - on a miss, show the evidence and ask the fairness question; and
   - never run `charge.py` or manufacture fairness confirmation.

If scheduling fails, report that the commitment was recorded without a follow-up; do not imply that a check exists.

## Check due commitments

1. Run `python3 scripts/accountability.py due`.
2. Collect the evidence named by each commitment without changing its rule after the deadline.
3. For a completed commitment, run:

```bash
python3 scripts/accountability.py complete --id <id> --evidence "<concise evidence>"
```

4. When evidence supports a miss, run:

```bash
python3 scripts/accountability.py miss --id <id> --evidence "<concise evidence>"
```

5. Show the evidence and ask exactly one decision: “Is that fair? If yes, I will charge $X.”

Treat unavailable or ambiguous evidence as unknown: leave the commitment pending and report the limitation. Never infer consent from silence.

## Resolve the fairness decision

- If the user says the miss is fair, run `python3 scripts/charge.py --id <id> --fair-confirmed`. This creates the configured charge using `BEEMINDER_AUTH_TOKEN` and `BEEMINDER_USERNAME`.
- If the user says it is not fair, record their reason with `python3 scripts/accountability.py dispute --id <id> --reason "<reason>"` and do not charge.
- Use `--dry-run` with `charge.py` to validate credentials and the request without changing the ledger or charging.

Charging is two-phase: the helper records `charging` before calling BeeMinder, then records `charged` with the returned charge ID. A commitment left in `charging` requires manual reconciliation; never retry it automatically. This favors a missed charge over a duplicate charge.

## Hard rules

- Require explicit binding confirmation before `add` and explicit fairness confirmation before a real `charge`.
- Charge at most once per commitment ID.
- Use only `BEEMINDER_AUTH_TOKEN` for the secret and never print it.
- Preserve the original commitment, deadline, amount, and verification rule after creation.
- Scheduled checks may gather evidence and request fairness confirmation; they may not manufacture that confirmation.
- Scheduled checks may run `accountability.py`; reserve `charge.py` for an interactive turn after confirmation.
