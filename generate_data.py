from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

app = FastAPI(title="Maersk West Africa API Gateway", version="1.0.0")

# Enable cross-origin requests so your frontend can read the data securely
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
    
    # Calculate operational metrics safely
    total_voyages = len(df)
    avg_turnaround = float(df['days_in_port'].mean()) if 'days_in_port' in df.columns else 0.0
    total_demurrage = float(df['demurrage_costs_usd'].sum()) if 'demurrage_costs_usd' in df.columns else 0.0
    total_carbon = float(df['co2_emissions_mt'].sum()) if 'co2_emissions_mt' in df.columns else 0.0
    
    # Port Bottleneck aggregation
    port_bottlenecks = df.groupby("arrival_port")["days_in_port"].mean().round(2).to_dict()
    
    # Financial Leakage aggregation
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
