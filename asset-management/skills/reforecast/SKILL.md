---
description: Update full-year outlook with YTD actuals, pipeline changes, and market conditions
argument-hint: "[property name or fund name]"
---

# Reforecast

Update the full-year financial forecast by blending YTD actuals with revised forward projections, incorporating pipeline changes, market shifts, and operational developments.

## Skills Invoked

- `underwriting-standards` (core, projection mode) -- pro forma construction for remaining months

## Required Inputs

- YTD actual operating results (P&L through latest month)
- Original budget or underwriting pro forma
- Reporting period (as-of month)

## Optional Inputs

- Revised leasing pipeline or rent assumptions
- Updated market data (rent growth, vacancy trends)
- Known capital events (tenant move-outs, renovation completions)
- Debt term changes (refi, rate reset)

## Reads from Manifest

- `underwriting/proforma.xlsx` -- original budget/UW baseline
- `underwriting/assumptions.json` -- original assumptions to compare against

## Writes to Manifest

- **Directory**: `reporting/`
- **Files**: `reforecast.xlsx`
- **Key metrics**: `reforecast_noi`, `original_budget_noi`, `variance_to_budget_pct`, `ytd_actual_noi`, `forward_noi_estimate`

## Workflow

### Step 1: Establish YTD Actuals

Parse YTD actual results. Confirm revenue, expenses, and NOI for completed months.

### Step 2: Identify Changes to Forward Assumptions

Compare original budget assumptions to current reality:
- Occupancy: known move-outs, signed leases, pipeline
- Rents: achieved rents vs. budgeted market rents
- Expenses: YTD run-rate vs. budget, known one-time items
- Capital: project timing shifts, cost changes

### Step 3: Build Forward Projection

Invoke `underwriting-standards` in projection mode to build remaining-month projections using revised assumptions. Blend YTD actuals + forward projection = full-year reforecast.

**CRITICAL**: All NOI and cash flow calculations MUST use validated Python functions. Do NOT estimate forward NOI by reasoning through the math.

### Step 4: Variance Analysis

Compare reforecast to original budget line by line. Identify and explain material variances. Classify as timing (will self-correct), structural (permanent change), or one-time.

### Step 5: Output

Generate `reforecast.xlsx` with tabs:
1. YTD Actuals (monthly detail)
2. Forward Projection (monthly detail, revised assumptions)
3. Full-Year Reforecast (combined)
4. Variance to Budget (line-by-line with explanations)
5. Assumptions (original vs. revised, with rationale for changes)

Write to reporting directory and update manifest.

## QA Checklist

- [ ] YTD actuals tie to source P&L
- [ ] Forward months use revised (not original) assumptions
- [ ] Known events (move-outs, lease-up, capex) reflected in timing
- [ ] Reforecast NOI = YTD actual NOI + forward projected NOI
- [ ] Variance explanations cover all material line items
- [ ] Assumption changes documented with rationale
- [ ] Calculations performed by validated code, not LLM reasoning

## Escalation Notes

- If YTD actuals are unavailable, cannot produce a reforecast -- ask user for data
- If original budget is unavailable, produce a forward projection without variance analysis and note the gap
- If as-of date is January or February, flag that limited YTD data makes the reforecast heavily assumption-driven
