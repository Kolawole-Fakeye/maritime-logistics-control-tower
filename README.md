# Maersk West Africa Fleet Control Tower (SHIPPING-AFRICA)

An interactive, data-driven fleet logistics and telemetry control tower dashboard built to monitor shipping performance, quantify supply chain bottlenecks, and track financial leakages across West African ports. Built using **Streamlit** and **Pandas**, this system transforms raw fleet telemetry metrics into high-impact operational intelligence.

---

## 🚀 Key Performance Indicators (KPIs) Tracked

* **Total Voyages Tracked:** Direct volume visibility into active and completed shipping routes across the continent.
* **Avg Turnaround Time:** Monitored via the `days_in_port` metric to immediately isolate port operational inefficiencies.
* **Financial Leakage (Demurrage Penalties):** Aggregated tracking of structural delays (`demurrage_costs_usd`) to calculate bottom-line capital losses.
* **Environmental Impact Tracker:** Cumulative tracking of vessel carbon output (`co2_emissions_mt`) to support green logistics and sustainability benchmarking.

---

## 📊 Operational Analytics Visualizations

The control tower segments telemetry data into two crucial operational views:
1. **⚠️ Port Bottlenecks Matrix:** A dynamic bar chart aggregating the average number of days vessels spend idle at port (`days_in_port`), categorized by the destination terminal (`arrival_port`).
2. **💰 Financial Leakage Explorer:** An operational cost bar chart grouping total accrued demurrage penalties strictly by individual shipping craft (`vessel_name`) to isolate high-risk assets.

---

## 🛠️ Tech Stack & Architecture

* **Language:** Python 3.10+
* **Frontend UI Framework:** Streamlit (Wide-layout Interactive User Interface)
* **Data Ingestion & Analytics:** Pandas
* **Data Source:** Tabular Fleet Telemetry Stream (`data/production_efficiency_metrics.csv`)

---

## 📋 Workspace Code Architecture

```python
import streamlit as st
import pandas as pd
import os

# Configures an expansive wide-layout control viewport
st.set_page_config(page_title="Maersk West Africa Control Tower", layout="wide")
st.title("🚢 Maersk West Africa Fleet Control Tower")
