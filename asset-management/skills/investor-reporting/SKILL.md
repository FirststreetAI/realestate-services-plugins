---
description: LP letter conventions, REIT disclosure standards, and fund-level attribution format for investor communications
---

# Investor Reporting

The canonical skill for investor communication conventions and formatting. Any command that produces LP letters, board updates, or REIT management reports MUST invoke this skill.

## Trigger Conditions

Activated when any command needs:
- LP letter structure and tone conventions
- REIT-style disclosure formatting and caveats
- Fund-level attribution presentation format
- Investor communication compliance considerations

## Business Context

Investor communications are the primary touchpoint between fund managers and their capital partners. LPs, board members, and public-entity stakeholders each expect specific formats, levels of detail, and tone. Consistency across periods builds trust; surprises destroy it. This skill standardizes format and ensures appropriate disclosure practices.

## Workflow

### LP Letter Conventions

#### Structure
1. **Performance Summary** (lead with headline metrics)
   - Fund-level return: TWRR and IRR (gross and net), since inception and period
   - Investment multiples: TVPI, DPI, RVPI
   - Portfolio occupancy and same-store NOI growth
   - Comparison to benchmark (NPI, ODCE)
2. **Market Context** (brief, relevant, not generic)
   - Macro environment (rates, GDP, employment) only if directly relevant
   - Sector-specific trends affecting the portfolio
   - 3-5 sentences maximum; do not repurpose a market research report
3. **Key Transactions**
   - Acquisitions: property, price, cap rate, strategy thesis (2-3 sentences each)
   - Dispositions: property, price, realized return, hold period
   - Financings: property, amount, rate, term, purpose
4. **Portfolio Highlights and Challenges**
   - Top 2-3 positive developments (leasing wins, value creation, outperformance)
   - Honest discussion of challenges (underperformers, market headwinds)
   - Action plans for challenged assets -- never present a problem without a plan
5. **Outlook**
   - Forward view (next 1-2 quarters)
   - Capital deployment pipeline
   - Key risks being monitored
   - Tone: cautiously constructive, never promotional

#### Tone Rules
- Professional, balanced, and transparent
- Contextualize misses: explain what happened and what you're doing about it
- Do not bury bad news in footnotes or appendices
- Use "we" for the management team, not "I"
- Performance is presented net of fees unless explicitly stated as gross

### REIT-Style Disclosure

For public entities (REITs, public non-traded vehicles):
1. Include forward-looking statement safe harbor language
2. Non-GAAP metrics (FFO, AFFO, same-store NOI) must be reconciled to GAAP
3. Clearly label estimates vs. audited figures
4. Risk factor disclosure follows SEC conventions
5. Distribution coverage ratio and payout ratio included

### Fund-Level Attribution Format

Present attribution in a standard table format:

| Segment | Weight | Total Return | Income | Appreciation | Contribution |
|---------|--------|-------------|--------|--------------|-------------|
| Office | % | % | % | % | bps |
| Industrial | % | % | % | % | bps |
| ... | | | | | |
| **Portfolio** | **100%** | **%** | **%** | **%** | **bps** |

- Contribution = Weight x (Segment Return - Portfolio Return)
- Show both absolute return and excess return vs. benchmark

### Frequency and Timing

| Report Type | Frequency | Typical Delivery |
|-------------|-----------|-----------------|
| LP Letter | Quarterly | 45-60 days after quarter-end |
| Capital Account Statement | Quarterly | With LP letter |
| Annual Report | Annual | 90 days after year-end |
| Board Update | Quarterly or monthly | Per governance calendar |
| K-1 / Tax | Annual | March 15 (partnerships) |

## Output Structure

- Formatted investor letter (markdown)
- Attribution tables (if fund returns available)
- Appendix: property-level summary (if appropriate for audience)

## QA Checks

- Performance figures consistent with fund return calculations
- Gross and net returns both stated (or clearly labeled which is presented)
- Benchmark comparison uses appropriate index
- Market commentary is current quarter, not stale
- Challenges addressed with action plans
- Forward-looking statements appropriately caveated
- REIT disclosures include required reconciliations (if applicable)
- Attribution contributions sum to total excess return

## Standards References

- NCREIF/PREA Reporting Standards for terminology and metric definitions
- ILPA Reporting Template for LP communications (private fund context)
- SEC Regulation FD considerations for public entities
- GIPS (CFA Institute) for performance presentation standards
