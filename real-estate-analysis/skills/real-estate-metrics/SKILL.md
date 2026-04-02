---
description: Standard real estate metric definitions -- DSCR, debt yield, LTV, cap rate, breakeven occupancy, yield-on-cost
---

# Real Estate Metrics

Reference skill providing standard definitions for real estate financial metrics. Other skills invoke this when they need metric definitions, acceptable ranges, or interpretation guidance.

## Trigger Conditions

Activated when any skill or command needs:
- Metric definitions for output labeling
- Acceptable ranges for QA checks
- Metric interpretation for memos and reports

## Metric Definitions

### Income Metrics

| Metric | Formula | Typical Range |
|--------|---------|---------------|
| **Cap Rate** | NOI / Property Value | 4-10% depending on type/market |
| **Yield-on-Cost** | Stabilized NOI / Total Development Cost | Target: 100-200bp spread to market cap |
| **Cash-on-Cash** | Annual CFAD / Equity Invested | 5-10% for core, higher for value-add |
| **NOI Margin** | NOI / EGI | 55-75% depending on property type |

### Return Metrics

| Metric | Formula | Notes |
|--------|---------|-------|
| **IRR** | Rate where NPV of cash flows = 0 | Time-weighted; penalizes slow J-curves |
| **Equity Multiple** | Total Distributions / Total Invested | Not time-weighted |
| **TVPI** | (Distributions + NAV) / Paid-In Capital | Fund-level; includes unrealized |
| **DPI** | Distributions / Paid-In Capital | Fund-level; realized only |

### Debt Metrics

| Metric | Formula | Typical Lender Minimum |
|--------|---------|----------------------|
| **DSCR** | NOI / Annual Debt Service | 1.20-1.35x |
| **Debt Yield** | NOI / Loan Amount | 7-10% |
| **LTV** | Loan Amount / Property Value | Max 60-75% |
| **Breakeven Occupancy** | (OpEx + Debt Service) / PGI | Target < 85% |

### Portfolio / REIT Metrics

| Metric | Formula | Notes |
|--------|---------|-------|
| **FFO** | Net Income + Depreciation + Amort - Gains on Sales | REIT standard; NAREIT definition |
| **AFFO** | FFO - Recurring CapEx - Straight-Line Rent Adj | More conservative than FFO |
| **NAV** | Sum of asset values - net debt + other adjustments | Per-share for REITs |
| **Same-Store NOI Growth** | YoY NOI change for properties owned in both periods | Excludes acquisitions/dispositions |

## Acceptable Ranges by Property Type

| Metric | Office | Industrial | Multifamily | Retail |
|--------|--------|------------|-------------|--------|
| Cap Rate | 5.5-8.0% | 4.5-6.5% | 4.0-6.0% | 5.5-8.5% |
| NOI Margin | 60-70% | 70-85% | 55-65% | 60-75% |
| Expense Ratio | 30-40% | 15-30% | 35-45% | 25-40% |

These ranges are guidelines for QA flagging, not hard constraints. Markets and vintage affect actual ranges significantly.

## Standards References

- NCREIF/PREA Global Definitions Database (GDD) -- authoritative definitions
- NAREIT FFO definition
- NCREIF NPI methodology for return decomposition
