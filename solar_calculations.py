
import math


def estimate_solar(
    capacity_kw: float,
    panel_w: float,
    sun_hours: float,
    performance_ratio: float,
    cost_per_kw: float,
    tariff: float,
    solar_offset_percent: float = 80,
    annual_maintenance: float = 0,
    daily_load: float = 0,
) -> dict:
    """Estimate solar generation and basic financial metrics.

    This is an estimate, not a site-specific PV simulation.
    """

    # Validate inputs
    if capacity_kw < 0:
        raise ValueError("Solar capacity cannot be negative.")
    if panel_w <= 0:
        raise ValueError("Panel wattage must be greater than zero.")
    if sun_hours < 0:
        raise ValueError("Sun hours cannot be negative.")
    if not 0 <= performance_ratio <= 1:
        raise ValueError("Performance ratio must be between 0 and 1.")
    if cost_per_kw < 0 or tariff < 0:
        raise ValueError("Cost and electricity tariff cannot be negative.")
    if not 0 <= solar_offset_percent <= 100:
        raise ValueError("Solar offset must be between 0 and 100 percent.")
    if annual_maintenance < 0 or daily_load < 0:
        raise ValueError("Maintenance and daily load cannot be negative.")

    # Energy generation estimates
    daily_kwh = capacity_kw * sun_hours * performance_ratio
    monthly_kwh = daily_kwh * 30
    annual_kwh = daily_kwh * 365

    # System size and cost
    panels = math.ceil((capacity_kw * 1000) / panel_w)
    gross_cost = capacity_kw * cost_per_kw

    # Estimated bill savings
    offset_kwh = annual_kwh * (solar_offset_percent / 100)
    annual_savings = offset_kwh * tariff
    net_annual_benefit = annual_savings - annual_maintenance

    payback_years = (
        gross_cost / net_annual_benefit
        if net_annual_benefit > 0
        else None
    )

    required_capacity_kw = (
        daily_load / (sun_hours * performance_ratio)
        if sun_hours > 0 and performance_ratio > 0
        else None
    )

    return {
        "daily_kwh": daily_kwh,
        "monthly_kwh": monthly_kwh,
        "annual_kwh": annual_kwh,
        "panels": panels,
        "gross_cost": gross_cost,
        "annual_savings": annual_savings,
        "payback_years": payback_years,
        "required_capacity_kw": required_capacity_kw,
    }
