---
description: Capex scoring methodology by urgency, NOI impact, tenant retention value, and deferral risk
---

# Capex Prioritization

The canonical skill for evaluating and ranking capital expenditure projects. Any command that needs to prioritize, score, or schedule capex MUST invoke this skill.

## Trigger Conditions

Activated when any command needs:
- Capital project scoring and ranking
- Multi-year capex scheduling
- Reserve adequacy analysis
- ROI analysis for value-add capital projects

## Business Context

Capital allocation is a zero-sum game: every dollar spent on one project is unavailable for another. This skill provides a consistent, defensible framework for ranking projects so that safety-critical items are never deferred, high-ROI projects are prioritized, and discretionary spending is right-sized relative to available capital.

## Workflow

### Scoring Methodology

Each project is scored on four dimensions (1-5 scale each):

#### Urgency (weight: 35%)
| Score | Criteria |
|-------|----------|
| 5 | Safety hazard or code compliance violation -- immediate action required |
| 4 | Active building system failure affecting operations or tenant comfort |
| 3 | Deferred maintenance with accelerating deterioration |
| 2 | Preventive replacement approaching end of useful life |
| 1 | Cosmetic improvement or amenity enhancement |

#### NOI Impact (weight: 30%)
| Score | Criteria |
|-------|----------|
| 5 | Direct revenue enhancement >5% NOI uplift (e.g., unit renovation with rent premium) |
| 4 | Significant expense reduction with <3 year payback |
| 3 | Moderate revenue or expense impact with 3-5 year payback |
| 2 | Indirect benefit (tenant satisfaction, competitive positioning) |
| 1 | No measurable NOI impact |

#### Tenant Retention Value (weight: 20%)
| Score | Criteria |
|-------|----------|
| 5 | Directly tied to a lease renewal negotiation (tenant requirement) |
| 4 | Addresses known tenant complaint affecting retention |
| 3 | General amenity improvement supporting retention |
| 2 | Indirect tenant benefit |
| 1 | No tenant impact |

#### Risk if Deferred (weight: 15%)
| Score | Criteria |
|-------|----------|
| 5 | Deferral creates liability exposure or insurance risk |
| 4 | Deferral causes cascading damage (water intrusion, structural) |
| 3 | Deferral increases future cost by >25% |
| 2 | Deferral has modest cost escalation |
| 1 | Deferral has minimal consequence |

**Composite Score** = (Urgency x 0.35) + (NOI Impact x 0.30) + (Retention x 0.20) + (Deferral Risk x 0.15)

### Multi-Year Scheduling

1. **Year 1**: All projects scoring >= 4.0 composite, plus all safety/code items regardless of score
2. **Year 2**: Projects scoring 3.0-3.9
3. **Year 3+**: Projects scoring < 3.0 (discretionary, schedule as capital allows)
4. Within each year, sequence by: dependencies first, then highest composite score first
5. Validate that annual spend does not exceed available capital; if it does, defer lowest-priority items

### Reserve Adequacy Check

1. Beginning reserve balance
2. + Annual reserve contributions (typically $0.15-$0.50/SF for commercial, $250-$500/unit for multifamily)
3. - Planned annual capex spend
4. = Ending reserve balance
5. Minimum reserve threshold: 3-6 months of planned annual capex
6. If ending balance falls below threshold, recommend: increase contributions, defer discretionary projects, or fund via capital call

### ROI Analysis (Value-Add Projects)

For projects with NOI impact score >= 3:
1. Estimate incremental NOI (annual revenue increase or expense savings)
2. Simple payback = project cost / annual incremental NOI
3. ROI = incremental NOI / project cost
4. Capitalized value creation = incremental NOI / cap rate

## Output Structure

- Scored project list (all projects with dimension scores and composite rank)
- Multi-year schedule (projects assigned to years with timing)
- Reserve projection (beginning balance through end of plan)
- ROI summary for value-add projects (payback, ROI, value creation)

## QA Checks

- All projects scored on all four dimensions
- Weights sum to 100%
- Safety/code items never deferred to Year 2+ regardless of budget
- Reserve balance never goes negative without flagging
- ROI calculations use realistic rent premiums or expense savings
- Project costs include soft costs (design, permitting, management)
- Multi-year total ties to sum of individual project budgets

## Edge Cases

- **Emergency repairs**: Score 5 on urgency, bypass normal scheduling -- execute immediately
- **Tenant-funded improvements**: Exclude from capital plan if 100% tenant-funded; include if landlord share exists
- **Insurance-covered items**: Net of expected insurance recovery; track gross and net cost
- **ESG / sustainability projects**: Score NOI impact based on measurable savings (energy, water); do not score based on ESG narrative alone
