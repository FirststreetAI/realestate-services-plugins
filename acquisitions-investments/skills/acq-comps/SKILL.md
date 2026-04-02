---
description: Gather sale and lease comps, adjust for property differences
argument-hint: "[property name or address]"
---

# Acquisition Comps

Gather sale and/or lease comps relevant to an acquisition opportunity. Adjust for property differences and produce a formatted comp set.

## Skills Invoked

- `market-analysis` (core) -- comp selection, adjustment methodology

## Reads from Manifest

- `screening/screen-summary.md` -- property type, location context

## Writes to Manifest

- **Directory**: `comps/`
- **Files**: `sale-comps.csv`, `lease-comps.csv` (if applicable)
- **Key metrics**: `median_cap_rate`, `median_price_psf`, `comp_count`

## Workflow

1. Define comp criteria (property type, size range, market, vintage)
2. If MCP available, query CoStar/Reonomy for transactions
3. If not, ask user for comp data or broker reports
4. Normalize and format into standard comp table
5. Adjust for differences (age, quality, occupancy, location)
6. Derive implied pricing benchmarks

## QA Checklist

- [ ] Comps are same property type as subject
- [ ] Transaction dates are within 24 months (prefer 12)
- [ ] At least 3 comps for meaningful analysis
- [ ] Adjustments are stated and reasonable
