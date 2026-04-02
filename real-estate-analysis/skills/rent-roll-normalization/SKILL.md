---
description: Rent roll cleanup, standardization, rollover analysis, WALT, and tenant credit flagging
---

# Rent Roll Normalization

The canonical skill for rent roll parsing, standardization, and analysis. Any command that works with a rent roll MUST invoke this skill for normalization before analysis.

## Trigger Conditions

Activated when any command needs:
- Rent roll parsing from Excel or PDF
- Standardized rollover/expiration schedule
- WALT calculation
- Tenant concentration analysis
- Mark-to-market comparison

## Business Context

Rent rolls arrive in dozens of formats -- every owner, broker, and property manager uses different column names, date formats, and rent conventions. This skill normalizes them into a standard schema so downstream analysis is consistent.

## Source Hierarchy

1. Rent roll from executed leases / property management system (primary)
2. Rent roll from offering memorandum (secondary -- may be seller-optimized)
3. User-typed summary (last resort)

## Workflow

### Step 1: Parse and Identify Columns
Map source columns to standard fields:
- `tenant_name` -- tenant / lessee name
- `suite` -- suite or unit number
- `square_feet` or `units` -- leased area
- `lease_start` -- commencement date
- `lease_end` -- expiration date
- `annual_rent` -- annual base rent (convert from monthly/PSF if needed)
- `rent_per_sf` -- calculated if not present (annual_rent / SF)
- `escalation` -- annual escalation rate or schedule
- `options` -- renewal options (term, notice, rate)
- `expense_structure` -- NNN, gross, modified gross

### Step 2: Normalize Units
- Convert all rents to annual and per-SF
- Convert all dates to ISO format
- Flag rows with missing critical fields
- Separate occupied from vacant suites

### Step 3: Rollover Schedule
- Group expirations by year and quarter
- Calculate SF and rent expiring per period
- Flag years with >20% rollover as concentrated

### Step 4: WALT (Weighted Average Lease Term)
- WALT by rent: Σ(remaining_term × annual_rent) / Σ(annual_rent)
- WALT by SF: Σ(remaining_term × SF) / Σ(SF)

### Step 5: Tenant Concentration
- Top tenant by rent and SF (percentage of total)
- Top 5 and top 10 concentration
- HHI (Herfindahl-Hirschman Index) for quantitative concentration

### Step 6: Mark-to-Market (if market rents provided)
- Compare in-place rent/SF to market rent/SF per tenant
- Calculate total portfolio mark-to-market opportunity (positive) or risk (negative)
- Flag tenants significantly above or below market (>15% deviation)

## Output Structure

Standardized rent roll with all normalized fields, plus summary tabs:
- Rollover schedule (by year)
- Tenant concentration table
- Mark-to-market analysis (if market rents available)
- Data quality flags

## QA Checks

- Total occupied SF + vacant SF = total building SF (within 2%)
- Sum of tenant rents = reported gross revenue (within 2%)
- No duplicate tenant/suite combinations
- All leases have both start and end dates
- Rent per SF is reasonable for property type and market

## Edge Cases

- **Month-to-month tenants**: Treat as expiring in current period for rollover purposes
- **Master lease / sublease**: Flag but don't double-count SF
- **Ground lease**: Separate from building leases
- **Multifamily**: Unit-level with unit type, not tenant name. Use unit mix instead.

## Standards References

- NCREIF/PREA asset-level reporting (rent roll data fields)
