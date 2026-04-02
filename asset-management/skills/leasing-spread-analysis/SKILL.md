---
description: Lease spread calculations (cash and GAAP), rollover waterfall, and retention economics
---

# Leasing Spread Analysis

The canonical skill for analyzing leasing performance through rent spreads, rollover exposure, and retention economics. Any command that evaluates leasing activity or rollover risk MUST invoke this skill.

## Trigger Conditions

Activated when any command needs:
- New lease or renewal spread calculations (cash and GAAP)
- Rollover waterfall (expiration schedule with mark-to-market)
- Retention rate analysis
- Leasing cost comparison (new lease vs. renewal economics)

## Business Context

Leasing spreads measure whether new and renewal rents are above or below expiring rents, indicating pricing power and portfolio rent trajectory. Retention economics compare the cost of renewing an existing tenant vs. leasing to a new tenant (including downtime, TI, LC, and free rent). Together, these metrics drive revenue projections and inform leasing strategy.

## Workflow

### Cash Spread Calculation
1. For each executed lease (new or renewal):
   - Prior rent = expiring lease base rent per SF (or prior in-place rent for new lease on vacant space)
   - New rent = new lease starting base rent per SF
   - Cash spread = (new rent - prior rent) / prior rent
2. Weight by SF to compute portfolio-level average
3. Report separately for new leases and renewals

### GAAP Spread Calculation
1. For each executed lease:
   - Prior GAAP rent = straight-line average rent over prior lease term
   - New GAAP rent = straight-line average rent over new lease term (including free rent periods, step-ups)
   - GAAP spread = (new GAAP rent - prior GAAP rent) / prior GAAP rent
2. Weight by SF to compute portfolio-level average
3. GAAP spreads account for concessions that cash spreads miss

### Rollover Waterfall
1. List all lease expirations by year (SF, rent, % of total)
2. For each expiring lease, estimate mark-to-market: current rent vs. market rent
3. Calculate rollover exposure: if all expiring leases renew at market, what is the revenue impact?
4. Flag years with concentrated rollover (>15% of total rent expiring)

### Retention Economics
1. Renewal scenario: renewal TI/LC + modest downtime (if any)
2. New lease scenario: new tenant TI + LC + downtime (typically 6-12 months) + free rent
3. Net effective rent comparison: cash flows over lease term, discounted to present value
4. Retention premium: how much lower can a renewal rent be vs. new lease and still be economically equivalent?

## Output Structure

- Spread summary table (cash and GAAP, new leases and renewals, by period)
- Rollover waterfall (annual expirations, SF, rent, mark-to-market estimate)
- Retention economics comparison (renewal vs. new lease NPV)
- Leasing activity detail (each executed lease with terms and spread)

## QA Checks

- Cash and GAAP spreads both computed and reported
- Spreads weighted by SF, not simple average
- Rollover waterfall accounts for 100% of leased SF
- Mark-to-market estimates use current market rents (source stated)
- Retention economics include ALL costs (TI, LC, downtime, free rent)
- New leases on previously vacant space excluded from spread calculation (no prior rent to compare)

## Edge Cases

- **Month-to-month holdover**: Use holdover rent as prior rent; flag as at-risk rollover
- **Below-market lease (anchor)**: Large negative mark-to-market may distort portfolio averages -- report with and without
- **Blend-and-extend**: Treat as renewal; prior rent = current in-place rent, not original lease start rent
- **Multifamily**: Spreads computed per unit rather than per SF; renewal = re-lease to existing resident
