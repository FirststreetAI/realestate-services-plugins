---
description: Asset business plan structure, variance-to-plan reporting, and milestone tracking
---

# Business Plan Governance

The canonical skill for structuring asset-level business plans and tracking execution against plan. Any command that produces or evaluates an asset business plan MUST invoke this skill.

## Trigger Conditions

Activated when any command needs:
- Asset business plan structure and content requirements
- Variance-to-plan reporting format
- Milestone definition and tracking framework
- Plan amendment governance

## Business Context

Every institutional asset has a business plan that defines the strategy, operating targets, capital program, and milestones for a 12-24 month period. The plan is approved by the investment committee or portfolio manager and serves as the accountability framework for asset-level decisions. Variance-to-plan reporting ensures early detection of deviations and drives corrective action.

## Workflow

### Business Plan Structure

#### 1. Property Overview
- Property details: name, type, location, size, year built, class
- Ownership structure: fund, JV, co-investment
- Acquisition date and basis
- Current performance snapshot: occupancy, NOI, value

#### 2. Strategic Objectives
- 2-4 measurable objectives for the plan period
- Aligned to asset strategy: core (income preservation), value-add (NOI growth), opportunistic (repositioning)
- Each objective has: target metric, current baseline, target value, deadline
- Example: "Increase occupancy from 84% to 93% by Q4 2026"

#### 3. Operating Plan
- **Revenue plan**: contractual escalations, renewal assumptions, new leasing velocity, market rent trajectory
- **Expense plan**: controllable expense targets ($/SF by category), efficiency initiatives
- **NOI targets**: quarterly NOI projections with clear revenue and expense drivers

#### 4. Leasing Plan
- Expiration schedule for plan period with disposition strategy per lease (renew, release, restructure)
- Retention targets by tenant category
- New leasing velocity assumptions (SF/quarter, absorption timeline)
- Concession policy: max free rent, TI allowance by deal type

#### 5. Capital Plan
- Project list: description, budget, timing, NOI impact
- Prioritization per `capex-prioritization` methodology
- Funding source: reserves, operating cash flow, capital call

#### 6. Milestones and Timeline
- Quarterly milestones tied to objectives
- Decision points: lease execution deadlines, capital project approvals, refinance timing
- Gantt-style timeline for major workstreams

#### 7. Risk Factors and Mitigants
- Top 3-5 risks specific to this asset and plan
- Each risk paired with: likelihood, impact, mitigant, trigger for escalation

### Variance-to-Plan Reporting Format

Quarterly variance reports compare actual results to plan:

| Metric | Plan | Actual | Variance | Explanation |
|--------|------|--------|----------|-------------|
| NOI | | | $ / % | |
| Occupancy | | | bps | |
| Leasing (SF) | | | SF / % | |
| Capex spend | | | $ / % | |

Variance classification:
- **Timing**: Will self-correct in subsequent quarters (e.g., delayed lease commencement)
- **Structural**: Permanent deviation requiring plan amendment (e.g., market rent decline)
- **One-time**: Non-recurring item (e.g., insurance claim, legal settlement)

### Plan Amendment Triggers

A plan amendment is warranted when:
1. NOI deviates from plan by >10% for two consecutive quarters
2. A top-3 tenant provides notice to vacate (unplanned)
3. Capital needs exceed plan by >20%
4. Market conditions materially change (recession, new competitive supply)
5. Strategy shift (e.g., value-add to disposition)

## Output Structure

- Business plan document (structured markdown)
- Variance report template (for quarterly tracking)
- Milestone tracker (objectives, targets, status)

## QA Checks

- All strategic objectives are specific, measurable, and time-bound
- Operating plan revenue and expense projections internally consistent
- Leasing plan accounts for every expiration in the plan period
- Capital plan has cost estimates and funding sources identified
- Milestones have specific dates, not vague timelines
- Risks are specific to this asset, not boilerplate
- Variance thresholds defined for escalation
