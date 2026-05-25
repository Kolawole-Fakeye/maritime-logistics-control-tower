import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Maersk West Africa Control Tower", layout="wide")
st.title("🚢 Maersk West Africa Fleet Control Tower")
st.markdown("---")

DATA_PATH = "data/production_efficiency_metrics.csv"

if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Voyages Tracked", f"{len(df)}")
    col2.metric("Avg Turnaround Time", f"{df['days_in_port'].mean():.1f} Days")
    col3.metric("Total Demurrage Penalties", f"${df['demurrage_costs_usd'].sum():,.2f}")
    col4.metric("Total Carbon Footprint", f"{df['co2_emissions_mt'].sum():,.1f} MT CO2")
    
    st.markdown("---")
    left, right = st.columns(2)
    with left:
        st.subheader("⚠️ Port Bottlenecks (Avg Days in Port)")
        st.bar_chart(df.groupby("arrival_port")["days_in_port"].mean())
    with right:
        st.subheader("💰 Financial Leakage by Vessel")
        st.bar_chart(df.groupby("vessel_name")["demurrage_costs_usd"].sum())
        
    st.markdown("---")
    st.subheader("📋 Raw Telemetry Data Stream")
    st.dataframe(df, use_container_width=True)
else:
    st.error("Data file missing.")
