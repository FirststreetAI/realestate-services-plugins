---
description: Submarket delineation, supply/demand framework, comp selection and adjustment, demographic/employment context
---

# Market Analysis

The canonical skill for assembling market context. Any command that needs market rents, vacancy rates, comp data, or submarket fundamentals MUST invoke this skill.

## Trigger Conditions

Activated when any command needs:
- Submarket definition and boundaries
- Rent and vacancy benchmarks
- Comparable sales or lease transactions
- Construction pipeline data
- Demographic and employment context

## Business Context

Market context is essential for validating underwriting assumptions (rent growth, vacancy, exit cap rate) and providing credible support in memos and IC packages. Without market data, assumptions are unverifiable.

## Source Hierarchy

1. CoStar via MCP (when available) -- most comprehensive commercial data
2. REIS/Moody's Analytics CRE via MCP (when available) -- institutional forecasts
3. User-provided broker reports or market studies
4. Public data (census, BLS, local government)
5. User-stated assumptions (last resort -- clearly label)

## Workflow

### Submarket Definition
1. Identify relevant submarket for the subject property
2. Define boundaries (geographic, competitive set)
3. State submarket name consistently for all downstream commands

### Supply Analysis
- Existing competitive inventory (by class/type)
- Under construction (SF/units, expected delivery)
- Planned/proposed (pipeline visibility)
- Recent deliveries (last 12-24 months)
- Demolitions/conversions reducing supply

### Demand Analysis
- Net absorption (trailing 4-8 quarters)
- Major lease signings in submarket
- Tenant industry composition
- Employment trends in relevant sectors

### Rent and Vacancy
- Current asking rents (by class if applicable)
- Effective rents (net of concessions)
- Vacancy rate (direct and sublease)
- Rent growth trend (3-year, 5-year trailing)
- Concession trends

### Comparable Transactions
- Gather recent sales comps (last 24 months preferred)
- Fields: address, date, price, price/SF, cap rate, property type, size, buyer
- Adjust for differences: age, quality, occupancy, location
- Gather lease comps if relevant: tenant, term, rent/SF, TI, free rent

### Demographics
- Population growth (MSA and submarket)
- Employment growth by sector
- Household income trends
- Major employers and planned corporate relocations

## Output Structure

- Submarket overview (1-2 paragraphs)
- Key metrics table (vacancy, rent, absorption, pipeline)
- Comp table (sales and/or lease, with adjustments)
- Trend charts (rent growth, vacancy, absorption -- describe for markdown)
- Demographic highlights

## QA Checks

- Data sources and as-of dates documented for every metric
- Comp set is reasonable (same property type, similar size, recent vintage)
- Vacancy and rent figures from same source and period
- Pipeline data distinguishes under-construction from planned

## Escalation Notes

- Without MCP data, this skill relies entirely on user-provided information. Clearly state when market data is unverified or unavailable.
- Do not fabricate market statistics. If data is unavailable, say so and suggest where the user can obtain it.
