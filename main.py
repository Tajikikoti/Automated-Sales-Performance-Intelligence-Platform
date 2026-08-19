
from fastapi import FastAPI
import psycopg2
import pandas as pd
import json

app = FastAPI()

# --- Health check ---
@app.get("/")
def root():
    return {"message": "Automated Sales Performance Intelligence Platform backend is running!"}

# --- KPI targets endpoint ---
@app.get("/kpi-targets")
def get_kpi_targets():
    try:
        with open("config/kpi_targets.json", "r") as f:
            targets = json.load(f)
        return targets
    except Exception as e:
        return {"error": f"Unable to load KPI targets: {str(e)}"}

# --- Sales data endpoint ---
@app.get("/sales")
def get_sales(limit: int = 10):
    try:
        conn = psycopg2.connect(
            host="localhost",       # replace with your DB host
            database="sales_db",    # replace with your DB name
            user="postgres",        # replace with your DB user
            password="yourpassword" # replace with your DB password
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM sales LIMIT %s;", (limit,))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        # Convert rows to dict for JSON response
        sales_data = []
        for row in rows:
            sales_data.append({
                "date": row[1],
                "product": row[2],
                "branch": row[3],
                "sales_rep": row[4],
                "revenue": float(row[5]),
                "quantity": row[6]
            })
        return {"sales": sales_data}
    except Exception as e:
        return {"error": f"Unable to fetch sales data: {str(e)}"}

# --- Example KPI calculation endpoint ---
@app.get("/kpi/revenue-growth")
def revenue_growth(current: float, previous: float):
    try:
        growth = ((current - previous) / previous) * 100 if previous != 0 else None
        return {"RevenueGrowth": growth}
    except Exception as e:
        return {"error": f"Unable to calculate revenue growth: {str(e)}"}
