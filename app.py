
import calendar
from datetime import date, timedelta
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from solar_calculations import estimate_solar

st.set_page_config(
    page_title="Solar Power Calculator India | Savings & Generation",
    page_icon="☀️",
    layout="wide",
)

# Professional dashboard styling
st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(180deg, #f4fbf6 0%, #f7f9fc 45%, #ffffff 100%); }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #103d2b 0%, #176b45 100%); }
   /* Fix sidebar text visibility */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #ffffff !important;
}

/* Keep input fields readable */
[data-testid="stSidebar"] input {
    color: #ffffff !important;
}

/* Help text and slider labels */
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] *,
[data-testid="stSidebar"] [data-testid="stSlider"] * {
    color: #ffffff !important;
}
    [data-testid="stMetric"] {
        background: #ffffff; border: 1px solid #e0eee5; padding: 16px 18px;
        border-radius: 14px; box-shadow: 0 4px 14px rgba(18, 67, 43, 0.06);
    }
    [data-testid="stMetricLabel"] { color: #52665b; font-weight: 600; }
    [data-testid="stMetricValue"] { color: #176b45; font-weight: 750; }
    h1, h2, h3 {
    color: #173d2b !important;
}

p, label, [data-testid="stMarkdownContainer"] {
    color: #263b30 !important;
}

[data-testid="stMetric"] {
    min-width: 0;
    overflow-wrap: anywhere;
    padding: 12px;
    background: #ffffff;
    border: 1px solid #d5e7db;
    border-radius: 14px;
}

[data-testid="stMetricLabel"] {
    color: #40594a !important;
}

[data-testid="stMetricValue"] {
    color: #176b45 !important;
    font-size: clamp(1rem, 2vw, 1.8rem) !important;
}
    .dashboard-subtitle { color: #607368; font-size: 1.05rem; margin-top: -0.6rem; margin-bottom: 1.2rem; }

.hero-banner {
    background: linear-gradient(120deg, #103d2b, #198754);
    color: #ffffff;
    padding: clamp(24px, 5vw, 48px);
    border-radius: 22px;
    margin: 18px 0 26px 0;
    box-shadow: 0 10px 28px rgba(16, 61, 43, 0.16);
}

.hero-banner h1 {
    color: #ffffff !important;
    font-size: clamp(1.8rem, 4vw, 3rem);
    line-height: 1.15;
    margin: 12px 0;
}

.hero-banner p {
    color: #f0fff5 !important;
    font-size: clamp(1rem, 2vw, 1.15rem);
    max-width: 720px;
    line-height: 1.7;
}

.hero-tag {
    color: #d7ffe5;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 2px;
}

.hero-note {
    color: #ffffff;
    font-size: 0.95rem;
    margin-top: 22px;
    line-height: 2;
}

@media (max-width: 640px) {
    .hero-banner {
        padding: 22px 18px;
        border-radius: 16px;
        margin-top: 12px;
    }

    .hero-tag {
        letter-spacing: 1px;
        font-size: 0.7rem;
    }

    [data-testid="stMetric"] {
        padding: 10px;
        border-radius: 10px;
    }
}

/* Improve navigation button contrast */
.stApp [data-testid="stButton"] > button {
    background-color: #176b45 !important;
    color: #ffffff !important;
    border: 1px solid #176b45 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    min-height: 44px;
}

.stApp [data-testid="stButton"] > button p,
.stApp [data-testid="stButton"] > button span {
    color: #ffffff !important;
}

.stApp [data-testid="stButton"] > button:hover {
    background-color: #104b31 !important;
    border-color: #104b31 !important;
    color: #ffffff !important;
}

/* Improve download button visibility */
.stApp [data-testid="stDownloadButton"] > button {
    background-color: #176b45 !important;
    color: #ffffff !important;
    border: 1px solid #176b45 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

.stApp [data-testid="stDownloadButton"] > button p,
.stApp [data-testid="stDownloadButton"] > button span {
    color: #ffffff !important;
}

.stApp [data-testid="stDownloadButton"] > button:hover {
    background-color: #104b31 !important;
    color: #ffffff !important;
}

    </style>
    """,
    unsafe_allow_html=True,
)

st.title("☀️ Solar Energy — Intelligence System")

# Homepage hero section
st.markdown(
    """
    <div class="hero-banner">
        <div class="hero-tag">CLEAN ENERGY • SMART SAVINGS</div>
        <h1>Power Your Future with Solar Energy</h1>
        <p>
            Estimate solar electricity generation, understand your potential
            savings, and explore a cleaner energy future for your home.
        </p>
        <div class="hero-note">
            ☀️ Solar generation &nbsp; • &nbsp;
            ₹ Bill savings &nbsp; • &nbsp;
            🌱 Environmental impact
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="dashboard-subtitle">Solar production, financial insights, '
    'system sizing and environmental impact in one place.</div>',
    unsafe_allow_html=True,
)

# Website features section

# Quick navigation
st.markdown("### Explore the calculator")

nav1, nav2, nav3 = st.columns(3)

with nav1:
    if st.button("☀️ Solar Overview", use_container_width=True):
        st.session_state["show_solar_tip"] = True

with nav2:
    if st.button("💰 Savings Guide", use_container_width=True):
        st.session_state["show_savings_tip"] = True

with nav3:
    if st.button("📊 How It Works", use_container_width=True):
        st.session_state["show_method_tip"] = True

if st.session_state.get("show_solar_tip", False):
    st.info(
        "Choose your location and solar system settings in the sidebar "
        "to estimate electricity generation."
    )

if st.session_state.get("show_savings_tip", False):
    st.info(
        "Enter your monthly bill and electricity tariff in the sidebar "
        "to estimate potential savings."
    )

if st.session_state.get("show_method_tip", False):
    st.info(
        "The calculator uses historical solar-radiation data when available. "
        "Actual output depends on weather, shading, panel orientation and losses."
    )

st.markdown("## What you can calculate")

feature1, feature2, feature3 = st.columns(3)

with feature1:
    st.markdown("### ☀️ Solar Generation")
    st.write(
        "Estimate daily, monthly and yearly solar electricity "
        "generation using historical solar-radiation data."
    )

with feature2:
    st.markdown("### 💰 Electricity Savings")
    st.write(
        "Estimate monthly bill savings, annual savings and "
        "the remaining electricity bill."
    )

with feature3:
    st.markdown("### 📄 Solar Reports")
    st.write(
        "Explore your solar estimates and use the available "
        "report download options."
    )

st.divider()

# Approximate coordinates for supported locations.
LOCATIONS = {
    "Jaipur, Rajasthan": (26.9124, 75.7873),
    "Delhi, India": (28.6139, 77.2090),
    "Mumbai, Maharashtra": (19.0760, 72.8777),
    "Ahmedabad, Gujarat": (23.0225, 72.5714),
    "Jodhpur, Rajasthan": (26.2389, 73.0243),
    "Bengaluru, Karnataka": (12.9716, 77.5946),
    "Hyderabad, Telangana": (17.3850, 78.4867),
    "Chennai, Tamil Nadu": (13.0827, 80.2707),
    "Kolkata, West Bengal": (22.5726, 88.3639),
    "Lucknow, Uttar Pradesh": (26.8467, 80.9462),
}

with st.sidebar:
    st.header("Location and solar system")

    location = st.selectbox(
        "Select your location",
        list(LOCATIONS.keys()),
    )

    st.caption(
        "Location is used to request historical solar-radiation data. "
        "If the data service is unavailable, enter your own sun-hours estimate."
    )

    capacity_kw = st.number_input(
        "System capacity (kW)",
        min_value=0.5,
        max_value=1000.0,
        value=3.0,
        step=0.5,
    )

    panel_w = st.number_input(
        "Panel rating (W)",
        min_value=100,
        max_value=800,
        value=500,
        step=25,
    )

    fallback_sun_hours = st.number_input(
        "Fallback peak sun hours/day",
        min_value=0.5,
        max_value=10.0,
        value=5.0,
        step=0.25,
        help="Used only if historical radiation data cannot be retrieved.",
    )

    performance_ratio = st.slider(
        "System performance ratio",
        min_value=0.50,
        max_value=0.95,
        value=0.80,
        step=0.01,
    )

    daily_load = st.number_input(
        "Daily electricity use (kWh)",
        min_value=0.0,
        value=10.0,
        step=1.0,
    )

    monthly_bill = st.number_input(
        "Current monthly electricity bill (₹)",
        min_value=0.0,
        value=2400.0,
        step=100.0,
    )

    cost_per_kw = st.number_input(
        "Installed cost (₹ per kW)",
        min_value=0,
        value=60000,
        step=5000,
    )

    tariff = st.number_input(
        "Electricity tariff (₹/kWh)",
        min_value=0.0,
        value=8.0,
        step=0.5,
    )

    solar_offset = st.slider(
        "Share of generation that offsets your bill (%)",
        min_value=0,
        max_value=100,
        value=80,
    )

    annual_maintenance = st.number_input(
        "Annual maintenance estimate (₹)",
        min_value=0,
        value=1500,
        step=500,
    )


@st.cache_data(ttl=86400, show_spinner=False)
def fetch_solar_radiation(latitude, longitude):
    """Fetch approximately one year of historical daily solar radiation."""

    end_date = date.today() - timedelta(days=6)
    start_date = end_date - timedelta(days=364)

    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "daily": "shortwave_radiation_sum",
        "timezone": "auto",
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()
    payload = response.json()

    daily_data = payload.get("daily", {})
    dates = daily_data.get("time", [])
    radiation = daily_data.get("shortwave_radiation_sum", [])

    if not dates or not radiation or len(dates) != len(radiation):
        raise ValueError("No usable solar-radiation data was returned.")

    frame = pd.DataFrame({
        "date": pd.to_datetime(dates),
        "radiation_mj_m2": radiation,
    })

    frame["radiation_mj_m2"] = pd.to_numeric(
        frame["radiation_mj_m2"], errors="coerce"
    )
    frame = frame.dropna()

    if frame.empty:
        raise ValueError("Historical radiation data was empty.")

    # 1 kWh/m² = 3.6 MJ/m².
    # Daily irradiation in kWh/m² is used as equivalent peak sun hours.
    frame["peak_sun_hours"] = frame["radiation_mj_m2"] / 3.6
    frame["month"] = frame["date"].dt.month

    monthly_sun = frame.groupby("month")["peak_sun_hours"].mean()
    average_sun = float(frame["peak_sun_hours"].mean())

    return monthly_sun.to_dict(), average_sun, start_date.isoformat(), end_date.isoformat()


latitude, longitude = LOCATIONS[location]

try:
    with st.spinner("Loading historical solar-radiation data..."):
        monthly_sun, sun_hours, data_start, data_end = fetch_solar_radiation(
            latitude, longitude
        )

    data_source = (
        "Open-Meteo Historical Weather API — daily shortwave solar radiation"
    )
    st.success(f"Historical solar-radiation data loaded for {location}.")

except (requests.RequestException, ValueError, KeyError, TypeError) as exc:
    monthly_sun = {}
    sun_hours = float(fallback_sun_hours)
    data_start = None
    data_end = None
    data_source = "Manual fallback peak-sun-hours estimate"

    st.warning(
        "Historical data could not be loaded. The calculator is using your "
        "manual fallback sun-hours value instead. Check your internet "
        "connection and try again later."
    )

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

# Use historical monthly radiation when available; otherwise use a constant
# daily estimate. Missing months use the annual average sun-hours estimate.
months = list(calendar.month_abbr)[1:]
monthly_values = []

for month_number in range(1, 13):
    month_sun = float(monthly_sun.get(month_number, sun_hours))
    days = calendar.monthrange(date.today().year, month_number)[1]
    generation = capacity_kw * month_sun * performance_ratio * days
    monthly_values.append(generation)

monthly = pd.DataFrame({
    "Month": months,
    "Estimated generation (kWh)": monthly_values,
})

monthly_generation = float(monthly["Estimated generation (kWh)"].sum())
annual_generation = monthly_generation
average_daily_generation = annual_generation / 365

# Recalculate annual bill savings using the seasonal generation estimate.
annual_offset_kwh = annual_generation * solar_offset / 100
annual_savings = annual_offset_kwh * tariff
net_annual_benefit = annual_savings - annual_maintenance
payback_years = (
    result["gross_cost"] / net_annual_benefit
    if net_annual_benefit > 0
    else None
)

# Approximate generation for the next 30 days using the current month.
current_month_sun = float(monthly_sun.get(date.today().month, sun_hours))
current_month_daily_kwh = (
    capacity_kw * current_month_sun * performance_ratio
)
estimated_monthly_bill_savings = (
    current_month_daily_kwh * 30 * solar_offset / 100 * tariff
)
# Compare estimated solar savings with the current electricity bill.
estimated_monthly_bill_savings = min(
    monthly_bill,
    estimated_monthly_bill_savings,
)

estimated_remaining_bill = max(
    0.0,
    monthly_bill - estimated_monthly_bill_savings,
)

estimated_bill_reduction_percent = (
    estimated_monthly_bill_savings / monthly_bill * 100
    if monthly_bill > 0
    else 0.0
)
st.subheader("At-a-glance performance")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Average daily generation", f"{average_daily_generation:,.1f} kWh")
c2.metric("Average monthly generation", f"{annual_generation / 12:,.0f} kWh")
c3.metric("Annual generation", f"{annual_generation:,.0f} kWh")
c4.metric("Estimated panel count", f"{result['panels']}")

c5, c6, c7 = st.columns(3)
c5.metric("Estimated system cost", f"₹{result['gross_cost']:,.0f}")
c6.metric("Annual bill savings", f"₹{annual_savings:,.0f}")
c7.metric(
    "Simple payback",
    f"{payback_years:.1f} years" if payback_years is not None else "Not calculated",
)

st.caption(
    f"Location: {location} | Coordinates: {latitude:.4f}, {longitude:.4f}"
)
st.caption(f"Data source: {data_source}")
st.divider()
st.subheader("💡 Monthly Electricity Bill Savings")

bill_col1, bill_col2, bill_col3 = st.columns(3)

bill_col1.metric(
    "Current Monthly Bill",
    f"₹{monthly_bill:,.0f}",
)

bill_col2.metric(
    "Estimated Monthly Savings",
    f"₹{estimated_monthly_bill_savings:,.0f}",
    f"{estimated_bill_reduction_percent:.1f}% reduction",
)

bill_col3.metric(
    "Estimated Remaining Bill",
    f"₹{estimated_remaining_bill:,.0f}",
)

st.caption(
    "These are estimates. Actual savings depend on solar generation, "
    "electricity tariff, billing rules, and how much solar energy you use."
)
if data_start and data_end:
    st.caption(
        f"Historical data period: {data_start} to {data_end}. "
        "Historical weather is not a forecast of future generation."
    )

st.divider()
st.subheader("Financial overview: subsidy and installation cost")

subsidy_amount = st.number_input(
    "Enter subsidy amount (₹)",
    min_value=0.0,
    max_value=float(result["gross_cost"]),
    value=0.0,
    step=5000.0,
    help="Enter the subsidy amount you expect. Approval and eligibility are not guaranteed."
)

gross_cost = float(result["gross_cost"])
final_cost = max(0.0, gross_cost - subsidy_amount)

st.metric("Installation cost before subsidy", f"₹{gross_cost:,.0f}")
st.metric("Subsidy entered", f"₹{subsidy_amount:,.0f}")
st.metric("Final installation cost", f"₹{final_cost:,.0f}")

subsidized_payback = None

if net_annual_benefit > 0:
    subsidized_payback = final_cost / net_annual_benefit
    st.metric(
        "Estimated payback after subsidy",
        f"{subsidized_payback:.1f} years"
    )
else:
    st.metric("Estimated payback after subsidy", "Not calculated")


st.caption(
    "Subsidy is user-entered and is not a confirmation of government "
    "eligibility or approval. Actual savings and payback may vary."
)

st.divider()
st.subheader("Environmental impact")

# Editable estimate of grid emissions in India
grid_emission_factor = st.number_input(
    "Grid emission factor (kg CO2/kWh)",
    min_value=0.0,
    max_value=2.0,
    value=0.710,
    step=0.010,
    format="%.3f",
    help="Default: India's 2024-25 weighted-average grid factor. "
         "Change this value if you have a more suitable factor."
)

# Use the existing annual solar generation estimate
annual_generation_kwh = float(annual_generation)
co2_avoided_kg = annual_generation_kwh * grid_emission_factor
co2_avoided_tonnes = co2_avoided_kg / 1000

# Simple 25-year estimate, assuming constant generation and emissions factor
lifetime_co2_tonnes = co2_avoided_tonnes * 25

col1, col2 = st.columns(2)

col1.metric(
    "Annual solar generation",
    f"{annual_generation_kwh:,.0f} kWh"
)

col2.metric(
    "Estimated CO2 avoided per year",
    f"{co2_avoided_tonnes:,.2f} tonnes"
)

st.metric(
    "Estimated CO2 avoided over 25 years",
    f"{lifetime_co2_tonnes:,.2f} tonnes"
)

st.caption(
    "Environmental figures are estimates, not measured emissions "
    "reductions. The 25-year estimate assumes constant annual "
    "generation and grid emissions factor; actual results may vary."
)

st.info(
    f"Approximate next-30-day bill savings: ₹{estimated_monthly_bill_savings:,.0f}. "
    "Actual savings depend on your billing rules, self-consumption, exports, "
    "and fixed charges."
)

st.subheader("Monthly solar generation")

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(monthly["Month"], monthly["Estimated generation (kWh)"])
ax.set_ylabel("Energy (kWh)")
ax.set_xlabel("Month")
ax.set_title(f"Estimated monthly generation — {location}")
ax.grid(axis="y", alpha=0.25)
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.subheader("Generation analytics")
chart_tab_daily, chart_tab_monthly, chart_tab_yearly = st.tabs(
    ["Daily estimate", "Monthly trend", "Annual overview"]
)

# Daily estimates are modelled from each month's average historical radiation.
# They are estimates, not measured day-by-day future production.
daily_rows = []
current_year = date.today().year
for month_number in range(1, 13):
    month_sun = float(monthly_sun.get(month_number, sun_hours))
    number_of_days = calendar.monthrange(current_year, month_number)[1]
    daily_kwh = capacity_kw * month_sun * performance_ratio
    for day_number in range(1, number_of_days + 1):
        daily_rows.append({
            "Date": date(current_year, month_number, day_number),
            "Estimated generation (kWh)": daily_kwh,
        })
daily_estimates = pd.DataFrame(daily_rows)

with chart_tab_daily:
    st.caption(
        "Modelled daily estimates use each month's average solar radiation; "
        "they are not actual measurements or a weather forecast."
    )
    st.line_chart(daily_estimates.set_index("Date"), y="Estimated generation (kWh)")

with chart_tab_monthly:
    st.bar_chart(monthly.set_index("Month"), y="Estimated generation (kWh)")
    st.caption(
        f"Estimated annual production from the monthly model: "
        f"{annual_generation:,.0f} kWh."
    )

with chart_tab_yearly:
    annual_overview = pd.DataFrame({
        "Metric": ["Daily average", "Monthly average", "Annual total"],
        "Generation (kWh)": [
            average_daily_generation,
            annual_generation / 12,
            annual_generation,
        ],
    })
    st.bar_chart(annual_overview, x="Metric", y="Generation (kWh)")
    st.dataframe(annual_overview, hide_index=True, width="stretch")
    st.caption(
        "The yearly view summarizes this modelled year. The app does not "
        "have multiple years of actual solar-production measurements."
    )

st.divider()
st.subheader("System sizing check")

if daily_load > 0 and sun_hours > 0 and performance_ratio > 0:
    required_kw = daily_load / (sun_hours * performance_ratio)
    st.write(
        f"Approximate PV capacity to generate your daily usage: "
        f"**{required_kw:.2f} kW**."
    )
    st.write(f"Selected system capacity: **{capacity_kw:.2f} kW**.")
else:
    st.write("Enter a daily electricity use above zero to estimate capacity.")

st.subheader("Results table")


summary = pd.DataFrame([
    {"Metric": "Location", "Estimate": location},
    {"Metric": "Average daily generation", "Estimate": f"{average_daily_generation:.2f} kWh"},
    {"Metric": "Estimated annual generation", "Estimate": f"{annual_generation:.2f} kWh"},
    {"Metric": "Panel count", "Estimate": str(result["panels"])},
    {"Metric": "Gross installed cost", "Estimate": f"₹{gross_cost:,.0f}"},
    {"Metric": "Subsidy entered", "Estimate": f"₹{subsidy_amount:,.0f}"},
    {"Metric": "Final installation cost", "Estimate": f"₹{final_cost:,.0f}"},
    {"Metric": "Current monthly bill", "Estimate": f"₹{monthly_bill:,.0f}"},
    {"Metric": "Estimated annual bill savings", "Estimate": f"₹{annual_savings:,.0f}"},
    {"Metric": "Annual maintenance", "Estimate": f"₹{annual_maintenance:,.0f}"},
    {"Metric": "Simple payback before subsidy", "Estimate": f"{payback_years:.1f} years" if payback_years is not None else "Not calculated"},
    {"Metric": "Estimated payback after subsidy", "Estimate": f"{subsidized_payback:.1f} years" if subsidized_payback is not None else "Not calculated"},
    {"Metric": "Grid emission factor", "Estimate": f"{grid_emission_factor:.3f} kg CO2/kWh"},
    {"Metric": "Estimated CO2 avoided per year", "Estimate": f"{co2_avoided_tonnes:.2f} tonnes"},
    {"Metric": "Estimated CO2 avoided over 25 years", "Estimate": f"{lifetime_co2_tonnes:.2f} tonnes"},
    {"Metric": "Data source", "Estimate": data_source},
])


st.dataframe(summary, width="stretch", hide_index=True)

st.download_button(
    "Download results as CSV",
    data=summary.to_csv(index=False).encode("utf-8-sig"),
    file_name="solar_calculator_results.csv",
    mime="text/csv",
)


def create_pdf_report(summary_df, monthly_df, source, selected_location):
    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    story = [
        Paragraph("Solar Power Calculator Report", styles["Title"]),
        Spacer(1, 12),
        Paragraph(f"Location: {selected_location}", styles["Normal"]),
        Paragraph(f"Report date: {date.today().isoformat()}", styles["Normal"]),
        Paragraph(f"Data source: {source}", styles["Normal"]),
        Spacer(1, 16),
        Paragraph("System and financial estimates", styles["Heading2"]),
    ]

    table_data = [["Metric", "Estimate"]]
    table_data.extend(summary_df.values.tolist())

    table = Table(table_data, colWidths=[220, 260], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#176B45")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(table)
    story.append(Spacer(1, 18))
    story.append(Paragraph("Monthly generation estimate", styles["Heading2"]))

    monthly_data = [["Month", "Estimated generation (kWh)"]]
    for _, row in monthly_df.iterrows():
        monthly_data.append([
            str(row["Month"]),
            f"{row['Estimated generation (kWh)']:,.1f}",
        ])

    monthly_table = Table(monthly_data, colWidths=[150, 220], repeatRows=1)
    monthly_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#176B45")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(monthly_table)
    story.append(Spacer(1, 18))
    story.append(Paragraph(
        "Important assumptions: This report provides planning estimates, not "
        "a professional site survey or guaranteed production. Results depend "
        "on weather, shading, roof orientation, system losses, equipment, "
        "electricity tariffs, self-consumption, and applicable export rules. "
        "Historical solar radiation does not guarantee future output.",
        styles["BodyText"],
    ))

    document.build(story)
    buffer.seek(0)
    return buffer.getvalue()


try:
    pdf_bytes = create_pdf_report(summary, monthly, data_source, location)
    st.download_button(
        "Download solar report as PDF",
        data=pdf_bytes,
        file_name="solar_power_report.pdf",
        mime="application/pdf",
    )
except Exception as exc:
    st.error("PDF report could not be created. Check the app logs for details.")

st.subheader("Data sources and assumptions")
st.markdown(
    """
- **Historical solar radiation:** Open-Meteo Historical Weather API,
  when available. Its radiation data is converted from MJ/m² to kWh/m².
- **Fallback:** If the API is unavailable, the app uses the manually entered
  peak-sun-hours value and a constant daily estimate.
- **Performance ratio:** A user-selected allowance for system losses.
- **Savings:** Estimated offset energy multiplied by the entered tariff.
- **Payback:** Installed cost divided by annual savings after maintenance.
- **Not included:** Detailed rooftop shading, inverter modelling, panel
  degradation, financing, subsidies, taxes, fixed bill charges, or utility
  export-credit calculations.
"""
)
st.caption(
    "Historical data source: https://open-meteo.com/ | "
    "API documentation: https://open-meteo.com/en/docs/historical-weather-api"
)
