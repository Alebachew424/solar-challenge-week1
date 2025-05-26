import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set page configuration
st.set_page_config(page_title="🌞 Tenx Solar Dashboard", layout="wide")

# Title and Intro
st.title("🌞 Tenx Solar Data Discovery Dashboard")
st.markdown("""
This dashboard allows you to interactively explore solar radiation and environmental metrics 
for **Benin**, **Sierra Leone**, and **Togo** to identify the most promising regions for solar installation.
""")

# Helper function
@st.cache_data
def load_data(country_file):
    df = pd.read_csv(os.path.join("data", country_file))
    if 'Timestamp' in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    return df

# Country files map
country_map = {
    "Benin": "benin_clean.csv",
    "Sierra Leone": "sierra_leone_clean.csv",
    "Togo": "togo_clean.csv"
}

# Sidebar
st.sidebar.header("⚙️ Filters")
selected_country = st.sidebar.selectbox("Select Country", list(country_map.keys()))

# Load selected dataset
df = load_data(country_map[selected_country])

# Preview section
st.subheader(f"📊 Data Preview - {selected_country}")
st.dataframe(df.head(50), use_container_width=True)

# Section 1: Solar Irradiance Over Time
st.subheader("☀️ Solar Irradiance Over Time")
fig = px.line(df, x="Timestamp", y=["GHI", "DNI", "DHI"], title="Irradiance (GHI, DNI, DHI)")
st.plotly_chart(fig, use_container_width=True)

# Section 2: GHI Distribution
st.subheader("📈 GHI Distribution")
fig_hist = px.histogram(df, x="GHI", nbins=50, title="Distribution of GHI")
st.plotly_chart(fig_hist, use_container_width=True)

# Section 3: GHI vs Tamb with RH
if all(col in df.columns for col in ["GHI", "Tamb", "RH"]):
    st.subheader("🌡️ GHI vs Ambient Temperature (Bubble = RH)")
    fig_bubble = px.scatter(df, x="Tamb", y="GHI", size="RH", color="RH",
                            title="GHI vs Temperature Colored by RH",
                            labels={"Tamb": "Ambient Temp (°C)", "GHI": "GHI (W/m²)", "RH": "Humidity (%)"})
    st.plotly_chart(fig_bubble, use_container_width=True)

# Section 4: Cleaning Impact
if "Cleaning" in df.columns and "ModA" in df.columns and "ModB" in df.columns:
    st.subheader("🧽 Impact of Cleaning on Sensor Output")
    clean_avg = df.groupby("Cleaning")[["ModA", "ModB"]].mean().reset_index()
    fig_clean = px.bar(clean_avg, barmode="group", x="Cleaning", y=["ModA", "ModB"], 
                       title="Sensor Output Before and After Cleaning")
    st.plotly_chart(fig_clean, use_container_width=True)

# Section 5: Correlation Heatmap
if st.checkbox("Show Correlation Heatmap"):
    import seaborn as sns
    import matplotlib.pyplot as plt
    import numpy as np

    st.subheader("🔍 Correlation Heatmap")
    corr_df = df.select_dtypes(include='number')
    corr = corr_df.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", mask=mask, ax=ax)
    st.pyplot(fig)

# Section 6: Wind Speed Distribution
if "WS" in df.columns:
    st.subheader("💨 Wind Speed Distribution")
    fig_ws = px.histogram(df, x="WS", nbins=30, title="Wind Speed Distribution (m/s)")
    st.plotly_chart(fig_ws, use_container_width=True)

st.markdown("---")
st.markdown("Built for Tenx Academy Week 0 Challenge | ✨ [Streamlit Docs](https://docs.streamlit.io)")
