---
description: Rank and schedule capex projects by urgency, NOI impact, risk, and retention value
argument-hint: "[property name]"
---

# Capital Plan

Prioritize and schedule capital expenditure projects for an asset, scoring each by urgency, NOI impact, tenant retention value, and risk if deferred.

## Skills Invoked

- `capex-prioritization` -- scoring methodology, multi-year scheduling, reserve adequacy check

## Required Inputs

- Property name and basic details
- List of proposed capital projects with estimated costs
- Current capital reserve balance

## Optional Inputs

- Building condition assessment
- Tenant requests or requirements
- Annual capital budget or reserve contribution rate
- Prior capital plan for comparison

## Reads from Manifest

- `underwriting/assumptions.json` -- original capex reserves assumption
- `operations/capital-projects.xlsx` -- existing project tracking (if available)

## Writes to Manifest

- **Directory**: `strategy/`
- **Files**: `capital-plan.xlsx`
- **Key metrics**: `total_capex_planned`, `year1_capex`, `reserve_balance`, `reserve_adequacy`, `critical_projects_count`

## Workflow

### Step 1: Catalog Projects

List all proposed capital projects with description, estimated cost, category (safety/code, deferred maintenance, value-add, cosmetic), and requestor.

### Step 2: Score Projects

Invoke `capex-prioritization` to score each project on:
- Urgency (safety/code compliance > deferred maintenance > value-add > cosmetic)
- NOI impact (revenue enhancement vs. expense reduction, payback period)
- Tenant retention value (projects linked to lease renewals or tenant satisfaction)
- Risk if deferred (safety risk, accelerating deterioration, tenant loss)

### Step 3: Prioritize and Schedule

Rank projects by composite score. Schedule across plan period (typically 3-5 years) based on urgency and available capital. Front-load critical items.

### Step 4: Check Reserve Adequacy

Compare planned spend against current reserves and projected contributions. Flag any years where spend exceeds available capital. Recommend reserve contribution adjustments if needed.

### Step 5: Output

Generate `capital-plan.xlsx` with tabs:
1. Project List (all projects with scores, priority rank)
2. Multi-Year Schedule (projects by year, monthly timing for Year 1)
3. Budget Summary (annual spend by category)
4. Reserve Projection (beginning balance, contributions, spend, ending balance by year)
5. ROI Analysis (NOI impact and payback for value-add projects)

Write to strategy directory and update manifest.

## QA Checklist

- [ ] All proposed projects included and scored
- [ ] Scoring criteria applied consistently across projects
- [ ] Critical/safety items scheduled in Year 1
- [ ] Annual spend does not exceed available capital (or gap is flagged)
- [ ] Reserve projection carries through full plan period
- [ ] Value-add projects include expected NOI uplift and payback period
- [ ] Total planned capex reconciles to sum of individual projects

## Escalation Notes

- If project cost estimates are missing, ask user for estimates or note as TBD
- If reserve balance is unknown, ask user -- this is required for adequacy analysis
- If safety/code compliance projects are identified, flag as non-deferrable regardless of budget
