---
description: Performance attribution by property type, geography, vintage vs benchmark (NPI, ODCE)
argument-hint: "[fund or portfolio name]"
---

# Attribution

Decompose portfolio or fund returns by property type, geography, and vintage year, with benchmark comparison against NPI or ODCE.

## Skills Invoked

- `performance-attribution` -- return decomposition methodology, benchmark comparison

## Required Inputs

- Property-level returns (income and appreciation components)
- Portfolio composition (property type, geography, vintage for each asset)
- Reporting period

## Optional Inputs

- Benchmark data (NPI, ODCE) by property type and geography
- Fund-level return for reconciliation
- Prior period attribution for trend analysis

## Reads from Manifest

- `performance/fund-returns.xlsx` -- fund-level returns for reconciliation

## Writes to Manifest

- **Directory**: `performance/`
- **Files**: `attribution.xlsx`, `attribution.md`
- **Key metrics**: `total_return`, `income_return`, `appreciation_return`, `top_contributor`, `top_detractor`, `excess_return_vs_benchmark`

## Workflow

### Step 1: Compile Property-Level Returns

Gather income return and appreciation return for each property. Confirm weighting basis (beginning-of-period NAV or average NAV).

### Step 2: Decompose Returns

Invoke `performance-attribution` to decompose total portfolio return into:
- Income return vs. appreciation return
- Attribution by property type (office, industrial, multifamily, retail, etc.)
- Attribution by geography (region, MSA)
- Attribution by vintage year

### Step 3: Benchmark Comparison

Compare portfolio and segment returns to benchmark (NPI for property type, ODCE for fund-level). Calculate allocation effect (over/underweight in outperforming segments) and selection effect (asset-level outperformance within segments).

### Step 4: Identify Contributors and Detractors

Rank properties by contribution to portfolio return. Identify top 3 contributors and top 3 detractors with explanation of drivers.

### Step 5: Output

Generate `attribution.xlsx` with tabs:
1. Portfolio Return Summary (total, income, appreciation)
2. Property Type Attribution (return and weight by sector)
3. Geographic Attribution (return and weight by region)
4. Vintage Year Attribution
5. Benchmark Comparison (allocation and selection effects)
6. Property-Level Detail (individual asset returns, ranked)

Generate `attribution.md` with narrative summary of attribution findings.

Write to performance directory and update manifest.

## QA Checklist

- [ ] Property-level returns weighted correctly to portfolio total
- [ ] Income + appreciation = total return for each property and portfolio
- [ ] Attribution effects sum to total excess return vs. benchmark
- [ ] Property type and geography categories are mutually exclusive and exhaustive
- [ ] Top contributors/detractors identified with specific drivers
- [ ] Weighting basis (BOQ NAV, EOQ NAV, or average) stated consistently

## Escalation Notes

- If property-level return data is incomplete, note which assets are excluded and the coverage ratio
- If benchmark data is unavailable, produce attribution without benchmark comparison and note the omission
- For portfolios with fewer than 5 assets, sector/geographic attribution may not be meaningful -- note this limitation
