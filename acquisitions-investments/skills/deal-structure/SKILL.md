---
description: Compare direct acquisition vs. JV / preferred equity / programmatic structure
argument-hint: "[property name or address]"
---

# Deal Structure

Model and compare acquisition structures: direct purchase, joint venture with promote, preferred equity, and programmatic partnerships.

## Skills Invoked

- `deal-structuring` -- JV structures, promote mechanics, GP/LP alignment

## Reads from Manifest

- `underwriting/proforma.xlsx` -- project cash flows
- `pricing/bid-range.xlsx` -- target price

## Writes to Manifest

- **Directory**: `structure/`
- **Files**: `structure-comparison.xlsx`
- **Key metrics**: `recommended_structure`, `gp_irr`, `lp_irr`, `gp_promote_total`

## Workflow

1. Load project-level cash flows from manifest (or build from inputs)
2. Model structures:
   - **Direct**: 100% equity, no promote split
   - **JV with promote**: GP coinvest (5-20%), LP provides balance, promote tiers above hurdle
   - **Preferred equity**: Senior position with fixed return, residual to common
   - **Programmatic**: Multi-deal commitment with portfolio-level promote
3. For each structure, calculate GP and LP returns using `scripts/returns.py:calculate_waterfall()`
4. Compare: GP IRR, LP IRR, alignment of interests, complexity
5. Recommend structure based on deal characteristics and capital availability

## QA Checklist

- [ ] All waterfall calculations via validated Python functions
- [ ] GP coinvest percentage clearly stated
- [ ] Promote tiers documented with hurdle rates
- [ ] Cash flows sum correctly (GP + LP = total project cash flows)
