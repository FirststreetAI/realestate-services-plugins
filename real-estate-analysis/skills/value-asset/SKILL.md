---
description: Property valuation using cap rate, DCF, and market comp framing
argument-hint: "[property name or address]"
---

# Value Asset

Produce a property valuation with supportable range using multiple approaches.

## Skills Invoked

- `valuation-methods` -- income approach (direct cap, DCF), sales comparison, reconciliation
- `market-analysis` -- market comp context, cap rate benchmarks

## Required Inputs

- Stabilized NOI OR enough data to derive one (rent roll + T-12, or stated assumptions)

## Optional Inputs

- Cap rate assumption or range
- Discount rate / target return
- Exit cap rate
- Hold period
- Comparable sales data

## Reads from Manifest

- `underwriting/proforma.xlsx` -- stabilized NOI, cash flows (if `/underwrite-asset` was run)
- `underwriting/assumptions.json` -- hold period, growth rates

## Writes to Manifest

- **Directory**: `valuation/`
- **Files**: `valuation.xlsx`, `valuation-summary.md`
- **Key metrics**: `direct_cap_value`, `dcf_value`, `reconciled_value`, `value_per_sf`, `value_per_unit`, `implied_cap_rate`

## Workflow

### Step 1: Establish NOI

Check manifest for prior underwriting output. If available, use stabilized NOI from pro forma. If not, ask user for NOI or inputs to derive it.

### Step 2: Direct Capitalization

Invoke `valuation-methods` for direct cap approach. Requires NOI and cap rate. If no cap rate provided, invoke `market-analysis` to suggest a supportable range based on property type, location, and quality.

### Step 3: DCF Valuation

Invoke `valuation-methods` for DCF approach. Requires projected cash flows, discount rate, exit cap, and hold period. Calculations performed by validated Python functions.

### Step 4: Sales Comparison Cross-Check

If comp data is available (from manifest or user), derive implied value per SF/unit from comps and compare to income approach results.

### Step 5: Reconcile

Present all approaches, weight them based on data quality, and produce a reconciled value range.

### Step 6: Output

Fill `valuation-methods/assets/valuation-template.xlsx` with results. Write to deal context directory and update manifest.

## QA Checklist

- [ ] Cap rate sourced or explicitly stated as assumption
- [ ] DCF discount rate justified
- [ ] Exit cap rate relationship to going-in cap rate explained
- [ ] Per-SF/per-unit cross-check performed
- [ ] Value range provided, not single point estimate
- [ ] All calculations via validated code

## Escalation Notes

- If NOI is unavailable from any source, ask user -- do not estimate
- If cap rate data is unavailable, present a range based on property type norms and flag as unverified
