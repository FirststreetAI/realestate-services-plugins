---
description: Fund-level return calculations including TWRR, IRR, TVPI/DPI/RVPI, and TGER
argument-hint: "[fund name or period]"
---

# Fund Performance

Calculate and present fund-level performance metrics: time-weighted return (TWRR), internal rate of return (IRR), investment multiples (TVPI/DPI/RVPI), and total gross expense ratio (TGER).

## Skills Invoked

- `fund-return-calculations` -- return methodology, NCREIF/PREA standards compliance

## Required Inputs

- Fund cash flow history (contributions, distributions, with dates)
- Current fund NAV (as of reporting date)
- Fund expense data (management fees, fund-level expenses)

## Optional Inputs

- Property-level valuations for NAV build-up
- Benchmark data (NPI, ODCE) for comparison
- Prior period returns for trend analysis
- Fund terms (vintage year, committed capital, investment period status)

## Reads from Manifest

None -- fund-level command that operates on fund-level data.

## Writes to Manifest

- **Directory**: `performance/`
- **Files**: `fund-returns.xlsx`
- **Key metrics**: `twrr_gross`, `twrr_net`, `irr_gross`, `irr_net`, `tvpi`, `dpi`, `rvpi`, `tger`

## Workflow

### Step 1: Validate Cash Flow Data

Confirm cash flow series is complete: all contributions, distributions, and current NAV with dates. Flag gaps or inconsistencies.

### Step 2: Calculate Returns

**CRITICAL**: ALL return calculations MUST be performed by `scripts/fund_returns.py`. Do NOT compute TWRR, IRR, or multiples by reasoning through the math.

Invoke `fund-return-calculations` which calls:
- `scripts/fund_returns.py:calculate_twrr()` -- time-weighted return (gross and net)
- `scripts/fund_returns.py:calculate_irr()` -- since-inception IRR (gross and net)
- `scripts/fund_returns.py:calculate_multiples()` -- TVPI, DPI, RVPI
- `scripts/fund_returns.py:calculate_tger()` -- total gross expense ratio

### Step 3: Benchmark Comparison (if data available)

Compare fund returns to relevant benchmark (NPI for core, ODCE for open-end commingled). Calculate excess return and tracking error.

### Step 4: Period Returns

Calculate quarterly and YTD returns in addition to since-inception. TWRR for periodic, IRR for since-inception.

### Step 5: Output

Generate `fund-returns.xlsx` with tabs:
1. Return Summary (TWRR, IRR, multiples -- gross and net)
2. Cash Flow Detail (contributions, distributions, NAV by period)
3. Period Returns (quarterly, annual, since-inception)
4. Benchmark Comparison (if applicable)
5. Expense Analysis (TGER components)

Write to performance directory and update manifest.

## QA Checklist

- [ ] Cash flow series is complete with no gaps
- [ ] TWRR and IRR computed by `scripts/fund_returns.py`, not LLM reasoning
- [ ] Gross and net returns both reported
- [ ] TVPI = DPI + RVPI (must tie)
- [ ] NAV used for RVPI matches latest valuation
- [ ] TGER components itemized
- [ ] Benchmark comparison uses appropriate index
- [ ] Period returns chain-link to since-inception return

## Escalation Notes

- If cash flow data is incomplete, cannot produce reliable returns -- ask user for complete data
- If NAV is stale (>1 quarter old), flag and note the as-of date
- This skill assists with return calculation and preparation. Output does NOT guarantee submission-readiness for NCREIF or other reporting bodies.
