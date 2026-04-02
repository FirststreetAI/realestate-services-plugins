---
description: Same-store NOI analysis, occupancy bridge, and revenue/expense decomposition
---

# Same-Store NOI

The canonical skill for analyzing property-level NOI performance on a same-store basis. Any command that needs NOI trend analysis, occupancy bridges, or revenue/expense decomposition MUST invoke this skill.

## Trigger Conditions

Activated when any command needs:
- Same-store NOI comparison (period over period)
- Occupancy bridge (beginning -> changes -> ending)
- Revenue decomposition (base rent, reimbursements, other income)
- Expense decomposition (controllable vs. uncontrollable)
- NOI variance analysis vs. budget or prior year

## Business Context

Same-store NOI growth is the primary measure of organic operating performance in real estate. By comparing a consistent pool of assets across periods, it strips out the noise of acquisitions, dispositions, and development completions to reveal true operational trends. This metric is reported by REITs, open-end funds, and institutional managers as a key performance indicator.

## Same-Store Criteria

A property qualifies as same-store when it meets ALL of the following:
1. **Owned in both comparison periods** (beginning and end)
2. **Not in active development** during either period
3. **Not in initial lease-up** (typically: must have reached stabilized occupancy, usually >80%, prior to the beginning of the comparison period)
4. **Not undergoing major renovation** that materially disrupts operations

Properties failing these criteria are classified as "non-same-store" and reported separately.

## Workflow

### Revenue Decomposition
1. Break total revenue into: base rent, expense reimbursements (CAM/tax/insurance), percentage rent, parking, other income
2. Compare each component period-over-period
3. Identify drivers: rate increases, occupancy changes, reimbursement timing, one-time items

### Expense Decomposition
1. Classify expenses as controllable (R&M, utilities, G&A, payroll) vs. uncontrollable (real estate taxes, insurance)
2. Compare each line item period-over-period
3. Calculate expense ratio (OpEx / EGI) and compare to prior period

### NOI Calculation
1. NOI = Effective Gross Income - Operating Expenses
2. Same-store NOI growth = (current NOI - prior NOI) / prior NOI
3. Decompose NOI change into: revenue-driven vs. expense-driven

### Occupancy Bridge
1. Beginning occupancy (prior period end)
2. + New leases / lease-up (SF and count)
3. - Move-outs / expirations (SF and count)
4. +/- Other adjustments (remeasurements, conversions)
5. = Ending occupancy
6. Report both physical (SF-based) and economic (revenue-based) occupancy

## Output Structure

- Same-store NOI summary (current vs. prior, dollar and % change)
- Revenue waterfall (component-level comparison)
- Expense waterfall (component-level comparison)
- Occupancy bridge (beginning -> changes -> ending)
- Key driver narrative (top 3 factors affecting NOI change)

## QA Checks

- Same-store pool consistently defined across periods
- Revenue components sum to total revenue
- Expense components sum to total expenses
- NOI = Revenue - Expenses (arithmetic tie)
- Occupancy bridge ties (beginning +/- changes = ending)
- Physical and economic occupancy both reported
- Non-same-store assets identified and excluded with rationale

## Edge Cases

- **Partial-period ownership**: Exclude from same-store; report separately with annualized run-rate
- **Major lease event**: If a single tenant represents >25% of revenue and vacates, flag as distorting same-store comparison
- **Expense reclass**: If chart of accounts changed between periods, restate prior period to match current classification before comparing
- **Tax reassessment**: Large tax increases are uncontrollable but can dominate NOI variance -- call out separately
