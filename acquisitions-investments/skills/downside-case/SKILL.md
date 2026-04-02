---
description: Pressure-test rents, downtime, exit cap, capex, and financing terms
argument-hint: "[property name or address]"
---

# Downside Case

Build bear-case scenarios that stress key assumptions and compare downside returns to base case.

## Skills Invoked

- `scenario-stress-testing` -- downside construction methodology
- `underwriting-standards` (core) -- re-run pro forma with stressed assumptions

## Reads from Manifest

- `underwriting/proforma.xlsx` and `underwriting/assumptions.json`

## Writes to Manifest

- **Directory**: `stress/`
- **Files**: `downside-scenarios.xlsx`
- **Key metrics**: `downside_irr`, `downside_multiple`, `breakeven_scenario`

## Workflow

1. Load base-case assumptions from manifest
2. Invoke `scenario-stress-testing` to define stress scenarios:
   - Rent: -5%, -10%, -15% vs. base
   - Vacancy: +200bp, +500bp, +1000bp
   - Exit cap: +25bp, +50bp, +100bp
   - Capex: +20%, +50%
   - Interest rate: +100bp, +200bp
3. Run each scenario through `underwriting-standards` via Python scripts
4. Identify breakeven scenario (where IRR = 0 or equity multiple = 1.0x)
5. Produce comparison table: base vs. downside returns

## QA Checklist

- [ ] All calculations via validated Python functions
- [ ] Stress ranges are realistic (not extreme)
- [ ] Breakeven point identified
- [ ] Base case numbers match underwriting output exactly
