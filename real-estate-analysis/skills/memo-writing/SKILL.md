---
description: IC memo, asset report, investor letter structure, tone conventions, and section templates
---

# Memo Writing

The canonical skill for narrative document structure and tone. Any command that produces a memo, report, or investor letter MUST invoke this skill for structure and language conventions.

## Trigger Conditions

Activated when any command needs:
- Investment committee memo structure
- Asset management report format
- Investor update letter conventions
- Financing memo structure
- Any formal narrative deliverable

## Business Context

Real estate memos follow established conventions that vary by audience (IC, board, LP, lender) and purpose (acquisition, disposition, hold review, quarterly update). This skill standardizes structure and tone so outputs feel professional and consistent.

## Memo Types and Structures

### Investment Committee Memo (Acquisition)
1. **Executive Summary** (1 page max)
   - Property: name, type, location, size
   - Price / cap rate / key return metrics
   - Strategy: why this deal, what the thesis is
   - Recommendation: proceed / decline / conditional
2. **Property Overview**
   - Physical description, age, condition, improvements
   - Tenancy summary (occupancy, WALT, top tenants)
3. **Market Overview**
   - Submarket fundamentals (reference `/market-snapshot` output)
   - Competitive positioning
4. **Financial Analysis**
   - Pro forma summary (reference `/underwrite-asset` output)
   - Returns: IRR, equity multiple, cash-on-cash
   - Sensitivity to key assumptions
5. **Risk Factors and Mitigants**
   - Specific to this deal (not generic)
   - Each risk paired with a mitigant or monitoring plan
6. **Recommendation**
   - Clear action requested
   - Conditions or open items if applicable

### Monthly Asset Report
1. **Executive Summary** (key metrics, 3-5 bullet points)
2. **Leasing Update** (activity, expirations, pipeline)
3. **Financial Performance** (NOI vs. budget, variance drivers)
4. **Capital / Construction** (if applicable)
5. **Market Update** (brief, only if material changes)
6. **Action Items / Watchlist**

### Investor Update (LP Letter)
1. **Portfolio Performance Summary**
2. **Market Commentary**
3. **Key Transactions** (acquisitions, dispositions)
4. **Outlook**
5. **Appendix**: property-level detail

### Financing Memo
1. **Borrower / Sponsor Overview**
2. **Property Summary**
3. **Market Overview**
4. **Financial Analysis** (NOI, debt coverage)
5. **Loan Request and Terms**
6. **Risk Assessment**

## Tone Guidelines

| Audience | Tone | Specifics |
|----------|------|-----------|
| IC / Internal | Direct, analytical | Lead with recommendation. Risks stated plainly. |
| LP / Board | Professional, balanced | Emphasize performance narrative. Contextualize misses. |
| Lender | Conservative, precise | Focus on coverage and collateral. Understate upside. |
| Broker | Brief, action-oriented | Focus on positioning and market context. |

## Rules

- **Never overstate certainty**: Use "we estimate," "our analysis indicates," not "this property will"
- **Source all numbers**: Every financial figure should reference its source (pro forma, market data, trailing actuals)
- **Lead with the answer**: Executive summary first, supporting detail after
- **Be specific about risks**: "Tenant X (32% of rent) expires in 18 months with no renewal option" not "there is tenant concentration risk"
- **State what's missing**: If a section lacks data, include the header with a note about what's needed

## Standards References

- NCREIF/PREA Reporting Standards for terminology
- NAREIM best practices for asset-level reporting
