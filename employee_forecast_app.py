import streamlit as st
import pandas as pd
import numpy as np

def generate_forecast(passenger_volume, flight_schedule, labor_efficiency):
    base_staffing = passenger_volume * 0.05 + flight_schedule * 2 
    #passenger_volume * 0.05 ->
#assumes that for every passenger traveling, a certain fraction (5%) contributes to staffing needs.
#if passenger_volume = 50,000, then 50,000 * 0.05 = 2,500 staff would be needed based on passengers alone.
#flight_schedule * 2 ->
#assumes that each flight requires a fixed number of employees (2 per flight).
#if flight_schedule = 500, then 500 * 2 = 1,000 staff are needed based on the number of flights.
    adjusted_staffing = base_staffing * (1 - labor_efficiency / 100)
    return round(adjusted_staffing, 2)

st.title("Airport Labor Planning and Forecasting Tool")

st.sidebar.header("Input Parameters")
passenger_volume = st.sidebar.number_input("Passenger Volume", min_value=0, value=50000, step=1000)
flight_schedule = st.sidebar.number_input("Number of Flights", min_value=0, value=500, step=10)
labor_efficiency = st.sidebar.slider("Labor Efficiency Improvement (%)", min_value=0, max_value=50, value=10)

generated_forecast = generate_forecast(passenger_volume, flight_schedule, labor_efficiency)

st.subheader("Forecasted Staffing Levels")
st.write(f"Recommended staffing level: {generated_forecast} employees")

# Variance analysis
#actual_staffing is the real number of employees working.
#generated_forecast is the recommended number of employees based on passenger volume, flight schedule, and labor efficiency.

st.subheader("Variance Analysis")
actual_staffing = st.number_input("Actual Staffing", min_value=0, value=int(generated_forecast), step=1)
variance = actual_staffing - generated_forecast
st.write(f"Variance: {variance} employees")
if variance > 0:
    st.success("Overstaffed.")
elif variance < 0:
    st.warning("Understaffed.")
else:
    st.info("Optimal staffing level achieved.")

# Scenario Analysis
st.subheader("Scenario Analysis")
scenario_factor = st.slider("Adjust Scenario Factor (%)", min_value=-20, max_value=20, value=0)
scenario_forecast = generate_forecast(passenger_volume * (1 + scenario_factor / 100), flight_schedule, labor_efficiency)
st.write(f"Adjusted staffing recommendation under scenario: {scenario_forecast} employees")

st.markdown("### Summary Report")
report_data = {
    "Metric": ["Passenger Volume", "Flight Schedule", "Labor Efficiency", "Recommended Staffing", "Actual Staffing", "Variance"],
    "Value": [passenger_volume, flight_schedule, f"{labor_efficiency}%", generated_forecast, actual_staffing, variance]
}
st.table(pd.DataFrame(report_data))

#scenario_factor: This is a percentage slider (-20% to +20%) that modifies passenger volume to simulate different traffic conditions.
#generate_forecast(): The function recalculates staffing needs by scaling passenger volume based on the scenario factor.

#Example 1: Lower Passenger Volume (-10%)
#Suppose the current passenger volume is 50,000.
#If we reduce traffic by 10%, the new passenger volume becomes:
#50000×(1−0.10)=45000
#he forecasted staffing level adjusts accordingly
