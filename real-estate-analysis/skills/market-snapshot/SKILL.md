---
description: Submarket supply/demand summary with vacancy, rents, and pipeline
argument-hint: "[submarket or MSA name]"
---

# Market Snapshot

Produce a submarket analysis covering supply/demand dynamics, vacancy trends, rent growth, construction pipeline, absorption, and demographics.

## Skills Invoked

- `market-analysis` -- submarket delineation, supply/demand framework, comp assembly

## Required Inputs

- Submarket or MSA name
- Property type (office, industrial, retail, multifamily)

## Optional Inputs

- Specific competitors or comparable properties to include
- Time period for trend analysis

## Reads from Manifest

None -- typically run standalone or early in a workflow.

## Writes to Manifest

- **Directory**: `market/`
- **Files**: `submarket-snapshot.md`
- **Key metrics**: `vacancy_rate`, `asking_rent_psf`, `yoy_rent_growth`, `pipeline_sf`, `absorption_sf`

## Workflow

### Step 1: Define Submarket

Invoke `market-analysis` to delineate the relevant submarket boundaries. If MCP data sources are available (CoStar), use them. Otherwise, ask user to describe the competitive set.

### Step 2: Supply Analysis

Gather: existing inventory, construction pipeline (under construction + planned), recent deliveries, demolitions/conversions.

### Step 3: Demand Analysis

Gather: net absorption trends, major lease signings, tenant industry composition, employment growth in relevant sectors.

### Step 4: Rent and Vacancy

Current vacancy rate, asking vs. effective rents, rent growth trend (3-year and 5-year), concession trends.

### Step 5: Demographics and Drivers

Population growth, employment by sector, income trends, major employers. Focus on factors that drive demand for the subject property type.

### Step 6: Output

Generate structured markdown report. Write to deal context and update manifest.

## QA Checklist

- [ ] Submarket boundaries defined and stated
- [ ] Data sources and as-of dates documented
- [ ] Vacancy and rent figures include source attribution
- [ ] Pipeline includes both under-construction and planned

## Escalation Notes

- Without MCP data sources, this command relies entirely on user-provided data or publicly available information. State data limitations clearly.
- If user provides no submarket data, explain what data is needed and where to find it (CoStar, local broker reports, census data).
