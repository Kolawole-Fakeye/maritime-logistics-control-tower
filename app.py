import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="Maersk West Africa Control Tower", layout="wide")
st.title("🚢 Maersk West Africa Fleet Control Tower")
st.markdown("---")

DATA_PATH = "data/production_efficiency_metrics.csv"

# --- INTERNAL DATA GENERATION LAYER ---
@st.cache_data
def ensure_local_data():
    if not os.path.exists(DATA_PATH):
        np.random.seed(42)
        voyages = 150
        ports = ['Apapa', 'Tin Can Island', 'Tema', 'Luanda']
        vessels = ['Maersk Mc-Kinney Moller', 'Maersk Mc-Kinney', 'Maersk Hangzhou', 'Maersk Camacari', 'Maersk Herrera']
        
        df = pd.DataFrame({
            'voyage_id': [f"V-2026-{i:03d}" for i in range(1, voyages + 1)],
            'vessel_name': np.random.choice(vessels, voyages),
            'arrival_port': np.random.choice(ports, voyages, p=[0.4, 0.3, 0.15, 0.15]),
            'cargo_volume_teu': np.random.randint(2500, 8500, voyages)
        })
        
        df['days_in_port'] = df['arrival_port'].apply(lambda p: np.random.randint(5, 18) if p in ['Apapa', 'Tin Can Island'] else np.random.randint(2, 6))
        df['demurrage_costs_usd'] = df['days_in_port'].apply(lambda x: max(0, (x - 5) * 3500))
        df['fuel_consumed_mt'] = df['days_in_port'] * np.random.uniform(35.0, 45.0, voyages)
        df['co2_emissions_mt'] = df['fuel_consumed_mt'] * 3.114
        df['cii_rating'] = df['days_in_port'].apply(lambda d: 'A' if d<=4 else 'B' if d<=6 else 'C' if d<=9 else 'D' if d<=13 else 'E')
        
        os.makedirs('data', exist_ok=True)
        df.to_csv(DATA_PATH, index=False)

# Trigger the check to make sure the CSV exists inside the Streamlit Container
ensure_local_data()

# --- DASHBOARD VISUALIZATION LAYER ---
if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
    
    # KPI Matrix Row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Voyages Tracked", f"{len(df)}")
    col2.metric("Avg Turnaround Time", f"{df['days_in_port'].mean():.1f} Days")
    col3.metric("Total Demurrage Penalties", f"${df['demurrage_costs_usd'].sum():,.2f}")
    col4.metric("Total Carbon Footprint", f"{df['co2_emissions_mt'].sum():,.1f} MT CO2")
    
    st.markdown("---")
    
    # Analytics Charts Row (Native & Zero-Dependency)
    left, right = st.columns(2)
    
    with left:
        st.subheader("⚠️ Port Bottlenecks (Avg Days in Port)")
        port_analysis = df.groupby("arrival_port")["days_in_port"].mean()
        st.bar_chart(port_analysis)
        
    with right:
        st.subheader("💰 Financial Leakage by Vessel")
        vessel_analysis = df.groupby("vessel_name")["demurrage_costs_usd"].sum()
        st.bar_chart(vessel_analysis)
        
    st.markdown("---")
    
    # Complete Operational Telemetry Log
    st.subheader("📋 Raw Telemetry Data Stream")
    st.dataframe(df, use_container_width=True)
else:
    st.error("Telemetry data initialization failed.")
