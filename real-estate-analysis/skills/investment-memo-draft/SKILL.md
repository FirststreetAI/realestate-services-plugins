---
description: Draft a neutral investment memo using standard real estate template
argument-hint: "[property name or address]"
---

# Investment Memo Draft

Produce a neutral draft investment memo adaptable for acquisitions, dispositions, or hold reviews.

## Skills Invoked

- `memo-writing` -- memo structure, tone conventions, section templates

## Required Inputs

- Property name and basic details (type, location, size)
- Purpose of memo (acquisition, disposition, hold review, or general)

## Optional Inputs

- Prior analysis outputs (underwriting, valuation, market snapshot)
- Key risks and mitigants to highlight
- Target audience (IC, board, LP, internal)

## Reads from Manifest

- `underwriting/summary.md` -- financial summary
- `underwriting/assumptions.json` -- key assumptions
- `valuation/valuation-summary.md` -- valuation conclusion
- `market/submarket-snapshot.md` -- market context
- `pricing/bid-range.xlsx` -- bid recommendation (if acquisition)

## Writes to Manifest

- **Directory**: `memo/`
- **Files**: `draft-memo.md`
- **Key metrics**: none (narrative output)

## Workflow

### Step 1: Gather Context

Check manifest for prior outputs. The more prior commands have been run, the richer the memo. If no prior outputs exist, gather information directly from user.

### Step 2: Draft Memo

Invoke `memo-writing` skill. The skill provides section structure:

1. Executive Summary
2. Property Overview
3. Market Overview
4. Financial Analysis
5. Risk Factors and Mitigants
6. Recommendation

### Step 3: Populate Sections

Fill each section using data from manifest artifacts and user inputs. Financial exhibits reference the underwriting/valuation outputs rather than duplicating numbers.

### Step 4: Output

Generate structured markdown memo. Write to deal context and update manifest.

## QA Checklist

- [ ] All stated facts sourced (from manifest artifacts or user)
- [ ] Financial figures consistent with underwriting output
- [ ] Risks are specific to this deal, not generic
- [ ] Recommendation is stated or explicitly marked as TBD
- [ ] Tone matches target audience

## Escalation Notes

- If critical sections lack data (e.g., no financial analysis available), include the section header with "[TO BE COMPLETED]" placeholder and note what's needed
- This produces a DRAFT. Always tell the user it requires human review and editing.
