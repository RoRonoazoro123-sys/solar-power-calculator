import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from solar_calculations import estimate_solar

st.set_page_config(page_title="Solar Power Calculator", page_icon="☀️", layout="wide")
st.title("☀️ Solar Power Calculator")
st.write("Estimate solar electricity generation, system cost, savings, and simple payback.")

with st.sidebar:
    st.header("Solar system inputs")
    capacity_kw = st.number_input("System capacity (kW)", min_value=0.5, max_value=1000.0, value=3.0, step=0.5)
    panel_w = st.number_input("Panel rating (W)", min_value=100, max_value=800, value=500, step=25)
    sun_hours = st.number_input("Average peak sun hours/day", min_value=0.5, max_value=10.0, value=5.0, step=0.25)
    performance_ratio = st.slider("Performance ratio", min_value=0.50, max_value=0.95, value=0.80, step=0.01)
    daily_load = st.number_input("Daily electricity use (kWh)", min_value=0.0, value=10.0, step=1.0)
    cost_per_kw = st.number_input("Installed cost (₹ per kW)", min_value=0, value=60000, step=5000)
    tariff = st.number_input("Electricity tariff (₹/kWh)", min_value=0.0, value=8.0, step=0.5)
    solar_offset = st.slider("Share of solar generation that offsets your bill (%)", 0, 100, 80)
    annual_maintenance = st.number_input("Annual maintenance estimate (₹)", min_value=0, value=1500, step=500)

result = estimate_solar(
    capacity_kw=capacity_kw,
    panel_w=panel_w,
    sun_hours=sun_hours,
    performance_ratio=performance_ratio,
    cost_per_kw=cost_per_kw,
    tariff=tariff,
    solar_offset_percent=solar_offset,
    annual_maintenance=annual_maintenance,
    daily_load=daily_load,
)

st.subheader("Estimated results")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Daily generation", f"{result['daily_kwh']:,.1f} kWh")
c2.metric("Monthly generation", f"{result['monthly_kwh']:,.0f} kWh")
c3.metric("Annual generation", f"{result['annual_kwh']:,.0f} kWh")
c4.metric("Estimated panel count", f"{result['panels']}")

c5, c6, c7 = st.columns(3)
c5.metric("Estimated system cost", f"₹{result['gross_cost']:,.0f}")
c6.metric("Annual bill savings (estimate)", f"₹{result['annual_savings']:,.0f}")
if result["payback_years"] is None:
    payback_text = "Not calculated"
else:
    payback_text = f"{result['payback_years']:.1f} years"
c7.metric("Simple payback", payback_text)

st.caption("Estimates only. Actual output depends on location, weather, roof direction/tilt, shading, equipment, tariff rules, and how much energy you use or export.")

st.subheader("Monthly energy estimate")
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
# Simple demonstration model: equal monthly generation. Replace with location-specific monthly solar data for better accuracy.
monthly_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
monthly = pd.DataFrame({
    "Month": months,
    "Estimated generation (kWh)": [result["daily_kwh"] * d for d in monthly_days]
})
fig, ax = plt.subplots()
ax.bar(monthly["Month"], monthly["Estimated generation (kWh)"])
ax.set_ylabel("Energy (kWh)")
ax.set_xlabel("Month")
ax.set_title("Estimated monthly solar generation (constant average conditions)")
ax.grid(axis="y", alpha=0.25)
st.pyplot(fig)
plt.close(fig)

st.subheader("System sizing check")
if daily_load > 0:
    required_kw = daily_load / (sun_hours * performance_ratio)
    st.write(f"Approximate PV capacity to generate your daily usage: **{required_kw:.2f} kW**.")
    st.write(f"Your selected system capacity is **{capacity_kw:.2f} kW**.")
else:
    st.write("Enter a daily electricity use above zero to estimate the capacity required.")

st.subheader("Results table")
summary = pd.DataFrame([
    {"Metric": "Daily generation", "Estimate": f"{result['daily_kwh']:.2f} kWh"},
    {"Metric": "Annual generation", "Estimate": f"{result['annual_kwh']:.2f} kWh"},
    {"Metric": "Panel count", "Estimate": str(result["panels"])},
    {"Metric": "Gross installed cost", "Estimate": f"₹{result['gross_cost']:,.0f}"},
    {"Metric": "Annual bill savings", "Estimate": f"₹{result['annual_savings']:,.0f}"},
    {"Metric": "Simple payback", "Estimate": payback_text},
])
st.dataframe(summary, use_container_width=True, hide_index=True)
st.download_button(
    "Download results as CSV",
    data=summary.to_csv(index=False).encode("utf-8"),
    file_name="solar_calculator_results.csv",
    mime="text/csv",
)
