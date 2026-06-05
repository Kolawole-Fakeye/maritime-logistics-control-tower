from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import os

# =====================================================================
# 🚢 DATA GENERATION LAYER (Executes on startup so the file always exists)
# =====================================================================
def generate_fleet_data():
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
    df.to_csv('data/production_efficiency_metrics.csv', index=False)
    print("✅ CSV Fleet Telemetry Layer serialized successfully!")

# Automatically fire the generator on startup
generate_fleet_data()

# =====================================================================
# 🚀 FASTAPI GATEWAY ROUTING
# =====================================================================
app = FastAPI(title="Maersk West Africa API Gateway", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = "data/production_efficiency_metrics.csv"

def load_data():
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=404, detail="Operational telemetry data file missing.")
    return pd.read_csv(DATA_PATH)

@app.get("/")
def root():
    return {"status": "online", "system": "Maersk West Africa Fleet Control Tower API"}

@app.get("/api/v1/telemetry")
def get_telemetry():
    """Returns the full fleet telemetry dataset"""
    df = load_data()
    return df.to_dict(orient="records")

@app.get("/api/v1/metrics")
def get_aggregated_metrics():
    """Processes and returns high-level logistics KPIs"""
    df = load_data()
    
    total_voyages = len(df)
    avg_turnaround = float(df['days_in_port'].mean()) if 'days_in_port' in df.columns else 0.0
    total_demurrage = float(df['demurrage_costs_usd'].sum()) if 'demurrage_costs_usd' in df.columns else 0.0
    total_carbon = float(df['co2_emissions_mt'].sum()) if 'co2_emissions_mt' in df.columns else 0.0
    
    port_bottlenecks = df.groupby("arrival_port")["days_in_port"].mean().round(2).to_dict()
    financial_leakage = df.groupby("vessel_name")["demurrage_costs_usd"].sum().round(2).to_dict()

    return {
        "kpis": {
            "total_voyages": total_voyages,
            "avg_turnaround_days": avg_turnaround,
            "total_demurrage_usd": total_demurrage,
            "total_co2_mt": total_carbon
        },
        "port_bottlenecks": port_bottlenecks,
        "financial_leakage": financial_leakage
    }
