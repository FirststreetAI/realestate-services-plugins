---
description: Pro forma construction, NOI projection, cash flow waterfall, and return calculation for income-producing real estate
---

# Underwriting Standards

The canonical skill for all pro forma and return calculations. Every command that needs NOI projections, cash flow waterfalls, or return metrics MUST invoke this skill rather than reimplementing the logic.

## Trigger Conditions

Activated when any command needs:
- Multi-year NOI projection
- Cash flow waterfall (before or after debt)
- Property-level return calculations (IRR, equity multiple, cash-on-cash)
- Reversion / terminal value calculation

## Business Context

Underwriting is the foundation of every real estate investment decision. This skill standardizes how pro formas are built across all commands, ensuring consistent assumptions, line-item structure, and calculation methodology regardless of whether the user is screening a deal, bidding, or running a hold-sell analysis.

## Source Hierarchy

1. User-provided rent roll and T-12 (primary)
2. Yardi/MRI GL data via MCP (when available)
3. Offering memorandum financials (secondary -- seller's numbers, use with caution)
4. User-stated assumptions (last resort -- clearly label as manual)

## Workflow

### Revenue Projection
1. Start with in-place rent roll (invoke `rent-roll-normalization` if needed)
2. Apply contractual escalations for in-place leases
3. At lease expiry: model rollover with downtime, TI/LC, and re-leasing at market
4. Apply structural vacancy and credit loss assumptions
5. Result: Effective Gross Income (EGI) by year

### Expense Projection
1. Start with trailing actuals (T-12) or budget
2. Grow controllable expenses at stated inflation rate
3. Grow uncontrollable expenses (taxes, insurance) at category-specific rates
4. Apply management fee as % of EGI
5. Result: Total Operating Expenses by year

### NOI and Cash Flow
1. NOI = EGI - Operating Expenses
2. Below-the-line: capital reserves, TI/LC
3. Net Cash Flow = NOI - Capital Items
4. Cash Flow After Debt = NCF - Debt Service (if debt)

### Returns
1. Build equity cash flow series: initial equity (negative), annual CFAD, terminal equity (reversion - loan payoff)
2. Call `scripts/returns.py:calculate_irr()` for IRR
3. Call `scripts/returns.py:calculate_equity_multiple()` for multiple
4. Call `scripts/returns.py:calculate_cash_on_cash()` for annual CoC

### CRITICAL: Computational Trust
**All financial calculations MUST use the validated Python functions in `scripts/`.**
- `scripts/proforma.py` -- pro forma construction, debt service, reversion
- `scripts/returns.py` -- IRR, XIRR, NPV, equity multiple, cash-on-cash, waterfall
- `scripts/debt_sizing.py` -- DSCR/DY/LTV sizing, amortization

Do NOT reason through IRR, amortization, or waterfall math in natural language.

## Output Structure

### Pro Forma Excel (via template)
- Tab 1: Assumptions (all inputs documented)
- Tab 2: Revenue Detail (tenant-by-tenant with rollover)
- Tab 3: Expense Detail (line-by-line with growth)
- Tab 4: Cash Flow Summary (NOI, NCF, CFAD by year)
- Tab 5: Returns Summary (IRR, EM, CoC, cap rates)
- Tab 6: Sources & Assumptions (data provenance, as-of dates)

### Quick Mode (for `/screen-deal`)
When invoked with screening flag, produce abbreviated output:
- Stabilized NOI (year 1)
- Going-in cap rate
- Unlevered IRR (5-year)
- One-paragraph summary
Skip tenant-level detail and rollover modeling.

## QA Checks

- Revenue growth rate is within market norms (flag if >5% annually)
- Expense ratio (OpEx/EGI) is within range for property type
- Cap rate is supportable by market data
- IRR computed by code matches a manual sanity check (e.g., if 10-year hold with 7% cap and 3% growth, IRR should be roughly 10%)
- Vacancy assumption is justified

## Edge Cases

- **Single-tenant NNN**: Expenses passed through; NOI ≈ base rent. Different template needed.
- **Multifamily**: Unit-level rent roll, not SF-based. Concessions and loss-to-lease modeling.
- **Retail with % rent**: Base rent + percentage rent requires sales projections.
- **Development/lease-up**: Forward-looking only, no trailing operations. Use `lease-up-tracking` skill instead.

## Standards References

- NCREIF property data fields (for institutional reporting compatibility)
- NCREIF/PREA Global Definitions Database for metric terminology
