"""Unit tests for fund_returns.py with known-answer inputs."""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fund_returns import (
    PeriodData,
    calculate_twrr,
    decompose_return,
    calculate_tvpi,
    calculate_dpi,
    calculate_rvpi,
    calculate_tger,
    fund_performance_summary,
)


def _make_periods():
    """4 quarters of sample fund data."""
    return [
        PeriodData("2025-Q1", beginning_nav=100_000_000, contributions=0, distributions=1_000_000,
                    ending_nav=102_000_000, income=1_500_000, appreciation=1_500_000),
        PeriodData("2025-Q2", beginning_nav=102_000_000, contributions=0, distributions=1_000_000,
                    ending_nav=104_000_000, income=1_500_000, appreciation=1_500_000),
        PeriodData("2025-Q3", beginning_nav=104_000_000, contributions=0, distributions=1_000_000,
                    ending_nav=106_000_000, income=1_500_000, appreciation=1_500_000),
        PeriodData("2025-Q4", beginning_nav=106_000_000, contributions=0, distributions=1_000_000,
                    ending_nav=108_000_000, income=1_500_000, appreciation=1_500_000),
    ]


class TestTWRR:
    def test_positive_return(self):
        periods = _make_periods()
        twrr = calculate_twrr(periods)
        assert twrr is not None
        assert twrr > 0  # NAV grew and distributed cash

    def test_single_quarter(self):
        periods = [PeriodData("2025-Q1", 100_000, 0, 0, 105_000)]
        twrr = calculate_twrr(periods)
        assert twrr is not None
        assert abs(twrr - 0.05) < 0.001

    def test_empty(self):
        assert calculate_twrr([]) is None

    def test_with_contributions(self):
        """Contributions should not inflate TWRR (time-weighted removes cash flow impact)."""
        periods = [
            PeriodData("Q1", 100_000, contributions=50_000, distributions=0, ending_nav=155_000),
        ]
        twrr = calculate_twrr(periods)
        assert twrr is not None
        # Return should be 5% (155K - 100K - 50K) / 100K = 5%
        assert abs(twrr - 0.05) < 0.001


class TestDecomposeReturn:
    def test_decomposition(self):
        periods = _make_periods()
        result = decompose_return(periods)
        assert result["income_return"] is not None
        assert result["appreciation_return"] is not None
        # Income + appreciation should approximately equal total
        assert abs(result["total_return"] - (result["income_return"] + result["appreciation_return"])) < 0.001

    def test_empty(self):
        result = decompose_return([])
        assert result["total_return"] is None


class TestMultiples:
    def test_tvpi(self):
        # Contributed 100M, received 20M distributions, current NAV = 110M
        tvpi = calculate_tvpi(20_000_000, 110_000_000, 100_000_000)
        assert tvpi is not None
        assert abs(tvpi - 1.30) < 0.001

    def test_dpi(self):
        dpi = calculate_dpi(20_000_000, 100_000_000)
        assert dpi is not None
        assert abs(dpi - 0.20) < 0.001

    def test_rvpi(self):
        rvpi = calculate_rvpi(110_000_000, 100_000_000)
        assert rvpi is not None
        assert abs(rvpi - 1.10) < 0.001

    def test_tvpi_equals_dpi_plus_rvpi(self):
        contrib = 100_000_000
        distrib = 20_000_000
        nav = 110_000_000
        tvpi = calculate_tvpi(distrib, nav, contrib)
        dpi = calculate_dpi(distrib, contrib)
        rvpi = calculate_rvpi(nav, contrib)
        assert abs(tvpi - (dpi + rvpi)) < 0.0001

    def test_zero_contributions(self):
        assert calculate_tvpi(100, 200, 0) is None
        assert calculate_dpi(100, 0) is None
        assert calculate_rvpi(200, 0) is None


class TestTGER:
    def test_simple_tger(self):
        tger = calculate_tger(
            management_fees=1_500_000,
            performance_fees=500_000,
            fund_expenses=200_000,
            gross_asset_value=150_000_000,
        )
        assert tger is not None
        # (1.5M + 0.5M + 0.2M) / 150M = 1.47%
        assert abs(tger - 0.01467) < 0.001

    def test_annualization(self):
        """6 months of fees should be annualized."""
        tger = calculate_tger(
            management_fees=750_000,
            performance_fees=0,
            fund_expenses=0,
            gross_asset_value=100_000_000,
            period_months=6,
        )
        # Annualized: 750K * (12/6) = 1.5M / 100M = 1.5%
        assert abs(tger - 0.015) < 0.001

    def test_zero_gav(self):
        assert calculate_tger(100, 0, 0, 0) is None


class TestFundPerformanceSummary:
    def test_complete_summary(self):
        periods = _make_periods()
        result = fund_performance_summary(
            periods=periods,
            total_contributions=100_000_000,
            total_distributions=4_000_000,
            management_fees=1_500_000,
            performance_fees=0,
            fund_expenses=200_000,
            gross_asset_value=108_000_000,
        )
        assert result["twrr"] is not None
        assert result["tvpi"] is not None
        assert result["dpi"] is not None
        assert result["rvpi"] is not None
        assert result["tger"] is not None
        assert result["current_nav"] == 108_000_000


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
