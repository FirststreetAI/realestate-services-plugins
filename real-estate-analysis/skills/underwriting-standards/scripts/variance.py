"""
Validated variance analysis functions for comparing actuals vs. budget/prior year.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class VarianceItem:
    """Single line-item variance result."""
    line_item: str
    actual: float
    comparison: float
    variance_dollar: float
    variance_pct: Optional[float]
    is_material: bool
    category: str = ""  # Revenue, Operating Expense, Capital, etc.
    controllable: bool = True  # Controllable vs. uncontrollable


def calculate_variance(
    actuals: Dict[str, float],
    comparison: Dict[str, float],
    materiality_threshold_pct: float = 0.05,
    materiality_threshold_dollar: float = 10_000,
    revenue_items: Optional[List[str]] = None
) -> List[VarianceItem]:
    """
    Calculate line-item variances between actuals and comparison basis.

    Args:
        actuals: Dict of {line_item: amount} for actual results.
        comparison: Dict of {line_item: amount} for budget/prior year.
        materiality_threshold_pct: Flag if abs(variance_pct) exceeds this.
        materiality_threshold_dollar: Flag if abs(variance_dollar) exceeds this.
        revenue_items: List of line item names that are revenue (positive = favorable).
                       All others treated as expenses (negative = favorable).

    Returns:
        List of VarianceItem sorted by absolute dollar variance descending.
    """
    if revenue_items is None:
        revenue_items = []

    all_items = set(list(actuals.keys()) + list(comparison.keys()))
    results = []

    for item in all_items:
        actual_val = actuals.get(item, 0.0)
        comp_val = comparison.get(item, 0.0)

        variance_dollar = actual_val - comp_val

        if comp_val != 0:
            variance_pct = variance_dollar / abs(comp_val)
        else:
            variance_pct = None

        is_material = (
            abs(variance_dollar) >= materiality_threshold_dollar and
            (variance_pct is None or abs(variance_pct) >= materiality_threshold_pct)
        )

        results.append(VarianceItem(
            line_item=item,
            actual=actual_val,
            comparison=comp_val,
            variance_dollar=variance_dollar,
            variance_pct=variance_pct,
            is_material=is_material,
        ))

    # Sort by absolute dollar variance, largest first
    results.sort(key=lambda x: abs(x.variance_dollar), reverse=True)
    return results


def noi_variance_bridge(
    actual_revenue: float,
    actual_expenses: float,
    budget_revenue: float,
    budget_expenses: float
) -> dict:
    """
    Build an NOI variance bridge from budget to actual.

    Returns dict with revenue_variance, expense_variance, noi_variance,
    and whether NOI beat or missed budget.
    """
    actual_noi = actual_revenue - actual_expenses
    budget_noi = budget_revenue - budget_expenses
    noi_variance = actual_noi - budget_noi
    revenue_variance = actual_revenue - budget_revenue
    expense_variance = actual_expenses - budget_expenses  # Positive = over budget (bad)

    return {
        "actual_noi": actual_noi,
        "budget_noi": budget_noi,
        "noi_variance": noi_variance,
        "noi_variance_pct": noi_variance / abs(budget_noi) if budget_noi != 0 else None,
        "revenue_variance": revenue_variance,
        "expense_variance": expense_variance,
        "beat_budget": noi_variance > 0,
    }
