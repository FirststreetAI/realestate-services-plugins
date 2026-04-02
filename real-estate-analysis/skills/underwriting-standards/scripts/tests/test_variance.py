"""Unit tests for variance.py."""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from variance import calculate_variance, noi_variance_bridge


class TestCalculateVariance:
    def test_basic_variance(self):
        actuals = {"Rent": 1_000_000, "Utilities": 50_000}
        budget = {"Rent": 950_000, "Utilities": 45_000}
        results = calculate_variance(actuals, budget)
        assert len(results) == 2
        rent = next(r for r in results if r.line_item == "Rent")
        assert rent.variance_dollar == 50_000

    def test_materiality_flagging(self):
        actuals = {"Big Item": 200_000, "Small Item": 10_100}
        budget = {"Big Item": 100_000, "Small Item": 10_000}
        results = calculate_variance(
            actuals, budget,
            materiality_threshold_pct=0.05,
            materiality_threshold_dollar=10_000,
        )
        big = next(r for r in results if r.line_item == "Big Item")
        small = next(r for r in results if r.line_item == "Small Item")
        assert big.is_material
        assert not small.is_material  # $100 variance < $10K threshold

    def test_missing_items(self):
        actuals = {"A": 100, "B": 200}
        budget = {"B": 150, "C": 300}
        results = calculate_variance(actuals, budget)
        assert len(results) == 3
        a = next(r for r in results if r.line_item == "A")
        assert a.comparison == 0.0
        c = next(r for r in results if r.line_item == "C")
        assert c.actual == 0.0

    def test_sorted_by_magnitude(self):
        actuals = {"Small": 110, "Large": 500}
        budget = {"Small": 100, "Large": 200}
        results = calculate_variance(actuals, budget)
        assert results[0].line_item == "Large"


class TestNOIBridge:
    def test_beat_budget(self):
        result = noi_variance_bridge(
            actual_revenue=2_000_000,
            actual_expenses=1_000_000,
            budget_revenue=1_900_000,
            budget_expenses=1_050_000,
        )
        assert result["beat_budget"]
        assert result["actual_noi"] == 1_000_000
        assert result["budget_noi"] == 850_000
        assert result["noi_variance"] == 150_000

    def test_miss_budget(self):
        result = noi_variance_bridge(
            actual_revenue=1_800_000,
            actual_expenses=1_100_000,
            budget_revenue=1_900_000,
            budget_expenses=1_000_000,
        )
        assert not result["beat_budget"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
