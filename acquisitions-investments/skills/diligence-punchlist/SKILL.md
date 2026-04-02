---
description: Generate diligence checklist and open-issues tracker
argument-hint: "[property name or address]"
---

# Diligence Punchlist

Generate a sector-specific due diligence checklist and open-issues tracker with responsibility assignments.

## Skills Invoked

- `acquisition-risk` -- risk taxonomy, DD scoping by property type

## Reads from Manifest

- `screening/screen-summary.md` -- property type, key risk flags

## Writes to Manifest

- **Directory**: `diligence/`
- **Files**: `punchlist.md`, `issues.csv`
- **Key metrics**: `total_items`, `open_items`, `critical_items`

## Workflow

1. Determine property type and transaction type
2. Invoke `acquisition-risk` for sector-specific DD checklist
3. Generate categorized punchlist: legal, financial, physical, environmental, market, tenant, title, insurance, zoning
4. Create open-issues tracker with columns: item, category, status, owner, due date, notes
5. Pre-populate with standard items; let user customize

## QA Checklist

- [ ] All major DD categories covered
- [ ] Property-type-specific items included (e.g., Phase I for any acquisition, rent roll audit for multi-tenant)
- [ ] Environmental / climate risk items included
- [ ] Each item has an assigned responsibility
