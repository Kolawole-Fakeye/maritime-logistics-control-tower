import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import os

st.set_page_config(page_title="Maersk West Africa Control Tower", layout="wide")
st.title("🚢 Maersk West Africa Fleet Control Tower")
st.markdown("---")

# Use environment variable for cloud deployment, fallback to local for development
API_BASE_URL = os.getenv("MAERSK_API_URL", "http://127.0.0.1:8000")

@st.cache_data(ttl=60)
def fetch_api_data(endpoint):
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None

# Fetch computed data from our FastAPI backend
metrics_data = fetch_api_data("/api/v1/metrics")
raw_data = fetch_api_data("/api/v1/telemetry")

if metrics_data and raw_data:
    kpis = metrics_data["kpis"]
    
    # Top Row: Operational KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Voyages Tracked", f"{kpis['total_voyages']}")
    col2.metric("Avg Turnaround Time", f"{kpis['avg_turnaround_days']:.1f} Days")
    col3.metric("Total Demurrage Penalties", f"${kpis['total_demurrage_usd']:,.2f}")
    col4.metric("Total Carbon Footprint", f"{kpis['total_co2_mt']:,.1f} MT CO2")
    
    st.markdown("---")
    
    # Middle Row: Professional Interactive Visualization Charts
    left, right = st.columns(2)
    
    with left:
        st.subheader("⚠️ Port Bottlenecks (Avg Days in Port)")
        port_df = pd.DataFrame(list(metrics_data["port_bottlenecks"].items()), columns=["Port", "Avg Days"])
        fig_port = px.bar(port_df, x="Port", y="Avg Days", text_auto='.1f', color="Avg Days",
                          color_continuous_scale="Reds")
        st.plotly_chart(fig_port, use_container_width=True)
        
    with right:
        st.subheader("💰 Financial Leakage by Vessel")
        vessel_df = pd.DataFrame(list(metrics_data["financial_leakage"].items()), columns=["Vessel", "Demurrage (USD)"])
        fig_vessel = px.bar(vessel_df, y="Vessel", x="Demurrage (USD)", orientation='h', text_auto=',.0f',
                            color="Demurrage (USD)", color_continuous_scale="Purples")
        st.plotly_chart(fig_vessel, use_container_width=True)
        
    st.markdown("---")
    
    # Bottom Row: Complete Telemetry Log
    st.subheader("📋 Raw Telemetry Data Stream")
    df_raw = pd.DataFrame(raw_data)
    st.dataframe(df_raw, use_container_width=True)

else:
    st.error("📡 Unable to connect to the Maersk API Gateway. Please verify the backend service is running.")
