---
description: Draft acquisition investment committee memo
argument-hint: "[property name or address]"
---

# IC Memo

Draft an acquisition investment committee memo with executive summary, market overview, financial analysis, risk factors, and recommendation.

## Skills Invoked

- `ic-memo-conventions` -- IC-specific structure and risk format
- `memo-writing` (core) -- narrative structure and tone
- `underwriting-standards` (core) -- financial exhibits

## Reads from Manifest

- `underwriting/*` -- pro forma, assumptions, summary
- `comps/*` -- comp tables
- `market/*` -- submarket snapshot
- `pricing/*` -- bid recommendation and sensitivity
- `stress/*` -- downside scenarios

## Writes to Manifest

- **Directory**: `memo/`
- **Files**: `ic-memo.md`
- **Key metrics**: none (narrative output)

## Workflow

1. Check manifest for all available prior outputs
2. Invoke `ic-memo-conventions` for acquisition-specific structure
3. Invoke `memo-writing` for tone and formatting
4. Populate each section from manifest artifacts
5. Financial exhibits reference underwriting outputs
6. Risks must be deal-specific with paired mitigants
7. State clear recommendation: proceed at [price], decline, or conditional

## QA Checklist

- [ ] Executive summary fits on one page
- [ ] Financial metrics consistent with underwriting
- [ ] At least 5 deal-specific risk factors (not generic)
- [ ] Each risk has a mitigant or monitoring plan
- [ ] Recommendation is clear and actionable
- [ ] Sources referenced for all factual claims
