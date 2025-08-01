# 🌫️ Beijing PM2.5 Air Quality Prediction App

**Predict PM2.5 pollution levels in Beijing using machine learning and meteorological data.**

This **web application** allows users to **predict the concentration** of **PM2.5 particulate matter in Beijing's air** based on **weather conditions** and **historical pollution data**. Built with `Streamlit` and a **pre-trained machine learning model**, it provides **real-time, interactive forecasts** with intuitive color-coded results indicating **air quality levels**.


## Streamlit web app

| Streamlit web app                          |
| ------------------------------------------ |
| ![streamlit](images/streamlit.jpg)         |


## 📌Features
- Input precise **date** and **time **for accurate timestamping of predictions
- Enter **meteorological parameters**: temperature, dew point, pressure, wind direction & speed, solar radiation
- Include **historical PM2.5 measurements** (lag features and moving averages)
- **Dynamic prediction** with clear, color-coded air quality levels and health advice
- Expandable sections with **detailed input parameters** and **app info**
- Responsive, user-friendly interface with custom styling and helpful tooltips


## 🛠️ Installation & Run

1. Clone this repository:
```bash
git clone https://github.com/antoningr/PM2.5_Air_Quality_Predictor.git
```

2. Change directory:
```bash
cd PM2.5_Air_Quality_Predictor
```

3. Install required packages: dependencies:
```bash
pip install -r requirements.txt
```

4. Run the web app:
```bash
streamlit run app.py
```

Open your browser at [http://localhost:8501](http://localhost:8501) and use the sidebar to input weather and pollution data. The predicted PM2.5 level will be displayed with color-coded air quality classification and health advice.


## 📁 Dataset

We use the [Beijing PM2.5](https://archive.ics.uci.edu/dataset/381/beijing+pm2+5+data) dataset.
This hourly data set contains the **PM2.5 data of US Embassy in Beijing**. Meanwhile, meteorological data from Beijing Capital International Airport are also included.

- Dataset Characteristics: Multivariate, Time-Series
- Subject Area: Climate and Environment
- Associated Tasks: Regression
- Feature Type: Integer, Real
- Instances: 43824
- Features: 11

Dataset Information
- Additional Information : The data's time period is between Jan 1st, 2010 to Dec 31st, 2014. Missing data are denoted as "NA".
- Has Missing Values? Yes 


## 🌫️ Air Quality Categories

| PM2.5 Level (μg/m³) | Category                       | Advice                                                          |
| ------------------- | ------------------------------ | --------------------------------------------------------------- |
| 0 - 50              | Good                           | Air quality is satisfactory.                                    |
| 51 - 100            | Moderate                       | Acceptable, sensitive groups should reduce outdoor activity.    |
| 101 - 150           | Unhealthy for Sensitive Groups | Sensitive groups may experience health effects.                 |
| 151 - 200           | Unhealthy                      | Everyone may experience health effects; limit outdoor exertion. |
| 201 - 300           | Very Unhealthy                 | Health warnings of emergency conditions.                        |
| 301+                | Hazardous                      | Serious health effects; avoid outdoor exposure.                 |


## 📘 Language

- Python