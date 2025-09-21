from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from typing import Optional, List, Dict, Any
import json

app = FastAPI(title="Sales Data Dashboard API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable to store the loaded data
df = None

def load_data():
    """Load the cleaned sales data"""
    global df
    try:
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "sales_cleaned.csv")
        df = pd.read_csv(data_path)
        df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'])
        print(f"Data loaded successfully: {df.shape}")
    except Exception as e:
        print(f"Error loading data: {e}")
        # Create sample data if file doesn't exist
        create_sample_data()

def create_sample_data():
    """Create sample data for testing"""
    global df
    np.random.seed(42)
    n_records = 1000
    
    dates = pd.date_range(start='2020-01-01', end='2024-12-31', freq='D')
    countries = ['USA', 'Canada', 'UK', 'Germany', 'France', 'Japan', 'Australia', 'Brazil']
    product_lines = ['Classic Cars', 'Motorcycles', 'Planes', 'Ships', 'Trains', 'Trucks and Buses', 'Vintage Cars']
    statuses = ['Shipped', 'In Process', 'Cancelled', 'On Hold', 'Disputed', 'Resolved']
    
    data = {
        'ORDERNUMBER': range(10100, 10100 + n_records),
        'SALES': np.random.uniform(1000, 50000, n_records),
        'ORDERDATE': np.random.choice(dates, n_records),
        'PRODUCTLINE': np.random.choice(product_lines, n_records),
        'COUNTRY': np.random.choice(countries, n_records),
        'QUANTITYORDERED': np.random.randint(1, 50, n_records),
        'CUSTOMERNAME': [f'Customer_{i}' for i in range(n_records)],
        'STATUS': np.random.choice(statuses, n_records, p=[0.6, 0.15, 0.05, 0.05, 0.05, 0.1])
    }
    
    df = pd.DataFrame(data)
    df['YEAR'] = df['ORDERDATE'].dt.year
    df['MONTH'] = df['ORDERDATE'].dt.month
    df['QUARTER'] = df['ORDERDATE'].dt.quarter
    print(f"Sample data created: {df.shape}")

# Load data on startup
@app.on_event("startup")
async def startup_event():
    load_data()

@app.get("/")
def root():
    return {"message": "Sales Data Dashboard API", "status": "OK", "endpoints": [
        "/sales_over_time",
        "/sales_by_category", 
        "/sales_by_country",
        "/top_customers",
        "/kpis",
        "/order_status"
    ]}

@app.get("/sales_over_time")
def sales_over_time(period: str = "month", year: Optional[int] = None):
    """Get sales data over time by day/month/year"""
    if df is None:
        raise HTTPException(status_code=500, detail="Data not loaded")
    
    data = df.copy()
    
    if year:
        data = data[data['YEAR'] == year]
    
    if period == "day":
        grouped = data.groupby('ORDERDATE')['SALES'].sum().reset_index()
        grouped['date'] = grouped['ORDERDATE'].dt.strftime('%Y-%m-%d')
    elif period == "month":
        grouped = data.groupby(['YEAR', 'MONTH'])['SALES'].sum().reset_index()
        grouped['date'] = grouped['YEAR'].astype(str) + '-' + grouped['MONTH'].astype(str).str.zfill(2)
    elif period == "year":
        grouped = data.groupby('YEAR')['SALES'].sum().reset_index()
        grouped['date'] = grouped['YEAR'].astype(str)
    else:
        raise HTTPException(status_code=400, detail="Period must be 'day', 'month', or 'year'")
    
    return {
        "period": period,
        "year": year,
        "data": grouped[['date', 'SALES']].to_dict('records')
    }

@app.get("/sales_by_category")
def sales_by_category():
    """Get sales data by product line"""
    if df is None:
        raise HTTPException(status_code=500, detail="Data not loaded")
    
    category_sales = df.groupby('PRODUCTLINE')['SALES'].sum().reset_index()
    category_sales = category_sales.sort_values('SALES', ascending=False)
    
    return {
        "data": category_sales.to_dict('records')
    }

@app.get("/sales_by_country")
def sales_by_country(limit: int = 10):
    """Get sales data by country"""
    if df is None:
        raise HTTPException(status_code=500, detail="Data not loaded")
    
    country_sales = df.groupby('COUNTRY')['SALES'].sum().reset_index()
    country_sales = country_sales.sort_values('SALES', ascending=False).head(limit)
    
    return {
        "limit": limit,
        "data": country_sales.to_dict('records')
    }

@app.get("/top_customers")
def top_customers(limit: int = 10):
    """Get top customers by sales"""
    if df is None:
        raise HTTPException(status_code=500, detail="Data not loaded")
    
    customer_sales = df.groupby('CUSTOMERNAME').agg({
        'SALES': 'sum',
        'ORDERNUMBER': 'count',
        'QUANTITYORDERED': 'sum'
    }).reset_index()
    
    customer_sales.columns = ['customer', 'total_sales', 'order_count', 'total_quantity']
    customer_sales = customer_sales.sort_values('total_sales', ascending=False).head(limit)
    
    return {
        "limit": limit,
        "data": customer_sales.to_dict('records')
    }

@app.get("/kpis")
def get_kpis():
    """Get key performance indicators"""
    if df is None:
        raise HTTPException(status_code=500, detail="Data not loaded")
    
    total_sales = df['SALES'].sum()
    total_orders = df['ORDERNUMBER'].nunique()
    total_quantity = df['QUANTITYORDERED'].sum()
    avg_order_value = df['SALES'].mean()
    
    # Year over year growth
    current_year = df['YEAR'].max()
    previous_year = current_year - 1
    
    current_year_sales = df[df['YEAR'] == current_year]['SALES'].sum()
    previous_year_sales = df[df['YEAR'] == previous_year]['SALES'].sum()
    
    yoy_growth = ((current_year_sales - previous_year_sales) / previous_year_sales * 100) if previous_year_sales > 0 else 0
    
    return {
        "total_sales": round(float(total_sales), 2),
        "total_orders": int(total_orders),
        "total_quantity": int(total_quantity),
        "avg_order_value": round(float(avg_order_value), 2),
        "yoy_growth": round(float(yoy_growth), 2),
        "current_year": int(current_year),
        "previous_year": int(previous_year)
    }

@app.get("/order_status")
def order_status():
    """Get order counts by status"""
    if df is None:
        raise HTTPException(status_code=500, detail="Data not loaded")
    
    status_counts = df['STATUS'].value_counts().reset_index()
    status_counts.columns = ['status', 'count']
    
    return {
        "data": status_counts.to_dict('records')
    }

@app.get("/data_summary")
def data_summary():
    """Get overall data summary"""
    if df is None:
        raise HTTPException(status_code=500, detail="Data not loaded")
    
    return {
        "total_records": int(len(df)),
        "date_range": {
            "start": df['ORDERDATE'].min().strftime('%Y-%m-%d'),
            "end": df['ORDERDATE'].max().strftime('%Y-%m-%d')
        },
        "unique_customers": int(df['CUSTOMERNAME'].nunique()),
        "unique_countries": int(df['COUNTRY'].nunique()),
        "unique_products": int(df['PRODUCTLINE'].nunique()),
        "columns": list(df.columns)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
