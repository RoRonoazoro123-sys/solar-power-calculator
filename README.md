# Solar Power Calculator

A beginner-friendly educational project built with Python and Streamlit.

## Features
- Estimate daily, monthly, and annual solar generation
- Estimate panel count
- Estimate installed cost
- Estimate annual bill savings and simple payback
- Display a monthly generation chart
- Download a summary CSV

## Run on Windows
1. Install Python from https://www.python.org/downloads/windows/
2. Extract this project ZIP.
3. Open PowerShell in the extracted `solar_power_calculator` folder.
4. (Optional) Create a virtual environment:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
5. Install packages:
   ```powershell
   python -m pip install -r requirements.txt
   ```
6. Run:
   ```powershell
   python -m streamlit run app.py
   ```

If `py` or `python` is not recognized, install Python and enable the Python PATH option, then reopen PowerShell.

## Important assumptions
- Daily generation = system capacity (kW) × peak sun hours/day × performance ratio.
- The monthly chart uses a constant daily average, so it is for demonstration only.
- Actual generation requires location-specific solar data and depends on weather, orientation, tilt, shading, equipment, and system losses.
- Bill savings depend on self-consumption, export compensation, utility tariff rules, and applicable charges.
- Costs are user-entered estimates; subsidy is not automatically applied.
- This tool is for educational estimation and is not a certified system design.
