---
description: Summarize unresolved diligence, approvals, and closing risks
argument-hint: "[property name or address]"
---

# Close Readiness

Aggregate status of all pre-closing workstreams and produce a go/no-go recommendation for closing. Pure orchestration -- no reusable analytical logic.

## Skills Invoked

- Uses `acquisition-risk` diligence templates for checklist structure (no calculation logic)

## Reads from Manifest

- `diligence/punchlist.md` and `diligence/issues.csv` -- DD status
- `underwriting/*` -- financial summary
- `debt/*` -- financing status
- `memo/*` -- IC approval status

## Writes to Manifest

- **Directory**: `closing/`
- **Files**: `close-readiness.md`
- **Key metrics**: `open_critical_items`, `go_nogo`, `target_close_date`

## Workflow

1. Pull current diligence punchlist from manifest
2. Categorize open items by severity: critical (blocks close), important (should resolve), minor (can survive)
3. Check for IC approval status (memo produced and approved?)
4. Check financing status (commitment letter received?)
5. Check title, survey, environmental, insurance
6. Produce go/no-go summary with open item list and risk assessment
7. Recommend: close, delay with conditions, or walk

## QA Checklist

- [ ] All critical DD categories assessed
- [ ] Open items have clear owners and timelines
- [ ] Financing status confirmed
- [ ] IC approval status confirmed
- [ ] Clear recommendation stated
