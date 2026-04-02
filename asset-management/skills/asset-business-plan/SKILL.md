---
description: 12-24 month operating and capital plan for an individual asset
argument-hint: "[property name]"
---

# Asset Business Plan

Produce a 12-24 month business plan for an income-producing property, covering strategic objectives, operating plan, leasing plan, capital plan, milestones, and risk factors.

## Skills Invoked

- `business-plan-governance` -- plan structure, variance-to-plan reporting format, milestone tracking

## Required Inputs

- Property name and basic details (type, location, size, year built)
- Current operating performance (rent roll, T-12 or YTD actuals)
- Strategic context (core hold, value-add execution, stabilization, disposition prep)

## Optional Inputs

- Original underwriting or acquisition business plan
- Market data (submarket rents, vacancy, supply pipeline)
- Capital project list and estimates
- Leasing pipeline
- Debt terms and maturity dates

## Reads from Manifest

- `underwriting/proforma.xlsx` -- original UW for variance context
- `underwriting/assumptions.json` -- original assumptions
- `operations/rent-roll.xlsx` -- current rent roll

## Writes to Manifest

- **Directory**: `strategy/`
- **Files**: `business-plan.md`
- **Key metrics**: `plan_noi_year1`, `plan_noi_year2`, `target_occupancy`, `planned_capex`, `key_milestones`

## Workflow

### Step 1: Assess Current Position

Review current operating performance, occupancy, tenant mix, lease rollover schedule, capital condition, and market positioning. Compare to original underwriting if available.

### Step 2: Define Strategic Objectives

Based on asset strategy (core/value-add/opportunistic) and current position, define 2-4 clear objectives for the plan period. Examples: stabilize occupancy above 93%, execute lobby renovation, achieve 10% NOI growth, prepare for disposition.

### Step 3: Build Operating Plan

Invoke `business-plan-governance` to structure the operating plan:
- Revenue plan: rent growth, lease-up, concession burn-off
- Expense plan: controllable expense targets, efficiency initiatives
- NOI targets by quarter

### Step 4: Build Leasing Plan

Define leasing strategy: retention targets, new lease velocity, concession policy, target tenant profile. Map upcoming expirations and assign disposition (renew, release, downtime assumption).

### Step 5: Build Capital Plan

List planned capital projects with timing, cost estimates, NOI impact, and priority. Reference `capex-prioritization` methodology for scoring.

### Step 6: Define Milestones and Risks

Set measurable milestones with target dates. Identify top risks to plan execution and mitigants.

### Step 7: Output

Generate `business-plan.md` with sections:
1. Property Overview and Current Position
2. Strategic Objectives
3. Operating Plan (revenue, expense, NOI targets)
4. Leasing Plan (rollover, retention, new leasing)
5. Capital Plan (projects, timing, budget)
6. Milestones and Timeline
7. Risk Factors and Mitigants

Write to strategy directory and update manifest.

## QA Checklist

- [ ] Strategic objectives are specific and measurable
- [ ] NOI targets tie to revenue and expense plans
- [ ] Leasing plan accounts for all expirations in the plan period
- [ ] Capital plan includes cost estimates and timing
- [ ] Milestones have specific target dates
- [ ] Risks are specific to this asset, not generic
- [ ] Plan is internally consistent (e.g., occupancy targets align with leasing assumptions)

## Escalation Notes

- If current operating data is unavailable, cannot produce a credible plan -- ask user for data
- If strategy is unclear, present 2-3 strategic options with trade-offs and ask user to select
- This is an operating plan, not a financial model -- for detailed pro forma projections, use `/reforecast`
