---
description: Decision framework comparing hold, sell, refinance, and recapitalize options using forward returns
---

# Hold-Sell Framework

The canonical skill for evaluating asset-level strategic options. Any command that compares hold, sell, refinance, or recapitalize alternatives MUST invoke this skill.

## Trigger Conditions

Activated when any command needs:
- Hold vs. sell comparison using forward returns
- Refinance or recapitalization scenario modeling
- Asset disposition analysis
- Fund lifecycle exit planning

## Business Context

The hold-sell decision is the most consequential call an asset manager makes. The question is not "has this asset performed well?" but "does holding this asset produce a better forward return than selling and redeploying the proceeds?" This framework ensures all relevant factors are considered: financial returns, tax implications, transaction friction, replacement risk, and fund lifecycle constraints.

## Workflow

### Establish Forward Return Basis
1. Forward returns are measured from TODAY's equity position, not original basis
2. Current equity = estimated market value - outstanding debt
3. This is the "invested capital" for forward return comparison
4. Sunk costs and prior returns are irrelevant to the forward decision

### Hold Scenario
1. Project forward cash flows using current operating trajectory (not original UW)
2. Assume hold for remaining fund life or stated hold period
3. Apply exit assumptions (exit cap rate, exit timing)
4. Calculate forward IRR and equity multiple on current equity
5. Factor in: planned capex, lease rollover risk, debt maturity events

### Sell Scenario
1. Estimate net disposition proceeds:
   - Gross sale price (current market value or BOV)
   - Less: brokerage (1-3%), legal, transfer tax, closing costs
   - Less: loan defeasance or prepayment penalty (if applicable)
   - Less: tax on gain (if tax basis provided)
     - Depreciation recapture (25% federal rate)
     - Capital gains on remaining gain
   - = Net proceeds to equity
2. Calculate redeployment return: net proceeds invested at assumed reinvestment yield
3. Forward IRR = redeployment yield (adjusted for deployment timing lag)

### Refinance Scenario
1. Model new loan: proceeds, rate, term, amortization
2. Cash-out amount = new loan - existing loan payoff
3. Revised equity = property value - new loan
4. Project revised CFAD with new debt service
5. Calculate forward IRR on revised (reduced) equity base

### Recapitalization Scenario
1. Model capital event: partner buyout, JV restructuring, preferred equity
2. Define revised capital structure and return splits
3. Project cash flows to sponsor/GP under new structure
4. Calculate forward IRR to each capital position

### Scenario Comparison
Compare all scenarios on:
1. **Forward IRR** (primary metric)
2. **Equity multiple** on remaining/redeployed capital
3. **Risk-adjusted return**: adjust for execution risk, market risk, lease risk
4. **Fund lifecycle fit**: time to liquidity, distribution needs, fund term
5. **Replacement risk**: probability of deploying sale proceeds at assumed yield
6. **Tax efficiency**: after-tax vs. pre-tax proceeds comparison

### Decision Matrix

| Factor | Hold | Sell | Refinance | Recap |
|--------|------|------|-----------|-------|
| Forward IRR | | | | |
| Risk profile | | | | |
| Liquidity timing | | | | |
| Tax impact | | | | |
| Fund lifecycle fit | | | | |

## Output Structure

- Scenario summary table (side-by-side comparison)
- Cash flow detail for each scenario
- Sensitivity analysis (exit cap rate, hold period, redeployment yield)
- Narrative recommendation with supporting rationale

## QA Checks

- Forward IRR calculated from current equity, not original investment
- Transaction costs realistic and itemized
- Tax analysis included if basis data provided (or omission noted)
- Redeployment yield assumption justified (not aspirational)
- Replacement risk honestly assessed
- Sensitivity analysis covers reasonable range of outcomes
- All IRR calculations via validated code (`scripts/returns.py`)

## Edge Cases

- **Negative equity**: If property is underwater, sell scenario may require capital call -- flag this prominently
- **Loan lockout**: If debt has prepayment prohibition, sell scenario must account for timing
- **1031 exchange**: If tax-deferred exchange is possible, model separately as it changes the sell economics
- **GP/LP conflicts**: In fund structures, hold-sell decision may differ from GP vs. LP perspective -- note both

## Standards References

- NCREIF/PREA methodology for return measurement
- Institutional hold-sell frameworks (Pension Real Estate Association)
