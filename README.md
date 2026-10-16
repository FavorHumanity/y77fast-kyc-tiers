# y77fast-kyc-tiers

First Python project for Favor Figota Taueva / Y77FAST Software Foundation.

Classifies a proposed transfer into KYC Tier 0, 1, or 2 using the limits in `Y77FAST_Tiered_KYC_Plan` (13 Oct 2026). Internal caps marked `†` are Y77FAST proposals, not Samoa law.

## Run

```bash
python3 kyc_tiers.py
python3 kyc_tiers.py --csv examples.csv
```

## Law vs proposal (GAV)

| Rule | Source |
|------|--------|
| Large cash ≥ SAT 20,000 | MLPA 2007 s.2, s.23A(1) — cash only |
| Stop if no ID | MLPA 2007 s.17 |
| Originator information | MLP Regulations 2009 reg 16(2) |
| Tier 0/1/2 transfer and monthly caps | Y77FAST proposed internal limits (†) |

Not production software. No claim of ML or banking certification.
