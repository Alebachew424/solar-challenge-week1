import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Title and intro
st.set_page_config(page_title="Solar Data Dashboard", layout="wide")
st.title("🔆 Solar Data Discovery Dashboard")
st.markdown("Visualize and compare solar data from **Benin**, **Sierra Leone**, and **Togo**.")

# Helper to load data
@st.cache_data
def load_data(country_file):
    return pd.read_csv(os.path.join("data", country_file))

# Country selection
country_map = {
    "Benin": "benin_clean.csv",
    "Sierra Leone": "sierra_leone_clean.csv",
    "Togo": "togo_clean.csv"
}
selected_country = st.sidebar.selectbox("Select Country", list(country_map.keys()))
df = load_data(country_map[selected_country])

# Preview
st.subheader(f"📊 Preview of {selected_country} Data")
st.dataframe(df.head(50), use_container_width=True)

# Line plot: GHI, DNI, DHI
st.subheader("☀️ Solar Irradiance Over Time")
if "Timestamp" in df.columns:
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    fig_irradiance = px.line(df, x="Timestamp", y=["GHI", "DNI", "DHI"],
                             labels={"value": "Irradiance (W/m²)", "Timestamp": "Date"},
                             title="GHI, DNI, DHI Over Time")
    st.plotly_chart(fig_irradiance, use_container_width=True)
else:
    st.warning("Timestamp column not found in data.")

# Histogram of GHI
st.subheader("📈 Distribution of GHI")
fig_hist = px.histogram(df, x="GHI", nbins=50, title="Global Horizontal Irradiance (GHI) Histogram")
st.plotly_chart(fig_hist, use_container_width=True)

# Scatter: GHI vs Tamb with RH as bubble size
if all(col in df.columns for col in ["GHI", "Tamb", "RH"]):
    st.subheader("🌡️ GHI vs Temperature with Humidity Bubble")
    fig_bubble = px.scatter(df, x="Tamb", y="GHI", size="RH", color="RH",
                            title="GHI vs Ambient Temperature (Bubble = Humidity)",
                            labels={"Tamb": "Ambient Temp (°C)", "GHI": "GHI (W/m²)", "RH": "Humidity (%)"})
    st.plotly_chart(fig_bubble, use_container_width=True)

# Correlation Heatmap (Optional toggle)
if st.checkbox("Show Correlation Heatmap"):
    import seaborn as sns
    import matplotlib.pyplot as plt
    import numpy as np

    numeric_df = df.select_dtypes(include="number")
    corr = numeric_df.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", mask=mask, fmt=".2f")
    st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("Developed for the 10x Academy Solar Challenge - Week 0")
