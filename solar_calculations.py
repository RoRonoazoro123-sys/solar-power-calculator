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
    """Estimate solar generation and simple financial metrics.

    This is a screening calculator, not a site-specific PV simulation.
    """
    daily_kwh = capacity_kw * sun_hours * performance_ratio
    monthly_kwh = daily_kwh * 30
    annual_kwh = daily_kwh * 365
    panels = math.ceil((capacity_kw * 1000) / panel_w)
    gross_cost = capacity_kw * cost_per_kw
    offset_kwh = annual_kwh * (solar_offset_percent / 100)
    annual_savings = offset_kwh * tariff
    net_annual_benefit = annual_savings - annual_maintenance
    payback_years = gross_cost / net_annual_benefit if net_annual_benefit > 0 else None

    return {
        "daily_kwh": daily_kwh,
        "monthly_kwh": monthly_kwh,
        "annual_kwh": annual_kwh,
        "panels": panels,
        "gross_cost": gross_cost,
        "annual_savings": annual_savings,
        "payback_years": payback_years,
        "required_capacity_kw": daily_load / (sun_hours * performance_ratio) if sun_hours > 0 else None,
    }
