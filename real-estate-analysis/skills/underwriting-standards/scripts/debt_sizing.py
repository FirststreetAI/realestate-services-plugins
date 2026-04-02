"""
Validated debt sizing functions for real estate underwriting.

Sizes loan proceeds based on DSCR, debt yield, and LTV constraints.
Calculates amortization schedules and loan balances.
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class LoanConstraints:
    """Lender underwriting constraints."""
    max_ltv: float = 0.65  # 65%
    min_dscr: float = 1.25  # 1.25x
    min_debt_yield: float = 0.08  # 8%
    interest_rate: float = 0.055  # 5.5%
    amortization_years: int = 30
    io_years: int = 0
    term_years: int = 10


@dataclass
class DebtSizingResult:
    """Result of debt sizing calculation."""
    max_loan_ltv: float  # Max loan from LTV constraint
    max_loan_dscr: float  # Max loan from DSCR constraint
    max_loan_dy: float  # Max loan from debt yield constraint
    binding_constraint: str  # Which constraint is most restrictive
    sized_loan: float  # Final sized loan (minimum of all constraints)
    ltv: float  # Actual LTV at sized loan
    dscr: float  # Actual DSCR at sized loan
    debt_yield: float  # Actual debt yield at sized loan
    annual_debt_service: float
    monthly_payment: float


def size_loan(
    noi: float,
    property_value: float,
    constraints: LoanConstraints
) -> DebtSizingResult:
    """
    Size a loan based on DSCR, debt yield, and LTV constraints.

    The binding (most restrictive) constraint determines the final loan amount.

    Args:
        noi: Net Operating Income (annual).
        property_value: Appraised or purchase price.
        constraints: Lender underwriting constraints.

    Returns:
        DebtSizingResult with sized loan and constraint analysis.
    """
    # LTV constraint
    max_loan_ltv = property_value * constraints.max_ltv

    # Debt yield constraint: DY = NOI / Loan => Loan = NOI / min_DY
    max_loan_dy = noi / constraints.min_debt_yield if constraints.min_debt_yield > 0 else float('inf')

    # DSCR constraint: DSCR = NOI / DS => DS = NOI / min_DSCR
    # Then solve for loan amount that produces that debt service
    max_ds = noi / constraints.min_dscr if constraints.min_dscr > 0 else float('inf')
    max_loan_dscr = loan_from_debt_service(
        annual_debt_service=max_ds,
        interest_rate=constraints.interest_rate,
        amortization_years=constraints.amortization_years,
        io_years=constraints.io_years
    )

    # Binding constraint is the minimum
    sized_loan = min(max_loan_ltv, max_loan_dscr, max_loan_dy)

    if sized_loan == max_loan_ltv:
        binding = "LTV"
    elif sized_loan == max_loan_dscr:
        binding = "DSCR"
    else:
        binding = "Debt Yield"

    # Calculate actual metrics at sized loan
    annual_ds = calculate_annual_debt_service_amount(
        loan_amount=sized_loan,
        interest_rate=constraints.interest_rate,
        amortization_years=constraints.amortization_years,
        io_years=constraints.io_years,
        current_year=1
    )

    monthly_payment = annual_ds / 12

    actual_ltv = sized_loan / property_value if property_value > 0 else 0
    actual_dscr = noi / annual_ds if annual_ds > 0 else float('inf')
    actual_dy = noi / sized_loan if sized_loan > 0 else float('inf')

    return DebtSizingResult(
        max_loan_ltv=max_loan_ltv,
        max_loan_dscr=max_loan_dscr,
        max_loan_dy=max_loan_dy,
        binding_constraint=binding,
        sized_loan=sized_loan,
        ltv=actual_ltv,
        dscr=actual_dscr,
        debt_yield=actual_dy,
        annual_debt_service=annual_ds,
        monthly_payment=monthly_payment,
    )


def loan_from_debt_service(
    annual_debt_service: float,
    interest_rate: float,
    amortization_years: int,
    io_years: int = 0
) -> float:
    """
    Calculate the loan amount that produces a given annual debt service.

    For IO period, Loan = DS / rate.
    For amortizing, solve the annuity formula backwards.
    """
    if io_years > 0:
        # During IO, DS = Loan * rate
        if interest_rate == 0:
            return float('inf')
        return annual_debt_service / interest_rate

    # Amortizing: monthly payment = DS / 12
    monthly_payment = annual_debt_service / 12
    monthly_rate = interest_rate / 12
    n = amortization_years * 12

    if monthly_rate == 0:
        return monthly_payment * n

    # PV of annuity: Loan = PMT * [(1 - (1+r)^-n) / r]
    loan = monthly_payment * ((1 - (1 + monthly_rate) ** (-n)) / monthly_rate)
    return loan


def calculate_annual_debt_service_amount(
    loan_amount: float,
    interest_rate: float,
    amortization_years: int,
    io_years: int = 0,
    current_year: int = 1
) -> float:
    """Calculate annual debt service for a given year."""
    if current_year <= io_years:
        return loan_amount * interest_rate

    monthly_rate = interest_rate / 12
    n = amortization_years * 12

    if monthly_rate == 0:
        return loan_amount / amortization_years

    monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** n) / \
                     ((1 + monthly_rate) ** n - 1)

    return monthly_payment * 12


def amortization_schedule(
    loan_amount: float,
    interest_rate: float,
    amortization_years: int,
    io_years: int = 0,
    term_years: int = 10
) -> List[dict]:
    """
    Generate annual amortization schedule.

    Returns list of dicts with: year, beginning_balance, interest, principal,
    total_payment, ending_balance.
    """
    schedule = []
    balance = loan_amount
    monthly_rate = interest_rate / 12
    n = amortization_years * 12

    if monthly_rate > 0:
        monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** n) / \
                         ((1 + monthly_rate) ** n - 1)
    else:
        monthly_payment = loan_amount / n

    for year in range(1, term_years + 1):
        beginning_balance = balance
        annual_interest = 0.0
        annual_principal = 0.0

        for month in range(12):
            if year <= io_years:
                month_interest = balance * monthly_rate
                month_principal = 0.0
                month_payment = month_interest
            else:
                month_interest = balance * monthly_rate
                month_principal = monthly_payment - month_interest
                month_payment = monthly_payment
                balance -= month_principal

            annual_interest += month_interest
            annual_principal += month_principal

        schedule.append({
            "year": year,
            "beginning_balance": beginning_balance,
            "interest": annual_interest,
            "principal": annual_principal,
            "total_payment": annual_interest + annual_principal,
            "ending_balance": balance,
        })

    return schedule


def calculate_breakeven_occupancy(
    potential_gross_income: float,
    operating_expenses: float,
    debt_service: float
) -> Optional[float]:
    """
    Calculate breakeven occupancy rate.

    Breakeven = (OpEx + Debt Service) / PGI

    Returns decimal (e.g., 0.82 for 82%), or None if PGI is zero.
    """
    if potential_gross_income == 0:
        return None
    return (operating_expenses + debt_service) / potential_gross_income
