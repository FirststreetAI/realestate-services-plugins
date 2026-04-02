"""
Unit tests for debt_sizing.py with known-answer inputs.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from debt_sizing import (
    size_loan,
    LoanConstraints,
    calculate_annual_debt_service_amount,
    amortization_schedule,
    calculate_breakeven_occupancy,
    loan_from_debt_service,
)


class TestSizeLoan:
    def test_ltv_binding(self):
        """When LTV is the most restrictive constraint."""
        result = size_loan(
            noi=2_000_000,
            property_value=20_000_000,
            constraints=LoanConstraints(
                max_ltv=0.50,  # Very conservative LTV
                min_dscr=1.00,  # Loose DSCR
                min_debt_yield=0.01,  # Loose DY
                interest_rate=0.05,
                amortization_years=30,
            )
        )
        assert result.binding_constraint == "LTV"
        assert abs(result.sized_loan - 10_000_000) < 1

    def test_dscr_binding(self):
        """When DSCR is the most restrictive constraint."""
        result = size_loan(
            noi=1_000_000,
            property_value=50_000_000,  # Very high value => loose LTV
            constraints=LoanConstraints(
                max_ltv=0.90,  # Loose LTV
                min_dscr=1.50,  # Tight DSCR
                min_debt_yield=0.01,  # Loose DY
                interest_rate=0.06,
                amortization_years=30,
            )
        )
        assert result.binding_constraint == "DSCR"
        assert result.dscr >= 1.49  # Should meet or exceed 1.50

    def test_debt_yield_binding(self):
        """When debt yield is the most restrictive constraint."""
        result = size_loan(
            noi=800_000,
            property_value=50_000_000,  # Very high value => loose LTV
            constraints=LoanConstraints(
                max_ltv=0.90,
                min_dscr=1.00,
                min_debt_yield=0.10,  # Tight DY
                interest_rate=0.04,
                amortization_years=30,
            )
        )
        assert result.binding_constraint == "Debt Yield"
        assert abs(result.sized_loan - 8_000_000) < 1  # NOI / DY = 800K / 0.10

    def test_actual_metrics_correct(self):
        """Verify actual DSCR, LTV, DY are computed correctly at sized loan."""
        result = size_loan(
            noi=1_500_000,
            property_value=20_000_000,
            constraints=LoanConstraints(
                max_ltv=0.65,
                min_dscr=1.25,
                min_debt_yield=0.08,
                interest_rate=0.055,
                amortization_years=30,
            )
        )
        # LTV should be <= 0.65
        assert result.ltv <= 0.6501
        # DSCR should be >= 1.25
        assert result.dscr >= 1.2499
        # DY should be >= 0.08
        assert result.debt_yield >= 0.0799


class TestDebtService:
    def test_io_period(self):
        """Interest-only payment = loan * rate."""
        ds = calculate_annual_debt_service_amount(
            loan_amount=10_000_000,
            interest_rate=0.05,
            amortization_years=30,
            io_years=2,
            current_year=1,
        )
        assert abs(ds - 500_000) < 1

    def test_amortizing(self):
        """Amortizing payment for $10M at 5% over 30 years."""
        ds = calculate_annual_debt_service_amount(
            loan_amount=10_000_000,
            interest_rate=0.05,
            amortization_years=30,
        )
        # Monthly payment ~$53,682, annual ~$644,184
        assert 640_000 < ds < 650_000


class TestAmortizationSchedule:
    def test_schedule_length(self):
        schedule = amortization_schedule(
            loan_amount=10_000_000,
            interest_rate=0.05,
            amortization_years=30,
            term_years=10,
        )
        assert len(schedule) == 10

    def test_balance_decreases(self):
        schedule = amortization_schedule(
            loan_amount=10_000_000,
            interest_rate=0.05,
            amortization_years=30,
            term_years=10,
        )
        for i in range(1, len(schedule)):
            assert schedule[i]["ending_balance"] < schedule[i - 1]["ending_balance"]

    def test_io_then_amortizing(self):
        schedule = amortization_schedule(
            loan_amount=10_000_000,
            interest_rate=0.05,
            amortization_years=30,
            io_years=2,
            term_years=5,
        )
        # First 2 years: no principal, balance unchanged
        assert abs(schedule[0]["principal"]) < 1
        assert abs(schedule[1]["principal"]) < 1
        # Year 3: principal starts
        assert schedule[2]["principal"] > 0


class TestBreakevenOccupancy:
    def test_simple(self):
        be = calculate_breakeven_occupancy(
            potential_gross_income=2_000_000,
            operating_expenses=1_000_000,
            debt_service=500_000,
        )
        assert be is not None
        assert abs(be - 0.75) < 0.001

    def test_zero_pgi(self):
        assert calculate_breakeven_occupancy(0, 100, 100) is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
