"""
Validated pro forma construction functions for real estate underwriting.

Builds multi-year NOI projections, cash flow waterfalls, and capital reserve schedules.
All functions are precision-sensitive -- the LLM must call these rather than reasoning.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class RentAssumptions:
    """Assumptions for a single tenant or unit type."""
    name: str
    annual_rent: float  # Current annual rent
    square_feet: float
    lease_start_year: int  # Year 1 = first year of hold
    lease_end_year: int
    annual_escalation: float = 0.03  # 3% annual bumps
    market_rent_psf: Optional[float] = None  # For mark-to-market at rollover
    renewal_probability: float = 0.70
    downtime_months: int = 6  # Months vacant if tenant leaves
    tenant_improvement_psf: float = 0.0  # TI on renewal/new lease
    leasing_commission_pct: float = 0.04  # LC as % of lease value


@dataclass
class ExpenseAssumptions:
    """Operating expense assumptions."""
    base_year_expenses: float  # Total operating expenses in year 1
    annual_growth_rate: float = 0.03  # Expense growth rate
    management_fee_pct: float = 0.03  # % of EGI


@dataclass
class DebtAssumptions:
    """Loan terms."""
    loan_amount: float
    interest_rate: float  # Annual rate as decimal
    amortization_years: int = 30
    io_years: int = 0  # Interest-only period
    term_years: int = 10


@dataclass
class ProFormaInputs:
    """All inputs needed to build a pro forma."""
    hold_period_years: int
    purchase_price: float
    closing_costs_pct: float = 0.02
    tenants: List[RentAssumptions] = field(default_factory=list)
    vacancy_rate: float = 0.05  # Structural vacancy
    credit_loss_pct: float = 0.01
    expenses: Optional[ExpenseAssumptions] = None
    capital_reserves_psf: float = 0.25  # Annual reserves per SF
    total_sf: float = 0.0
    exit_cap_rate: float = 0.06
    selling_costs_pct: float = 0.02
    debt: Optional[DebtAssumptions] = None


@dataclass
class ProFormaYear:
    """Single year of pro forma output."""
    year: int
    potential_gross_income: float = 0.0
    vacancy_loss: float = 0.0
    credit_loss: float = 0.0
    effective_gross_income: float = 0.0
    operating_expenses: float = 0.0
    management_fee: float = 0.0
    net_operating_income: float = 0.0
    capital_reserves: float = 0.0
    tenant_improvements: float = 0.0
    leasing_commissions: float = 0.0
    net_cash_flow: float = 0.0  # Before debt
    debt_service: float = 0.0
    cash_flow_after_debt: float = 0.0


def build_proforma(inputs: ProFormaInputs) -> List[ProFormaYear]:
    """
    Build a multi-year pro forma from inputs.

    Returns a list of ProFormaYear objects, one per year of the hold period.
    """
    years = []

    for yr in range(1, inputs.hold_period_years + 1):
        pfy = ProFormaYear(year=yr)

        # Revenue: sum of tenant rents with escalations
        pgi = 0.0
        ti_cost = 0.0
        lc_cost = 0.0

        for tenant in inputs.tenants:
            if yr < tenant.lease_start_year or yr > inputs.hold_period_years:
                continue

            if yr <= tenant.lease_end_year:
                # Tenant in place -- escalate from base
                years_escalated = yr - tenant.lease_start_year
                escalated_rent = tenant.annual_rent * (1 + tenant.annual_escalation) ** years_escalated
                pgi += escalated_rent
            else:
                # Lease expired -- model rollover
                rollover_year = tenant.lease_end_year + 1
                if yr == rollover_year:
                    # Downtime in rollover year
                    occupied_months = max(0, 12 - tenant.downtime_months)
                    if tenant.market_rent_psf is not None:
                        new_rent = tenant.market_rent_psf * tenant.square_feet
                    else:
                        # Escalate from last in-place
                        years_from_start = tenant.lease_end_year - tenant.lease_start_year
                        new_rent = tenant.annual_rent * (1 + tenant.annual_escalation) ** (years_from_start + 1)

                    pgi += new_rent * (occupied_months / 12.0)

                    # TI and LC costs
                    ti_cost += tenant.tenant_improvement_psf * tenant.square_feet
                    lc_cost += new_rent * tenant.leasing_commission_pct * 5  # 5-year lease assumption
                else:
                    # Post-rollover: tenant re-leased, escalate from market
                    years_since_rollover = yr - rollover_year
                    if tenant.market_rent_psf is not None:
                        base_rent = tenant.market_rent_psf * tenant.square_feet
                    else:
                        years_from_start = tenant.lease_end_year - tenant.lease_start_year
                        base_rent = tenant.annual_rent * (1 + tenant.annual_escalation) ** (years_from_start + 1)
                    pgi += base_rent * (1 + tenant.annual_escalation) ** years_since_rollover

        pfy.potential_gross_income = pgi
        pfy.vacancy_loss = pgi * inputs.vacancy_rate
        pfy.credit_loss = pgi * inputs.credit_loss_pct
        pfy.effective_gross_income = pgi - pfy.vacancy_loss - pfy.credit_loss

        # Expenses
        if inputs.expenses:
            pfy.operating_expenses = inputs.expenses.base_year_expenses * (1 + inputs.expenses.annual_growth_rate) ** (yr - 1)
            pfy.management_fee = pfy.effective_gross_income * inputs.expenses.management_fee_pct
        else:
            pfy.operating_expenses = 0.0
            pfy.management_fee = 0.0

        pfy.net_operating_income = pfy.effective_gross_income - pfy.operating_expenses - pfy.management_fee

        # Capital items
        pfy.capital_reserves = inputs.capital_reserves_psf * inputs.total_sf
        pfy.tenant_improvements = ti_cost
        pfy.leasing_commissions = lc_cost

        pfy.net_cash_flow = pfy.net_operating_income - pfy.capital_reserves - pfy.tenant_improvements - pfy.leasing_commissions

        # Debt service
        if inputs.debt:
            pfy.debt_service = calculate_annual_debt_service(
                loan_amount=inputs.debt.loan_amount,
                interest_rate=inputs.debt.interest_rate,
                amortization_years=inputs.debt.amortization_years,
                io_years=inputs.debt.io_years,
                current_year=yr
            )
        else:
            pfy.debt_service = 0.0

        pfy.cash_flow_after_debt = pfy.net_cash_flow - pfy.debt_service

        years.append(pfy)

    return years


def calculate_annual_debt_service(
    loan_amount: float,
    interest_rate: float,
    amortization_years: int,
    io_years: int = 0,
    current_year: int = 1
) -> float:
    """
    Calculate annual debt service for a given year.

    Handles interest-only periods followed by amortizing payments.
    """
    if current_year <= io_years:
        # Interest only
        return loan_amount * interest_rate

    # Amortizing payment
    monthly_rate = interest_rate / 12
    total_payments = amortization_years * 12

    if monthly_rate == 0:
        monthly_payment = loan_amount / total_payments
    else:
        monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** total_payments) / \
                         ((1 + monthly_rate) ** total_payments - 1)

    return monthly_payment * 12


def calculate_reversion(
    terminal_noi: float,
    exit_cap_rate: float,
    selling_costs_pct: float = 0.02,
    loan_balance: Optional[float] = None
) -> dict:
    """
    Calculate sale/reversion proceeds at end of hold period.

    Args:
        terminal_noi: NOI in the year after the hold period (forward NOI).
        exit_cap_rate: Exit capitalization rate.
        selling_costs_pct: Selling costs as % of sale price.
        loan_balance: Outstanding loan balance at sale (if applicable).

    Returns:
        Dict with gross_sale_price, selling_costs, net_sale_proceeds,
        loan_payoff, net_equity_proceeds.
    """
    gross_sale_price = terminal_noi / exit_cap_rate
    selling_costs = gross_sale_price * selling_costs_pct
    net_sale_proceeds = gross_sale_price - selling_costs
    loan_payoff = loan_balance or 0.0
    net_equity_proceeds = net_sale_proceeds - loan_payoff

    return {
        "gross_sale_price": gross_sale_price,
        "selling_costs": selling_costs,
        "net_sale_proceeds": net_sale_proceeds,
        "loan_payoff": loan_payoff,
        "net_equity_proceeds": net_equity_proceeds,
    }


def build_cashflow_series(
    inputs: ProFormaInputs,
    proforma_years: List[ProFormaYear]
) -> List[float]:
    """
    Build the full equity cash flow series for IRR/multiple calculation.

    Returns list where index 0 = initial equity investment (negative),
    indices 1..n = annual cash flows after debt,
    last element includes reversion proceeds.
    """
    # Initial investment
    total_cost = inputs.purchase_price * (1 + inputs.closing_costs_pct)
    equity = total_cost - (inputs.debt.loan_amount if inputs.debt else 0)
    cashflows = [-equity]

    # Annual operating cash flows
    for i, yr in enumerate(proforma_years):
        cf = yr.cash_flow_after_debt

        # Add reversion in final year
        if i == len(proforma_years) - 1:
            # Terminal NOI = last year NOI grown one more year
            terminal_noi = yr.net_operating_income * (1 + (inputs.expenses.annual_growth_rate if inputs.expenses else 0.03))
            reversion = calculate_reversion(
                terminal_noi=terminal_noi,
                exit_cap_rate=inputs.exit_cap_rate,
                selling_costs_pct=inputs.selling_costs_pct,
                loan_balance=inputs.debt.loan_amount * 0.95 if inputs.debt else None  # Simplified balance
            )
            cf += reversion["net_equity_proceeds"]

        cashflows.append(cf)

    return cashflows
