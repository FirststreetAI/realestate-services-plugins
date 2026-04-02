---
description: Compare actuals vs. budget, prior year, or underwriting case
argument-hint: "[property name or period]"
---

# Ops Variance

Compare actual operating performance against budget, prior year, or underwriting assumptions. Flag material variances with driver explanations.

## Skills Invoked

- `variance-analysis` -- driver decomposition, materiality thresholds, controllable vs. uncontrollable

## Required Inputs

- Actual operating results (P&L or T-12)
- At least one comparison basis: budget, prior year actuals, or underwriting assumptions

## Optional Inputs

- Property type (affects materiality thresholds)
- Specific line items to focus on

## Reads from Manifest

- `underwriting/assumptions.json` -- underwriting case for variance-to-UW analysis
- `operations/budget-*.xlsx` -- budget if previously created by `/property-budget`

## Writes to Manifest

- **Directory**: `variance/`
- **Files**: `variance-report.xlsx`, `variance-narrative.md`
- **Key metrics**: `revenue_variance_pct`, `expense_variance_pct`, `noi_variance_pct`, `top_variance_driver`

## Workflow

### Step 1: Parse Actuals

Extract revenue and expense line items from provided P&L. Standardize chart of accounts.

### Step 2: Align Comparison Basis

Match line items between actuals and comparison (budget/prior year/UW). Flag any items present in one but not the other.

### Step 3: Compute Variances

Invoke `variance-analysis`. Calculations done via `scripts/variance.py`. Produce dollar and percentage variance for each line item.

### Step 4: Decompose Drivers

For material variances (exceeding thresholds defined in skill), identify whether driven by rate, volume, or timing. Classify as controllable vs. uncontrollable.

### Step 5: Output

Generate variance Excel and narrative markdown explaining top drivers. Write to deal context and update manifest.

## QA Checklist

- [ ] Time periods aligned between actuals and comparison
- [ ] Chart of accounts mapping documented
- [ ] Material variance threshold stated
- [ ] Top 5 variance drivers identified with explanations

## Escalation Notes

- If chart of accounts doesn't map cleanly, present best-effort mapping and ask user to verify
- If actuals period doesn't match comparison period, flag the mismatch
