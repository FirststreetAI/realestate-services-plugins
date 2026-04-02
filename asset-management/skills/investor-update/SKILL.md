---
description: Draft LP, board, or REIT management update letter
argument-hint: "[fund or entity name, period]"
---

# Investor Update

Draft a professional investor update letter for LPs, board members, or REIT management, summarizing portfolio performance, market context, key transactions, and outlook.

## Skills Invoked

- `investor-reporting` -- LP letter conventions, REIT disclosure standards, fund-level attribution format
- `memo-writing` (core) -- narrative structure, tone conventions by audience

## Required Inputs

- Fund or entity name and reporting period
- Target audience (LP, board, REIT management)
- Portfolio performance summary (returns, occupancy, NOI)

## Optional Inputs

- Market commentary or macro outlook
- Key transactions (acquisitions, dispositions, financings)
- Capital activity (calls, distributions, commitments)
- Watchlist or challenged assets to address
- Prior investor letter for consistency of format and tone

## Reads from Manifest

- `reporting/portfolio-review.md` -- portfolio performance detail
- `reporting/asset-report-*.md` -- property-level summaries
- `performance/fund-returns.xlsx` -- fund-level return metrics
- `performance/attribution.xlsx` -- return attribution detail

## Writes to Manifest

- **Directory**: `reporting/`
- **Files**: `investor-update.md`
- **Key metrics**: none (narrative output)

## Workflow

### Step 1: Gather Context

Check manifest for prior outputs: fund returns, portfolio review, attribution, asset reports. The more prior commands have been run, the richer the letter.

### Step 2: Determine Format

Invoke `investor-reporting` to select appropriate format:
- **LP Letter**: Performance summary, market context, key transactions, outlook
- **Board Update**: More detailed, includes strategic discussion and watchlist
- **REIT Management**: Public-entity disclosure conventions, forward-looking statement caveats

### Step 3: Draft Letter

Invoke `memo-writing` for narrative structure and tone calibration:
1. Performance Summary (headline metrics, trend vs. prior period and benchmark)
2. Market Context (brief macro and sector commentary, only material points)
3. Key Transactions (acquisitions, dispositions, financings completed or in progress)
4. Portfolio Highlights (top performers, notable developments)
5. Challenges and Watchlist (honest discussion of underperformers, with action plans)
6. Outlook (forward view, key initiatives, capital deployment plans)
7. Appendix: Property-level detail (if appropriate for audience)

### Step 4: Output

Generate `investor-update.md`. Write to reporting directory and update manifest.

## QA Checklist

- [ ] Performance figures consistent with `fund-returns.xlsx` (if available)
- [ ] Tone appropriate for audience (LP vs. board vs. public)
- [ ] Market commentary is current and relevant, not generic
- [ ] Challenges addressed honestly with action plans, not buried
- [ ] Forward-looking statements appropriately caveated
- [ ] All financial figures sourced from manifest artifacts or stated as provided by user
- [ ] REIT updates include appropriate disclosure language (if applicable)

## Escalation Notes

- If fund return data is unavailable, ask user for headline performance numbers
- If this is the first investor letter (no prior letter for format reference), default to LP letter format
- This produces a DRAFT. Always tell the user it requires human review, compliance review (for REIT entities), and editing before distribution.
