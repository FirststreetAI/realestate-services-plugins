---
description: Quick go/no-go screen for an acquisition opportunity
argument-hint: "[property name or address]"
---

# Screen Deal

Quick go/no-go screen based on asset profile, market, seller ask, yield, and risk flags against fund criteria.

## Skills Invoked

- `deal-screening` -- go/no-go framework, strategy-specific criteria
- `underwriting-standards` (core, quick mode) -- abbreviated pro forma for screening-level returns

## Required Inputs

- Property name, type, location, size
- Asking price or pricing guidance
- Basic tenancy info (occupancy, major tenants)

## Optional Inputs

- Fund strategy (core / core-plus / value-add / opportunistic)
- Fund-specific criteria (min/max size, target geographies, target returns)
- Rent roll, T-12 (if available at screening stage)

## Reads from Manifest

None -- typically the first command in an acquisition workflow.

## Writes to Manifest

- **Directory**: `screening/`
- **Files**: `screen-summary.md`
- **Key metrics**: `go_nogo`, `going_in_yield`, `estimated_irr`, `risk_flags`

## Workflow

1. Gather basic property info from user or provided documents
2. Invoke `deal-screening` to evaluate against fund criteria
3. Invoke `underwriting-standards` in quick mode for screening-level returns
4. Produce go/no-go recommendation with rationale and key risk flags
5. Write to deal context and update manifest

## QA Checklist

- [ ] Property type matches fund mandate
- [ ] Size is within fund range
- [ ] Geography is within fund target markets
- [ ] Yield meets minimum thresholds
- [ ] Key risks identified (not generic list)
