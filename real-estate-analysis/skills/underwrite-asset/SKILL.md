---
description: Build a base underwriting view from OM, rent roll, T-12, and market data
argument-hint: "[property name or address]"
---

# Underwrite Asset

Build an institutional-grade underwriting package for an income-producing property.

## Skills Invoked

- `underwriting-standards` -- pro forma construction, NOI projection, cash flow waterfall
- `rent-roll-normalization` -- rent roll cleanup, rollover, WALT, mark-to-market
- `valuation-methods` -- cap rate and DCF valuation with supportable range
- `market-analysis` -- submarket context for rent/vacancy assumptions
- `debt-sizing-hierarchy` (capital-markets plugin) -- loan sizing if debt assumptions provided

## Required Inputs

- Rent roll (Excel or PDF) OR stated rent/occupancy assumptions
- Trailing 12-month operating statement (T-12) OR stated expense assumptions

## Optional Inputs

- Offering memorandum (PDF) -- will extract property details and seller assumptions
- Market data -- submarket, property type, class
- Debt terms -- loan amount, rate, term, amortization
- Hold period and exit cap rate assumptions

## Reads from Manifest

None -- this is typically the first command in an acquisition workflow.

## Writes to Manifest

- **Directory**: `underwriting/`
- **Files**: `proforma.xlsx`, `assumptions.json`, `summary.md`
- **Key metrics**: `going_in_cap`, `stabilized_noi`, `unlevered_irr`, `levered_irr`, `price_per_sf`, `price_per_unit`

## Workflow

### Step 1: Gather Property Information

If the user provided an OM, extract: property name, address, type, size (SF/units), year built, seller's asking price. If not, ask the user for these details.

### Step 2: Normalize the Rent Roll

Invoke `rent-roll-normalization` to clean and standardize the rent roll. Output: in-place rents, vacancy, rollover schedule, WALT, top-tenant concentration.

### Step 3: Analyze Trailing Operations

If a T-12 is provided, parse revenue and expense line items. Compare in-place revenue to rent roll. Flag discrepancies.

### Step 4: Build the Pro Forma

Invoke `underwriting-standards` to construct a multi-year pro forma. The skill will call validated Python functions in `scripts/proforma.py` for all calculations. Key outputs: revenue projection, expense projection, NOI, capital reserves, cash flow before/after debt.

**CRITICAL**: Do NOT calculate NOI, IRR, or cash flows by reasoning through the math. Invoke the Python functions.

### Step 5: Size Debt (if applicable)

If debt assumptions are provided, invoke `debt-sizing-hierarchy` to test DSCR, LTV, and debt yield constraints.

### Step 6: Calculate Returns

Invoke `underwriting-standards` which calls `scripts/returns.py` for IRR, equity multiple, and cash-on-cash yield. Do NOT compute these manually.

### Step 7: Value the Asset

Invoke `valuation-methods` to produce a cap rate valuation and DCF valuation. Cross-check against per-SF/per-unit benchmarks.

### Step 8: Produce Output

Generate `proforma.xlsx` using the template in `underwriting-standards/assets/proforma-template.xlsx`. Fill named ranges with computed values. Include "Sources & Assumptions" tab.

Generate `assumptions.json` with all inputs and assumptions used.

Generate `summary.md` with executive summary of the underwriting.

Write all to the deal context directory and update `_manifest.json`.

## QA Checklist

- [ ] Rent roll total ties to T-12 revenue (within 2%)
- [ ] Expense growth assumptions stated and sourced
- [ ] Cap rate supported by market comps or stated as assumption
- [ ] Vacancy assumption justified (physical vs. economic)
- [ ] Capital reserves included
- [ ] IRR and equity multiple computed by validated code, not LLM reasoning
- [ ] Sources & Assumptions tab populated

## Escalation Notes

- If rent roll is missing or incomplete, ask the user before proceeding
- If T-12 is unavailable, proceed with rent roll only but flag in summary
- If market data is unavailable, note the gap and use manual assumptions
- If rent roll and T-12 revenue diverge by >5%, flag and ask user which to rely on
