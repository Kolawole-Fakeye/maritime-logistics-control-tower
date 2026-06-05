import streamlit as st
import pandas as pd
import requests
import os

st.set_page_config(page_title="Maersk West Africa Control Tower", layout="wide")
st.title("🚢 Maersk West Africa Fleet Control Tower")
st.markdown("---")

# Point to your live API Gateway on Render
API_BASE_URL = os.getenv("MAERSK_API_URL", "https://maersk-backend-api.onrender.com")

@st.cache_data(ttl=60)
def fetch_api_data(endpoint):
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None

# Fetch processed JSON data packages from the FastAPI backend
metrics_data = fetch_api_data("/api/v1/metrics")
raw_data = fetch_api_data("/api/v1/telemetry")

if metrics_data and raw_data:
    kpis = metrics_data["kpis"]
    
    # KPI Matrix
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Voyages Tracked", f"{kpis['total_voyages']}")
    col2.metric("Avg Turnaround Time", f"{kpis['avg_turnaround_days']:.1f} Days")
    col3.metric("Total Demurrage Penalties", f"${kpis['total_demurrage_usd']:,.2f}")
    col4.metric("Total Carbon Footprint", f"{kpis['total_co2_mt']:,.1f} MT CO2")
    
    st.markdown("---")
    
    # Layout Grid: Native Streamlit Analytics (Completely Bypasses Module Errors)
    left, right = st.columns(2)
    
    with left:
        st.subheader("⚠️ Port Bottlenecks (Avg Days in Port)")
        port_df = pd.DataFrame(list(metrics_data["port_bottlenecks"].items()), columns=["Port", "Avg Days"])
        st.bar_chart(port_df.set_index("Port"))
        
    with right:
        st.subheader("💰 Financial Leakage by Vessel")
        vessel_df = pd.DataFrame(list(metrics_data["financial_leakage"].items()), columns=["Vessel", "Demurrage (USD)"])
        st.bar_chart(vessel_df.set_index("Vessel"))
        
    st.markdown("---")
    
    # Full Operational Telemetry Display
    st.subheader("📋 Raw Telemetry Data Stream")
    df_raw = pd.DataFrame(raw_data)
    st.dataframe(df_raw, use_container_width=True)

else:
    st.error("📡 Unable to connect to the Maersk API Gateway. Please verify the backend service is running.")
