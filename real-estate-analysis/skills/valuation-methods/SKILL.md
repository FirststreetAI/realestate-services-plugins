---
description: Property valuation using income approach (direct cap, DCF), sales comparison, and reconciliation
---

# Valuation Methods

The canonical skill for property valuation. Any command that needs to value a property MUST invoke this skill.

## Trigger Conditions

Activated when any command needs:
- Direct capitalization value (NOI / cap rate)
- DCF valuation (present value of projected cash flows + reversion)
- Sales comparison cross-check (per-SF, per-unit benchmarks)
- Value reconciliation across approaches

## Business Context

Valuation underpins acquisitions (what to bid), hold-sell decisions (current value vs. forward returns), and quarterly portfolio reporting (NAV). This skill ensures consistent methodology across all contexts.

## Source Hierarchy

1. Appraised value (if available -- institutional gold standard)
2. Income approach using verified NOI (from `underwriting-standards`)
3. Sales comps (from `market-analysis`)
4. Broker opinion of value (third-party, use as sanity check)

## Workflow

### Direct Capitalization
1. Obtain stabilized NOI (from underwriting or user)
2. Select cap rate: market-derived (from comps), user-provided, or range
3. Value = NOI / Cap Rate
4. Express as per-SF and per-unit for cross-check

### DCF Valuation
1. Obtain projected cash flows (from `underwriting-standards` pro forma)
2. Select discount rate (user-provided or derived from risk profile)
3. Calculate terminal value: forward NOI / exit cap rate
4. PV of cash flows + PV of terminal value = DCF Value
5. All PV calculations via `scripts/returns.py:calculate_npv()`

### Sales Comparison
1. Gather comparable sales (from `market-analysis` or user)
2. Extract price/SF, price/unit, implied cap rate from each comp
3. Adjust for property differences (age, quality, location, occupancy)
4. Derive indicated value range

### Reconciliation
1. Present all approaches with values
2. Weight based on data quality and reliability
3. Produce reconciled value range (low / target / high)
4. State which approach is most reliable and why

## Output Structure

- Valuation summary with all three approaches
- Cap rate support (source and rationale)
- Per-SF and per-unit cross-checks
- Sensitivity table: value at different cap rates (+/- 50bps)

## QA Checks

- Cap rate is within market range for property type and quality
- DCF discount rate > cap rate (risk premium exists)
- Exit cap rate >= going-in cap rate (unless strong appreciation thesis stated)
- Per-SF/per-unit values are within market range
- All PV/NPV calculations via validated code

## Edge Cases

- **Land valuation**: Income approach doesn't apply. Use comparable sales and residual land value.
- **Value-add / unstabilized**: Use DCF with explicit lease-up assumptions, not direct cap on current NOI.
- **Negative leverage**: Flag when cap rate < borrowing cost.

## Standards References

- NCREIF quarterly valuation methodology
- Appraisal Institute income approach standards
