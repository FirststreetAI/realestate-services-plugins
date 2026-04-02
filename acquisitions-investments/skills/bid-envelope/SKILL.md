---
description: Recommend bid range with key pricing sensitivities
argument-hint: "[property name or address]"
---

# Bid Envelope

Recommend a bid range (low / target / walk-away) with pricing sensitivities across exit cap rate, rent growth, vacancy, and capex scenarios.

## Skills Invoked

- `bid-strategy` -- bid range methodology, competitive positioning
- `underwriting-standards` (core) -- pro forma for each scenario
- `scenario-stress-testing` -- sensitivity framework

## Reads from Manifest

- `underwriting/proforma.xlsx` and `underwriting/assumptions.json` (from `/underwrite-asset`)

## Writes to Manifest

- **Directory**: `pricing/`
- **Files**: `bid-range.xlsx`, `sensitivity.csv`
- **Key metrics**: `bid_low`, `bid_target`, `bid_walk`, `target_irr`, `target_cap`

## Workflow

1. Load base-case underwriting from manifest (or build if not available)
2. Define bid-relevant scenarios: vary exit cap (+/- 25-50bp), rent growth (+/- 100bp), vacancy (+/- 200bp), capex (+/- 20%)
3. Run each scenario through `underwriting-standards` to get IRR / multiple
4. Invoke `bid-strategy` to frame competitive positioning and recommend range
5. Produce sensitivity matrix and bid recommendation
6. All return calculations via validated Python functions

## QA Checklist

- [ ] Base case IRR matches underwriting output
- [ ] Bid walk-away corresponds to minimum acceptable return threshold
- [ ] Sensitivity range is realistic (not extreme swings)
- [ ] Competitive context considered (is this a widely marketed deal?)
