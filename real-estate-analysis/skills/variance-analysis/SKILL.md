---
description: Actuals vs. budget/prior-year/underwriting comparison, driver decomposition, materiality thresholds
---

# Variance Analysis

The canonical skill for comparing actual operating performance against any comparison basis. Any command that needs variance reporting MUST invoke this skill.

## Trigger Conditions

Activated when any command needs:
- Actuals vs. budget comparison
- Actuals vs. prior year comparison
- Actuals vs. underwriting comparison
- NOI bridge / variance decomposition
- Material variance identification and explanation

## Business Context

Variance analysis is the backbone of asset management reporting. Every monthly asset report, quarterly review, and reforecast starts with understanding where actuals diverge from expectations and why.

## Source Hierarchy

1. Yardi/MRI GL data via MCP (when available) -- system of record for actuals
2. User-provided P&L or financial statements
3. Budget from property management system or user
4. Underwriting assumptions from manifest (`underwriting/assumptions.json`)

## Workflow

### Step 1: Align Data
- Map chart of accounts between actuals and comparison basis
- Verify time periods match (same months, same fiscal year)
- Flag any unmapped line items

### Step 2: Calculate Variances
Use `scripts/variance.py:calculate_variance()` for line-item analysis.
Use `scripts/variance.py:noi_variance_bridge()` for NOI-level summary.

### Step 3: Apply Materiality Thresholds
Default thresholds (can be overridden by user or `.claude/*.local.md`):
- **Dollar threshold**: $10,000 or 5% of line item, whichever is greater
- **NOI-level**: 2% of budgeted NOI
- Revenue items: positive variance = favorable
- Expense items: negative variance = favorable

### Step 4: Decompose Drivers
For each material variance:
- **Rate vs. volume**: Did the per-unit cost change, or did usage change?
- **Timing**: Is this a permanent variance or timing difference?
- **Controllable vs. uncontrollable**: Management actions vs. market/regulatory
- **One-time vs. recurring**: Flag non-recurring items

### Step 5: Output
- Variance summary table (all line items with $ and % variance)
- Material variance narrative (top 5 drivers with explanations)
- NOI bridge (budget NOI → actual NOI, showing each driver)
- YTD trend if multiple periods provided

## QA Checks

- Actuals and comparison periods are aligned
- Total revenue and total expense agree with source documents
- NOI variance = revenue variance - expense variance (arithmetic check)
- Material variances have explanations, not just numbers

## Edge Cases

- **Partial year**: Annualize carefully, or compare only matching months
- **Property acquired mid-year**: Pro-rate budget for ownership period
- **Major capital event**: Separate capital from operating variances

## Standards References

- IREM expense categorization for consistent line-item mapping
- BOMA expense classification for office properties
