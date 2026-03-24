# Name:Dellanely Sebastian
# Student ID: U0000023511
# I used the AI assistant to help me make sure I didn't submit my API key that was stored in my secret toml file.
# I also used it to make sure I had no typos and my syntax was correct.

import streamlit as st
import requests
import pandas as pd

# API Integration & Caching
@st.cache_data(ttl=300)  # Caches data for 5 minutes
def fetch_weather(city):
    # Access API Key securely from secrets, not commited to GitHub
    api_key = st.secrets["OPENWEATHER_API_KEY"]
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=imperial"

    try:
        response = requests.get(url)
        # If the API failes
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

# The weather dashboard
st.title("Weather Forecast Dashboard")

# Widgets, the City and Forecast table
with st.sidebar:
    st.header("Dashboard Inputs")
    # Text input for city name, allows us to change the city whenever
    city_input = st.text_input("Enter City Name", value="Orlando")
    # Check box, it allows us to add the Forecast Table
    show_raw = st.checkbox("Show Forecast Table")

# Fetches the data
data = fetch_weather(city_input)

if data:
    # 3. pandas Data Processing
    # Parse the 'list' from the JSON response
    forecast_list = data['list']

    # Flatten the nested JSON into a clean list of dictionaries
    processed_records = []
    for item in forecast_list:
        processed_records.append({
            'Time': item['dt_txt'],
            'Temp': item['main']['temp'],
            'Humidity': item['main']['humidity'],
            'Description': item['weather'][0]['description'].capitalize()
        })

    # Allows us to convert to a Data Frame
    df = pd.DataFrame(processed_records)

    # Converts 'Time' to datetime objects for proper charting
    df['Time'] = pd.to_datetime(df['Time'])

    # The dashboard components that help show the weather, time and raw data when clicked
    # Extracts the first forecast entry so it shows the current conditions
    current_temp = df.iloc[0]['Temp']
    current_hum = df.iloc[0]['Humidity']

    # Displays key weather starts at the top of the dashboard
    col1, col2 = st.columns(2)
    col1.metric(label="Current Temp", value=f"{current_temp}°F")
    col2.metric(label="Humidity", value=f"{current_hum}%")

    # The Time Series Chart
    st.subheader(f"Temperature Trend for {city_input}")
    # Display line chart with Time as the axis, works best this way
    st.line_chart(df.set_index('Time')['Temp'])

    # Shows the toggle visibility of full dataset based on the checkbox
    if show_raw:
        st.subheader("Raw Forecast Data")
        st.dataframe(df)  # Displays processed DataFrame