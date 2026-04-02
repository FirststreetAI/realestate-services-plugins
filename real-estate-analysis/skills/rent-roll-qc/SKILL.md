---
description: Normalize and QA a rent roll for rollover, tenant exposure, and mark-to-market
argument-hint: "[property name or address]"
---

# Rent Roll QC

Normalize and quality-check a rent roll: rollover schedule, downtime risk, top-tenant exposure, mark-to-market opportunity, and WALT.

## Skills Invoked

- `rent-roll-normalization` -- cleanup, standardization, all analytical outputs

## Required Inputs

- Rent roll (Excel or PDF)

## Optional Inputs

- Market rent assumptions (for mark-to-market analysis)
- Property type (office, industrial, retail, multifamily) -- affects normalization rules

## Reads from Manifest

None -- typically run standalone or as first step.

## Writes to Manifest

- **Directory**: `rent-roll/`
- **Files**: `rent-roll-analysis.xlsx`, `rent-roll-summary.md`
- **Key metrics**: `total_sf`, `occupied_sf`, `occupancy_pct`, `avg_in_place_rent`, `walt_years`, `largest_tenant_pct`

## Workflow

### Step 1: Parse and Normalize

Invoke `rent-roll-normalization`. The skill standardizes column names, date formats, rent units (annual vs. monthly vs. per-SF), and flags data quality issues.

### Step 2: Rollover Schedule

Build month-by-month and year-by-year lease expiration schedule. Flag concentrated rollover years.

### Step 3: Tenant Exposure

Identify top-10 tenants by rent and SF. Calculate concentration metrics (top tenant %, top 5 %, HHI).

### Step 4: Mark-to-Market

If market rents are provided, compare in-place rents to market for each tenant. Quantify upside (below-market) and risk (above-market).

### Step 5: WALT

Calculate weighted average lease term (by rent and by SF).

### Step 6: Output

Generate analysis Excel and summary markdown. Write to deal context and update manifest.

## QA Checklist

- [ ] All leases have start and end dates
- [ ] Total SF ties to building size (within 2%)
- [ ] No duplicate tenant entries
- [ ] Rent units are consistent (all converted to annual per-SF or monthly per-unit)
- [ ] Vacant spaces accounted for

## Escalation Notes

- If rent roll is PDF, extraction may be imperfect -- ask user to verify key figures
- If >10% of rows have missing dates, flag and ask user before proceeding
