---
description: JV, preferred equity, programmatic structures, and promote mechanics
---

# Deal Structuring

Framework for modeling and comparing acquisition structures. Uses validated waterfall calculation code.

## Structure Types

### Direct Acquisition
- Single investor, 100% equity (plus debt)
- Simplest structure
- All returns accrue to one party
- Best for: smaller deals, single-fund vehicles

### Joint Venture with Promote
- GP contributes 5-20% of equity, LP provides balance
- Returns distributed in tiers:
  - Tier 1: Pari passu until pref return (typically 7-9%)
  - Tier 2: GP catch-up (if applicable)
  - Tier 3+: Promote to GP above IRR hurdles
- Typical structures: 80/20 above 8%, 70/30 above 12%, 60/40 above 15%
- **All waterfall calculations MUST use `returns.py:calculate_waterfall()`**

### Preferred Equity
- Senior equity position with fixed preferred return (8-12%)
- Residual cash flow to common equity sponsor
- Lower risk for preferred investor, higher IRR for common
- Common in capital-constrained situations

### Programmatic Partnership
- Multi-deal commitment (e.g., $200M over 3 years)
- Portfolio-level promote calculation (not deal-by-deal)
- Alignment for repeat partnerships
- More complex to model; requires deal-aggregation logic

## Key Decision Factors

| Factor | Favors JV | Favors Direct | Favors Pref Equity |
|--------|-----------|---------------|-------------------|
| Capital availability | Low GP capital | Ample capital | Capital-constrained |
| Deal size | Large (>$50M) | Moderate | Any |
| GP track record | Proven (LP will trust) | N/A | Any |
| Return profile | High enough for promote | Moderate | High for sponsor |
| Complexity tolerance | Higher | Lower | Moderate |

## Computational Trust

All promote and waterfall calculations MUST be performed by `scripts/returns.py:calculate_waterfall()`. Do NOT reason through promote tiers or catch-up provisions in natural language.
