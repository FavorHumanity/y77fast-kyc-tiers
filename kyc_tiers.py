#!/usr/bin/env python3
"""Y77FAST proposed KYC tier checker. First student project — not production."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass

# † = Y77FAST proposed internal limit (not printed in Samoa law)
TIER0_PER_TX = 300  # †
TIER0_PER_MONTH = 1000  # †
TIER1_PER_TX = 2000  # †
TIER1_PER_MONTH = 5000  # †
TIER2_PER_TX = 19999  # †
TIER2_PER_MONTH = 50000  # †
LARGE_CASH_TALA = 20000  # MLPA 2007 s.2 / s.23A(1) — cash only
ORIGINATOR_FIELDS = ("name", "account", "address")  # MLP Regs 2009 reg 16(2)


@dataclass
class Transfer:
    amount: float
    is_cash: bool
    has_id: bool
    month_total: float
    originator: dict[str, str]


def tier_for(amount: float, month_total: float) -> str:
    if amount <= TIER0_PER_TX and month_total + amount <= TIER0_PER_MONTH:
        return "Tier 0"
    if amount <= TIER1_PER_TX and month_total + amount <= TIER1_PER_MONTH:
        return "Tier 1"
    if amount <= TIER2_PER_TX and month_total + amount <= TIER2_PER_MONTH:
        return "Tier 2"
    return "Above Tier 2 († — escalate)"


def check(t: Transfer) -> list[str]:
    notes: list[str] = []
    if not t.has_id:
        notes.append("STOP: no ID (MLPA 2007 s.17)")
        return notes
    notes.append(f"Tier: {tier_for(t.amount, t.month_total)}")
    if t.is_cash and t.amount >= LARGE_CASH_TALA:
        notes.append("REPORT large cash (MLPA 2007 s.23A(1))")
    elif (not t.is_cash) and t.amount >= LARGE_CASH_TALA:
        notes.append("Internal review (†): non-cash ≥ 20,000 — law applies to cash")
    missing = [f for f in ORIGINATOR_FIELDS if not t.originator.get(f)]
    if missing:
        notes.append(f"Originator incomplete (reg 16(2)): {', '.join(missing)}")
    else:
        notes.append("Originator fields present (reg 16(2))")
    return notes


def _self_tests() -> None:
    base = Transfer(100, False, True, 0, {k: "x" for k in ORIGINATOR_FIELDS})
    assert "Tier 0" in check(base)[0]
    no_id = Transfer(100, False, False, 0, {})
    assert check(no_id)[0].startswith("STOP")
    cash = Transfer(20000, True, True, 0, {k: "x" for k in ORIGINATOR_FIELDS})
    assert any("REPORT large cash" in n for n in check(cash))
    print("OK: 3 self-checks passed")


def main() -> None:
    p = argparse.ArgumentParser(description="Y77FAST proposed KYC tier checker")
    p.add_argument("--csv", help="CSV: amount,is_cash,has_id,month_total,name,account,address")
    p.add_argument("--test", action="store_true")
    args = p.parse_args()
    if args.test or not args.csv:
        _self_tests()
        if not args.csv:
            return
    with open(args.csv, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            t = Transfer(
                float(row["amount"]),
                row["is_cash"].strip().lower() in ("1", "true", "yes"),
                row["has_id"].strip().lower() in ("1", "true", "yes"),
                float(row.get("month_total") or 0),
                {k: row.get(k, "") for k in ORIGINATOR_FIELDS},
            )
            print(f"amount={t.amount}:")
            for n in check(t):
                print(f"  - {n}")


if __name__ == "__main__":
    main()
