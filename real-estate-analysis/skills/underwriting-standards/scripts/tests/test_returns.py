"""
Unit tests for returns.py with known-answer inputs verified against Excel.
"""

import pytest
from datetime import date
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from returns import (
    calculate_irr,
    calculate_xirr,
    calculate_npv,
    calculate_equity_multiple,
    calculate_cash_on_cash,
    calculate_waterfall,
)


class TestIRR:
    def test_simple_irr(self):
        """Verified against Excel IRR function."""
        # -1000 invested, +300/yr for 5 years => IRR ~= 15.24%
        cfs = [-1000, 300, 300, 300, 300, 300]
        irr = calculate_irr(cfs)
        assert irr is not None
        assert abs(irr - 0.15238) < 0.001

    def test_real_estate_acquisition(self):
        """Typical RE acquisition: buy, hold 5 years, sell."""
        # Buy for $10M, $800K/yr cash flow, sell for $12M in year 5
        cfs = [-10_000_000, 800_000, 800_000, 800_000, 800_000, 800_000 + 12_000_000]
        irr = calculate_irr(cfs)
        assert irr is not None
        assert 0.10 < irr < 0.15  # Should be ~12.4%

    def test_negative_irr(self):
        """Investment that loses money."""
        cfs = [-1000, 100, 100, 100, 100]
        irr = calculate_irr(cfs)
        assert irr is not None
        assert irr < 0

    def test_no_sign_change(self):
        """All positive or all negative => no IRR."""
        assert calculate_irr([100, 200, 300]) is None
        assert calculate_irr([-100, -200, -300]) is None

    def test_empty_cashflows(self):
        assert calculate_irr([]) is None
        assert calculate_irr([100]) is None

    def test_zero_irr(self):
        """Break-even investment."""
        cfs = [-1000, 250, 250, 250, 250]
        irr = calculate_irr(cfs)
        assert irr is not None
        assert abs(irr) < 0.01


class TestXIRR:
    def test_simple_xirr(self):
        """Verified against Excel XIRR."""
        cfs = [-10000, 2750, 4250, 3250, 2750]
        dates = [
            date(2024, 1, 1),
            date(2025, 1, 1),
            date(2026, 1, 1),
            date(2027, 1, 1),
            date(2028, 1, 1),
        ]
        xirr = calculate_xirr(cfs, dates)
        assert xirr is not None
        assert 0.10 < xirr < 0.20

    def test_mismatched_lengths(self):
        assert calculate_xirr([100, 200], [date(2024, 1, 1)]) is None


class TestNPV:
    def test_simple_npv(self):
        """Verified against Excel NPV (note: Excel NPV doesn't include period 0)."""
        # At 10% discount rate
        cfs = [-1000, 300, 300, 300, 300, 300]
        npv = calculate_npv(0.10, cfs)
        assert abs(npv - 137.24) < 1.0

    def test_zero_rate(self):
        cfs = [-1000, 300, 300, 300, 300]
        npv = calculate_npv(0.0, cfs)
        assert abs(npv - 200.0) < 0.01


class TestEquityMultiple:
    def test_simple_multiple(self):
        # Invest 1000, get back 2100 total => 2.1x
        cfs = [-1000, 200, 200, 200, 200, 1300]
        em = calculate_equity_multiple(cfs)
        assert em is not None
        assert abs(em - 2.1) < 0.01

    def test_no_investment(self):
        assert calculate_equity_multiple([100, 200]) is None

    def test_loss(self):
        cfs = [-1000, 100, 100]
        em = calculate_equity_multiple(cfs)
        assert em is not None
        assert em < 1.0


class TestCashOnCash:
    def test_simple(self):
        coc = calculate_cash_on_cash(80_000, 1_000_000)
        assert coc is not None
        assert abs(coc - 0.08) < 0.001

    def test_zero_equity(self):
        assert calculate_cash_on_cash(80_000, 0) is None


class TestWaterfall:
    def test_basic_waterfall(self):
        """Basic 80/20 promote above 8% pref."""
        cfs = [-10_000_000, 800_000, 800_000, 800_000, 800_000, 800_000 + 12_000_000]
        result = calculate_waterfall(
            cashflows=cfs,
            pref_rate=0.08,
            promote_tiers=[(0.08, 0.20)],
            gp_coinvest_pct=0.10,
        )
        assert result["lp_irr"] is not None
        assert result["gp_irr"] is not None
        assert result["lp_multiple"] is not None
        assert result["promote_total"] > 0
        # LP should get less than unlevered project
        project_irr = calculate_irr(cfs)
        assert result["lp_irr"] < project_irr

    def test_below_pref(self):
        """If project IRR is below pref, no promote."""
        cfs = [-10_000_000, 300_000, 300_000, 300_000, 300_000, 300_000 + 9_000_000]
        result = calculate_waterfall(
            cashflows=cfs,
            pref_rate=0.12,
            promote_tiers=[(0.12, 0.20)],
            gp_coinvest_pct=0.10,
        )
        assert result["promote_total"] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
