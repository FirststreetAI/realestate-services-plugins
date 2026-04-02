---
description: Evaluate hold, refinance, recapitalize, and sell options with forward return comparison
argument-hint: "[property name]"
---

# Hold-Sell Analysis

Evaluate strategic options for an asset -- hold, sell, refinance, or recapitalize -- by comparing forward returns under each scenario.

## Skills Invoked

- `hold-sell-framework` -- decision framework, scenario comparison methodology
- `underwriting-standards` (core) -- pro forma projection for hold scenario
- `valuation-methods` (core) -- current value estimate for sell scenario

## Required Inputs

- Property name and basic details
- Current operating results (rent roll and T-12 or YTD actuals)
- Original acquisition basis (price, date, equity invested)

## Optional Inputs

- Current debt terms (balance, rate, maturity)
- Estimated disposition value or broker opinion of value
- Redeployment opportunity yield (for sell proceeds)
- Tax basis and depreciation schedule
- Fund lifecycle constraints (term, extension options)

## Reads from Manifest

- `underwriting/proforma.xlsx` -- original UW pro forma
- `underwriting/assumptions.json` -- original UW assumptions
- `valuation/valuation-summary.md` -- prior valuation if available

## Writes to Manifest

- **Directory**: `strategy/`
- **Files**: `hold-sell.xlsx`, `hold-sell.md`
- **Key metrics**: `hold_forward_irr`, `sell_forward_irr`, `refi_forward_irr`, `recommendation`, `current_value_estimate`

## Workflow

### Step 1: Establish Current Value

Invoke `valuation-methods` to estimate current market value using direct cap and DCF approaches. If user provides a BOV or recent appraisal, use that as primary input.

### Step 2: Build Hold Scenario

Invoke `underwriting-standards` to project forward cash flows for remaining hold period. Calculate forward IRR from current equity basis (current value - debt = implied equity).

### Step 3: Build Sell Scenario

Estimate net sale proceeds: disposition value - transaction costs (brokerage, legal, transfer tax) - loan payoff. Factor in tax implications (depreciation recapture, capital gains) if tax basis provided. Calculate reinvestment yield on net proceeds.

### Step 4: Build Refinance / Recap Scenarios (if applicable)

Model refinance: new loan terms, cash-out proceeds, revised CFAD. Model recapitalization: partner buyout, JV restructuring, preferred equity. Calculate forward returns under each structure.

### Step 5: Compare Scenarios

Invoke `hold-sell-framework` to compare all scenarios on:
- Forward IRR
- Equity multiple on remaining capital
- Risk profile (lease rollover, capex needs, market exposure)
- Fund lifecycle fit (time to exit, distribution needs)
- Replacement risk (can proceeds be redeployed at equal or better return?)

**CRITICAL**: All IRR and return calculations MUST use `scripts/returns.py`. Do NOT compute forward returns by reasoning through the math.

### Step 6: Output

Generate `hold-sell.xlsx` with scenario comparison tabs:
1. Hold Scenario (forward cash flows, IRR)
2. Sell Scenario (net proceeds, redeployment return)
3. Refinance Scenario (revised cash flows, IRR)
4. Scenario Comparison (side-by-side summary)
5. Sensitivity (cap rate, exit timing, redeployment yield)

Generate `hold-sell.md` with narrative recommendation.

Write to strategy directory and update manifest.

## QA Checklist

- [ ] Current value supported by market evidence or stated as assumption
- [ ] Transaction costs realistic for property type and market (typically 2-4%)
- [ ] Tax implications included if tax basis provided
- [ ] Forward IRR calculated from current equity position, not original basis
- [ ] Redeployment yield assumption stated and justified
- [ ] Replacement risk addressed in recommendation
- [ ] All return calculations performed by validated code

## Escalation Notes

- If current value is uncertain, present analysis at multiple value assumptions
- If debt information is unavailable, analyze hold vs. sell on unlevered basis and note the gap
- If tax basis is unavailable, exclude tax analysis and flag as material omission
- This analysis supports a decision but does NOT constitute investment advice
