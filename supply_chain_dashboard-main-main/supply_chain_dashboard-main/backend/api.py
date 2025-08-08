from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

# Enable CORS to allow Streamlit (localhost:8501) to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the cleaned dataset
try:
    df = pd.read_csv("cleaned_supply_chain_data.csv")
except FileNotFoundError:
    df = pd.read_csv("supply_chain_data.csv")  # Fallback to original dataset

@app.get("/all_data")
async def get_all_data():
    return df.to_dict(orient="records")

@app.get("/forecast/{product_id}")
async def forecast_demand(product_id: str):
    # Placeholder: Return dummy forecast data (replace with Prophet model if available)
    forecast_data = [
        {"ds": "2025-08-08", "yhat": 100},
        {"ds": "2025-08-09", "yhat": 105},
        {"ds": "2025-08-10", "yhat": 110},
        {"ds": "2025-08-11", "yhat": 115},
        {"ds": "2025-08-12", "yhat": 120},
    ]
    return forecast_data

@app.get("/inventory_optimize/{product_id}")
async def optimize_inventory(product_id: str):
    # Filter data for the given product_id
    product_data = df[df["SKU"] == product_id]
    if product_data.empty:
        return {"error": f"Product {product_id} not found"}
    # Example reorder point calculation: lead time * avg daily sales + safety stock
    lead_time = product_data["Lead times"].iloc[0]
    sales_quantity = product_data["Number of products sold"].iloc[0]
    avg_daily_sales = sales_quantity / 30  # Assuming 30-day period
    safety_stock = 10  # Placeholder
    reorder_point = lead_time * avg_daily_sales + safety_stock
    return {
        "product_id": product_id,
        "reorder_point": round(reorder_point, 2),
        "current_stock": int(product_data["Stock levels"].iloc[0]),
        "recommended_action": "Reorder" if product_data["Stock levels"].iloc[0] < reorder_point else "Sufficient stock"
    }

@app.post("/market_analysis")
async def market_analysis(text: str):
    # Placeholder: Return dummy sentiment analysis
    # In a real implementation, use a model like TextBlob or transformers
    return {
        "sentiment": "Neutral",
        "confidence": 0.5,
        "suggested_action": "Monitor market trends"
    }