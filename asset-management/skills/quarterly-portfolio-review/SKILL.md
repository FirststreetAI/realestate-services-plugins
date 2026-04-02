---
description: Portfolio review across assets, sectors, geographies, and watchlist
argument-hint: "[portfolio name or period]"
---

# Quarterly Portfolio Review

Produce a comprehensive portfolio-level review summarizing performance across assets, sectors, and geographies, with watchlist identification and forward outlook.

## Skills Invoked

- `portfolio-review-writing` -- review structure, sector/geographic analysis, watchlist criteria
- `performance-attribution` -- return decomposition by property type, geography, vintage

## Required Inputs

- Portfolio property list with current period operating results
- Reporting period (quarter/year)

## Optional Inputs

- Benchmark data (NPI, ODCE)
- Prior quarter portfolio review for trend comparison
- Market outlook or macro commentary

## Reads from Manifest

None -- this is a portfolio-level command that aggregates across assets.

## Writes to Manifest

- **Directory**: `reporting/`
- **Files**: `portfolio-review.md`
- **Key metrics**: `portfolio_noi`, `portfolio_occupancy`, `same_store_noi_growth`, `watchlist_count`, `total_nav`

## Workflow

### Step 1: Aggregate Portfolio Data

Compile property-level results into portfolio summary. Group by sector (office, industrial, multifamily, retail, etc.) and geography (region, MSA).

### Step 2: Compute Portfolio Metrics

Calculate portfolio-level occupancy, NOI, same-store NOI growth, and NAV. Compare to budget and prior period.

### Step 3: Run Performance Attribution

Invoke `performance-attribution` to decompose returns by property type, geography, and vintage year. Compare to benchmark if data available.

### Step 4: Draft Portfolio Review

Invoke `portfolio-review-writing` to structure the review:
1. Executive Summary
2. Performance Summary (portfolio-level metrics, trends)
3. Sector Analysis (performance by property type)
4. Geographic Analysis (performance by region/MSA)
5. Watchlist (underperformers, high vacancy, rollover concentration, capital needs)
6. Outlook (forward view, key risks, opportunities)

### Step 5: Output

Generate `portfolio-review.md`. Write to reporting directory and update manifest.

## QA Checklist

- [ ] All portfolio properties accounted for in aggregation
- [ ] Same-store pool clearly defined (owned in both periods, excluding development/lease-up)
- [ ] Sector and geographic totals tie to portfolio total
- [ ] Watchlist criteria stated and consistently applied
- [ ] Benchmark comparison uses appropriate index (NPI for core, ODCE for open-end)
- [ ] Attribution totals reconcile to portfolio-level return

## Escalation Notes

- If property-level data is incomplete for some assets, include them with available data and note gaps
- If benchmark data is unavailable, skip benchmark comparison and note the omission
- If portfolio contains fewer than 3 assets, skip sector/geographic diversification analysis
