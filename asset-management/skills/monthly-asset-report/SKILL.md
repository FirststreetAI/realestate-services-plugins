---
description: Monthly asset report covering leasing, collections, NOI, occupancy, and capex
argument-hint: "[property name or period]"
---

# Monthly Asset Report

Produce a monthly asset management report for an income-producing property, covering leasing activity, collections, NOI performance, occupancy, and capital expenditures.

## Skills Invoked

- `same-store-noi` -- NOI analysis, occupancy bridge, revenue/expense decomposition
- `leasing-spread-analysis` -- lease spreads, rollover waterfall, retention economics

## Required Inputs

- Property name and reporting period (month/year)
- Actual operating results for the period (P&L or GL extract)
- Rent roll as of reporting date

## Optional Inputs

- Budget for comparison
- Prior year actuals for comparison
- Leasing pipeline / activity log
- Capital project status updates

## Reads from Manifest

- `underwriting/assumptions.json` -- original underwriting assumptions for variance context
- `underwriting/proforma.xlsx` -- budget/UW pro forma
- `operations/rent-roll.xlsx` -- prior period rent roll for delta analysis
- `operations/collections.xlsx` -- collections detail

## Writes to Manifest

- **Directory**: `reporting/`
- **Files**: `asset-report-YYYY-MM.md`
- **Key metrics**: `noi_actual`, `noi_budget`, `noi_variance_pct`, `occupancy_physical`, `occupancy_economic`, `collections_rate`, `leasing_activity_sf`

## Workflow

### Step 1: Gather Period Data

Collect actual P&L, rent roll, leasing activity, and capital project updates for the reporting period. Check manifest for prior-period data to enable trend analysis.

### Step 2: Analyze NOI Performance

Invoke `same-store-noi` to decompose revenue and expenses, compute NOI vs. budget and prior year, and build the occupancy bridge (beginning occupancy -> lease-up -> move-outs -> ending occupancy).

### Step 3: Analyze Leasing Activity

Invoke `leasing-spread-analysis` to evaluate new leases and renewals executed during the period. Compute cash and GAAP spreads vs. prior rents, and summarize upcoming rollover exposure.

### Step 4: Collections Summary

Summarize collections rate, aged receivables, and any credit watch tenants. Flag tenants >60 days past due.

### Step 5: Capital Expenditure Update

Summarize capex spend vs. budget, project status (on-track / delayed / over-budget), and remaining reserve balance.

### Step 6: Produce Report

Generate `asset-report-YYYY-MM.md` with the following sections:
1. Executive Summary (3-5 bullet points: NOI, occupancy, leasing, collections, capex)
2. Financial Performance (NOI vs. budget, variance drivers)
3. Occupancy Bridge (beginning -> changes -> ending)
4. Leasing Update (activity, spreads, pipeline, expirations)
5. Collections (rate, aged AR, watchlist tenants)
6. Capital / Construction (spend, status, reserves)
7. Action Items

Write to deal context and update manifest.

## QA Checklist

- [ ] Reporting period clearly stated
- [ ] NOI variance drivers identified (not just the variance amount)
- [ ] Occupancy bridge ties (beginning +/- changes = ending)
- [ ] Leasing spreads computed on both cash and GAAP basis
- [ ] Collections rate calculated and aged AR summarized
- [ ] Capex spend reconciles to budget
- [ ] All financial figures sourced from actuals, not estimated

## Escalation Notes

- If actual P&L is unavailable, cannot produce this report -- ask user for data
- If budget is unavailable, report actuals vs. prior year only and note the gap
- If leasing activity data is missing, include the section header with "[NO ACTIVITY THIS PERIOD]" or "[DATA NOT PROVIDED]"
