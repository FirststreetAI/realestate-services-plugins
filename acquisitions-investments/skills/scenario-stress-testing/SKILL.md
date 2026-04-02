---
description: Downside construction, breakeven analysis, and sensitivity methodology
---

# Scenario Stress Testing

Framework for constructing downside scenarios and sensitivity analyses. Used by `/downside-case`, `/bid-envelope`, and `/hold-sell`.

## Standard Stress Scenarios

### Rent Stress
- **Mild**: Market rents -5%, rent growth -100bp from base
- **Moderate**: Market rents -10%, rent growth -200bp, 3-month additional downtime on rollover
- **Severe**: Market rents -15%, flat rent growth, 6-month additional downtime

### Vacancy Stress
- **Mild**: +200bp structural vacancy
- **Moderate**: +500bp, largest tenant vacates
- **Severe**: +1000bp, two largest tenants vacate, extended downtime

### Exit Cap Stress
- **Mild**: +25bp exit cap rate
- **Moderate**: +50bp exit cap rate
- **Severe**: +100bp exit cap rate

### Capital Stress
- **Mild**: +20% capex / TI/LC
- **Moderate**: +50% capex, major system replacement
- **Severe**: +100% capex, full repositioning needed

### Financing Stress
- **Mild**: +100bp interest rate
- **Moderate**: +200bp rate, 5% lower LTV
- **Severe**: +300bp rate, 10% lower LTV, no IO period

## Breakeven Analysis

Identify the assumption value at which:
- IRR = 0%
- Equity multiple = 1.0x (return of capital only)
- Cash-on-cash = 0% (no distributable cash flow)

All calculations via `underwriting-standards` scripts. Do NOT solve breakeven by reasoning.

## Output Format

| Scenario | Exit Cap | Rent Growth | Vacancy | IRR | Multiple |
|----------|----------|-------------|---------|-----|----------|
| Base Case | 5.50% | 3.0% | 5.0% | 12.4% | 1.85x |
| Mild Down | 5.75% | 2.0% | 7.0% | 10.1% | 1.65x |
| Moderate | 6.00% | 1.0% | 10.0% | 7.2% | 1.42x |
| Severe | 6.50% | 0.0% | 15.0% | 3.1% | 1.15x |
| Breakeven | 7.25% | -1.0% | 18.0% | 0.0% | 1.00x |
