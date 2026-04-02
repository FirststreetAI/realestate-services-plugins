---
description: Fund-level return methodology including TWRR, IRR, TVPI/DPI/RVPI, and TGER using validated Python scripts
---

# Fund Return Calculations

The canonical skill for computing fund-level performance metrics. Any command that needs fund returns MUST invoke this skill, which delegates ALL calculations to `scripts/fund_returns.py`.

## Trigger Conditions

Activated when any command needs:
- Time-weighted rate of return (TWRR)
- Internal rate of return (IRR) at the fund level
- Investment multiples (TVPI, DPI, RVPI)
- Total gross expense ratio (TGER)
- Periodic returns (quarterly, annual)

## Business Context

Fund-level returns are the definitive measure of manager performance reported to LPs, boards, and benchmarking organizations. Calculation methodology must follow industry standards (NCREIF/PREA) to ensure comparability. Small errors in return calculation erode trust and can trigger reporting restatements.

## CRITICAL: Computational Trust

**ALL fund return calculations MUST use `scripts/fund_returns.py`.** Do NOT compute TWRR, IRR, multiples, or expense ratios by reasoning through the math in natural language. The Python functions handle:
- Day-count conventions
- Cash flow timing
- Iterative IRR solving
- Geometric chain-linking for TWRR
- Fee netting for gross-to-net conversion

## Workflow

### Time-Weighted Rate of Return (TWRR)

1. Divide measurement period into sub-periods at each external cash flow (contribution or distribution)
2. Calculate holding period return for each sub-period: (EMV - BMV - CF) / BMV
3. Geometrically chain-link sub-period returns: TWRR = [(1+r1)(1+r2)...(1+rn)] - 1
4. Call `scripts/fund_returns.py:calculate_twrr(nav_series, cash_flows)`
5. Report gross (before fees) and net (after fees) TWRR
6. TWRR is the primary periodic return metric (quarterly, annual)

### Internal Rate of Return (IRR)

1. Construct cash flow series: contributions (negative), distributions (positive), ending NAV (positive)
2. Call `scripts/fund_returns.py:calculate_irr(cash_flows, dates)`
3. IRR hierarchy:
   - Since-inception IRR (primary for closed-end funds)
   - Trailing 1-year, 3-year, 5-year, 10-year IRR
4. Report gross and net IRR
5. IRR is the primary since-inception metric, especially for closed-end funds

### Investment Multiples

1. **TVPI** (Total Value to Paid-In) = (Cumulative Distributions + Current NAV) / Cumulative Contributions
2. **DPI** (Distributions to Paid-In) = Cumulative Distributions / Cumulative Contributions
3. **RVPI** (Residual Value to Paid-In) = Current NAV / Cumulative Contributions
4. Validation: **TVPI = DPI + RVPI** (must tie exactly)
5. Call `scripts/fund_returns.py:calculate_multiples(contributions, distributions, nav)`

### Total Gross Expense Ratio (TGER)

1. Numerator: total fund expenses (management fees + fund-level expenses + transaction costs)
2. Denominator: average fund NAV over the period
3. TGER = Total Expenses / Average NAV
4. Call `scripts/fund_returns.py:calculate_tger(expenses, nav_series)`
5. Report components: management fee ratio, other expense ratio, transaction cost ratio

### Gross-to-Net Conversion

1. Gross return: before management fees and fund expenses, after property-level expenses
2. Net return: after all fees and expenses
3. Difference is approximately the TGER (exact only for TWRR, approximate for IRR)
4. Both gross and net MUST always be reported together

### Annualization

- Periods < 1 year: do NOT annualize (report actual period return)
- Periods >= 1 year: annualize using geometric method
- IRR is inherently annualized
- TWRR annualization: (1 + cumulative return)^(365/days) - 1

## Output Structure

- Return summary table (TWRR, IRR, multiples -- gross and net, multiple periods)
- Cash flow detail (contributions, distributions, NAV by period)
- Expense detail (TGER components)
- Period returns (quarterly and annual chain-linked returns)

## QA Checks

- TVPI = DPI + RVPI (exact arithmetic tie)
- Gross return > net return (fees are positive)
- IRR solved by validated code, not estimated
- TWRR sub-periods align with actual cash flow dates
- NAV used for RVPI is current (note as-of date)
- Returns not annualized for periods < 1 year
- Period returns chain-link to since-inception return
- TGER denominator uses time-weighted average NAV

## Edge Cases

- **New fund (< 1 year)**: Report actual returns, do not annualize. IRR may be misleading with J-curve -- note this.
- **Fund in wind-down**: DPI approaches TVPI as assets are sold. RVPI should be small. Flag if RVPI is large relative to TVPI.
- **Recallable distributions**: Treat as distributions for DPI but note recallability in commentary.
- **Multiple closings**: IRR should reflect actual cash flow timing per LP (or use aggregate for fund-level).

## Notes

- This skill assists with return calculation and preparation. Output does NOT guarantee submission-readiness for NCREIF, GIPS, or other reporting standards.
- Final reporting submissions require review by fund accounting and compliance.

## Standards References

- NCREIF/PREA Fund Return Methodology
- NCREIF Fund Index -- Open End Diversified Core Equity (ODCE) methodology
- GIPS (CFA Institute) for performance reporting standards
- ILPA reporting guidelines for private fund multiples
