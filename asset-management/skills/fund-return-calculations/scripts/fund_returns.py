"""
Validated fund-level return calculation functions.

Calculates TWRR, IRR, TVPI/DPI/RVPI, and TGER for fund-level performance reporting.
Assists with NCREIF/PREA reporting preparation -- does NOT guarantee submission-readiness.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class PeriodData:
    """Single period (quarter) of fund data."""
    period: str  # e.g., "2026-Q1"
    beginning_nav: float
    contributions: float  # Capital called (positive)
    distributions: float  # Capital returned (positive)
    ending_nav: float
    income: float = 0.0  # Net income for the period
    appreciation: float = 0.0  # Change in value net of capex


def calculate_twrr(periods: List[PeriodData]) -> Optional[float]:
    """
    Calculate Time-Weighted Rate of Return (TWRR).

    TWRR removes the impact of cash flow timing (contributions/distributions)
    and measures pure investment performance. This is the standard methodology
    for NCREIF index comparison.

    The formula chains sub-period returns:
    TWRR = [(1+r1) * (1+r2) * ... * (1+rn)] - 1

    Where each sub-period return:
    r = (ending_nav - beginning_nav - contributions + distributions) / beginning_nav

    Returns annualized TWRR if more than one year of data.
    """
    if not periods:
        return None

    chain = 1.0
    for p in periods:
        if p.beginning_nav == 0:
            continue
        # Sub-period return
        r = (p.ending_nav - p.beginning_nav - p.contributions + p.distributions) / p.beginning_nav
        chain *= (1 + r)

    total_return = chain - 1

    # Annualize if more than 4 quarters
    n_quarters = len(periods)
    if n_quarters > 4:
        years = n_quarters / 4.0
        if chain > 0:
            annualized = chain ** (1.0 / years) - 1
            return annualized
        return None

    return total_return


def decompose_return(periods: List[PeriodData]) -> dict:
    """
    Decompose total return into income return and appreciation return.

    Income return = sum of income / average NAV
    Appreciation return = sum of appreciation / average NAV

    Used for NCREIF NPI-style return attribution.
    """
    if not periods:
        return {"income_return": None, "appreciation_return": None, "total_return": None}

    total_income = sum(p.income for p in periods)
    total_appreciation = sum(p.appreciation for p in periods)

    # Average NAV (simple average of beginning NAVs)
    avg_nav = sum(p.beginning_nav for p in periods) / len(periods)

    if avg_nav == 0:
        return {"income_return": None, "appreciation_return": None, "total_return": None}

    income_return = total_income / avg_nav
    appreciation_return = total_appreciation / avg_nav
    total_return = income_return + appreciation_return

    return {
        "income_return": income_return,
        "appreciation_return": appreciation_return,
        "total_return": total_return,
    }


def calculate_tvpi(
    total_distributions: float,
    current_nav: float,
    total_contributions: float
) -> Optional[float]:
    """
    Calculate Total Value to Paid-In Capital (TVPI).

    TVPI = (Cumulative Distributions + Current NAV) / Cumulative Contributions

    Includes both realized and unrealized value.
    """
    if total_contributions == 0:
        return None
    return (total_distributions + current_nav) / total_contributions


def calculate_dpi(
    total_distributions: float,
    total_contributions: float
) -> Optional[float]:
    """
    Calculate Distributions to Paid-In Capital (DPI).

    DPI = Cumulative Distributions / Cumulative Contributions

    Realized returns only.
    """
    if total_contributions == 0:
        return None
    return total_distributions / total_contributions


def calculate_rvpi(
    current_nav: float,
    total_contributions: float
) -> Optional[float]:
    """
    Calculate Residual Value to Paid-In Capital (RVPI).

    RVPI = Current NAV / Cumulative Contributions

    Unrealized value remaining.
    Note: TVPI = DPI + RVPI
    """
    if total_contributions == 0:
        return None
    return current_nav / total_contributions


def calculate_tger(
    management_fees: float,
    performance_fees: float,
    fund_expenses: float,
    gross_asset_value: float,
    period_months: int = 12
) -> Optional[float]:
    """
    Calculate Total Global Expense Ratio (TGER).

    TGER = (Management Fees + Performance Fees + Fund Expenses) / GAV

    Per NCREIF/PREA/INREV Global Definitions Database methodology.
    Reported as a rolling 12-month figure.

    Args:
        management_fees: Total management/advisory fees for the period.
        performance_fees: Carried interest / promote fees for the period.
        fund_expenses: Other fund-level expenses (legal, audit, admin).
        gross_asset_value: Average GAV for the period.
        period_months: Number of months in the fee period (for annualization).

    Returns:
        TGER as decimal (e.g., 0.015 for 1.5%).
    """
    if gross_asset_value == 0:
        return None

    total_fees = management_fees + performance_fees + fund_expenses

    # Annualize if less than 12 months
    if period_months < 12:
        total_fees = total_fees * (12 / period_months)

    return total_fees / gross_asset_value


def fund_performance_summary(
    periods: List[PeriodData],
    total_contributions: float,
    total_distributions: float,
    management_fees: float = 0,
    performance_fees: float = 0,
    fund_expenses: float = 0,
    gross_asset_value: float = 0
) -> dict:
    """
    Produce a complete fund performance summary.

    Returns dict with all fund-level metrics.
    """
    current_nav = periods[-1].ending_nav if periods else 0

    twrr = calculate_twrr(periods)
    decomposition = decompose_return(periods)
    tvpi = calculate_tvpi(total_distributions, current_nav, total_contributions)
    dpi = calculate_dpi(total_distributions, total_contributions)
    rvpi = calculate_rvpi(current_nav, total_contributions)
    tger = calculate_tger(management_fees, performance_fees, fund_expenses, gross_asset_value) if gross_asset_value > 0 else None

    return {
        "twrr": twrr,
        "income_return": decomposition["income_return"],
        "appreciation_return": decomposition["appreciation_return"],
        "tvpi": tvpi,
        "dpi": dpi,
        "rvpi": rvpi,
        "tger": tger,
        "current_nav": current_nav,
        "total_contributions": total_contributions,
        "total_distributions": total_distributions,
    }
