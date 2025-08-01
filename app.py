# app.py
import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
from datetime import datetime

# Load trained model
model_path = Path("models/best_model.pkl")
model = joblib.load(model_path)

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Beijing PM2.5 Air Quality Predictor",
    page_icon="🌫️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR STYLE ---
st.markdown("""
<style>
/* Background gradient */
body {
    background: linear-gradient(135deg, #f0f4f8, #d9e2ec);
}

/* Title style */
h1 {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #023e8a;
    font-weight: 900;
    text-align: center;
}

/* Prediction result style */
.prediction {
    font-size: 2.5rem;
    font-weight: 900;
    text-align: center;
    margin-top: 1rem;
    margin-bottom: 1rem;
}

/* Sidebar logo */
.sidebar .sidebar-content {
    padding-top: 1rem;
}

/* Info box */
.info-box {
    background-color: #caf0f8;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 20px;
    font-size: 0.95rem;
    color: #03045e;
    line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("🌫️ Beijing PM2.5 Air Quality Predictor")
st.markdown("""
Welcome to the PM2.5 air quality prediction app for Beijing.  
Use the controls in the sidebar to input weather conditions and pollution history to get a prediction of the air quality.
""")

# --- SIDEBAR ---
st.sidebar.header("⚙️ Configure Inputs")

date = st.sidebar.date_input("📅 Date", datetime.today(), help="Select the date for prediction.")
time = st.sidebar.time_input("⏰ Time", datetime.now().time(), help="Select the hour of the day.")

st.sidebar.subheader("🌡️ Weather Conditions")
TEMP = st.sidebar.slider("Temperature (°C)", -20, 50, 20, help="Ambient air temperature.")
DEWP = st.sidebar.slider("Dew Point (°C)", -30, 50, 10, help="Dew point temperature.")
PRES = st.sidebar.slider("Pressure (hPa)", 800, 1100, 1013, help="Atmospheric pressure.")
cbwd = st.sidebar.selectbox("Wind Direction", ["NW", "NE", "SE", "cv"], help="Wind direction category.")
Iws = st.sidebar.slider("Wind Speed (m/s)", 0.0, 20.0, 5.0, help="Cumulative wind speed.")
Ir = st.sidebar.slider("Irradiance (W/m²)", 0, 1000, 200, help="Solar irradiance.")
Is = st.sidebar.slider("Solar Radiation (W/m²)", 0, 1000, 250, help="Solar radiation intensity.")

st.sidebar.subheader("🧪 Historical Pollution")
pm25_lag1 = st.sidebar.number_input("PM2.5 (t-1 hour)", 0, 1000, 50, help="PM2.5 concentration 1 hour ago.")
pm25_lag2 = st.sidebar.number_input("PM2.5 (t-2 hours)", 0, 1000, 45, help="PM2.5 concentration 2 hours ago.")
pm25_ma3 = st.sidebar.number_input("PM2.5 Moving Avg (3h)", 0, 1000, 48, help="3-hour moving average.")
pm25_ma6 = st.sidebar.number_input("PM2.5 Moving Avg (6h)", 0, 1000, 47, help="6-hour moving average.")
pm25_ma12 = st.sidebar.number_input("PM2.5 Moving Avg (12h)", 0, 1000, 46, help="12-hour moving average.")

# --- FEATURE ENGINEERING ---
year = date.year
month = date.month
day = date.day
hour = time.hour
dayofweek = date.weekday()
temp_iws = TEMP * Iws

input_dict = {
    "year": year,
    "month": month,
    "day": day,
    "hour": hour,
    "dayofweek": dayofweek,
    "TEMP": TEMP,
    "DEWP": DEWP,
    "PRES": PRES,
    "cbwd": cbwd,
    "Iws": Iws,
    "Ir": Ir,
    "Is": Is,
    "temp_iws": temp_iws,
    "pm2.5_lag1": pm25_lag1,
    "pm2.5_lag2": pm25_lag2,
    "pm2.5_ma3": pm25_ma3,
    "pm2.5_ma6": pm25_ma6,
    "pm2.5_ma12": pm25_ma12
}
input_df = pd.DataFrame([input_dict])

required_cols = model.feature_names_in_
missing_cols = set(required_cols) - set(input_df.columns)

st.markdown("---")
st.subheader("Air Quality Prediction:")

if missing_cols:
    st.error(f"❌ Missing columns for prediction: {missing_cols}")
else:
    input_df = input_df[required_cols]
    try:
        prediction = model.predict(input_df)[0]

        # Air quality categories + colors
        def get_quality_info(pm):
            if pm <= 50:
                return ("Good", "green", "Air quality is satisfactory.")
            elif pm <= 100:
                return ("Moderate", "yellow", "Acceptable for most, sensitive groups should reduce outdoor activities.")
            elif pm <= 150:
                return ("Unhealthy for Sensitive Groups", "orange", "Sensitive groups may experience health effects.")
            elif pm <= 200:
                return ("Unhealthy", "red", "Everyone may experience health effects; limit outdoor exertion.")
            elif pm <= 300:
                return ("Very Unhealthy", "purple", "Health warnings of emergency conditions.")
            else:
                return ("Hazardous", "maroon", "Serious health effects; everyone should avoid outdoor exposure.")

        quality, color, advice = get_quality_info(prediction)

        st.markdown(f"""
        <div class="prediction" style="color:{color};">
            <strong>PM2.5: {prediction:.2f} μg/m³ — {quality}</strong>
        </div>
        """, unsafe_allow_html=True)

        st.info(advice)

        with st.expander("📋 View Input Parameters"):
            st.dataframe(input_df.T, use_container_width=True)

    except Exception as e:
        st.error(f"⚠️ Prediction failed: {e}")

# --- ABOUT SECTION ---
with st.expander("ℹ️ About this app"):
    st.markdown("""
    This app predicts PM2.5 particulate matter concentrations in Beijing based on weather and historical pollution data.
    
    **Data and Model:**
    - The model was trained on historical Beijing air quality and meteorological data.
    - Features include temperature, pressure, wind direction and speed, solar radiation, and lagged pollution values.
    - The prediction output corresponds to μg/m³ of PM2.5, which is a key pollutant affecting respiratory health.

    **How to Interpret Results:**
    - The color-coded prediction helps quickly understand air quality risks.
    - Lower PM2.5 values indicate better air quality.
    - Follow local guidelines for outdoor activity, especially during high pollution.

    **Limitations:**
    - Predictions rely on the accuracy of inputs.
    - Sudden changes in weather or pollution sources might reduce prediction accuracy.

    Feel free to adjust parameters and explore how different conditions affect air quality!
    """)

# --- FOOTER ---
st.markdown("---")
st.markdown(
    "<center>2025 • Model trained on Beijing PM2.5 dataset</center>",
    unsafe_allow_html=True
)
