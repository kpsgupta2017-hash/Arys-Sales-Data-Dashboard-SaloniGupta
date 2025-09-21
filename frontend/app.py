import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import time

# Page configuration
st.set_page_config(
    page_title="Sales Data Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .stSelectbox > div > div {
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://localhost:8000"

def fetch_data(endpoint, params=None):
    """Fetch data from the API"""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from API: {e}")
        return None

def format_currency(value):
    """Format value as currency"""
    return f"${value:,.2f}"

def format_number(value):
    """Format value as number with commas"""
    return f"{value:,}"

# Main header
st.markdown('<h1 class="main-header">📊 Sales Data Dashboard</h1>', unsafe_allow_html=True)

# Sidebar for filters
st.sidebar.header("🔧 Filters & Controls")

# Check API connection
with st.spinner("Checking API connection..."):
    api_status = fetch_data("/")
    if api_status:
        st.sidebar.success("✅ API Connected")
    else:
        st.sidebar.error("❌ API Connection Failed")
        st.error("Please make sure the backend API is running on http://localhost:8000")
        st.stop()

# Sidebar filters
st.sidebar.subheader("📅 Time Filters")
period = st.sidebar.selectbox("Time Period", ["month", "day", "year"], index=0)
year_filter = st.sidebar.selectbox("Year Filter", ["All"] + list(range(2020, 2025)), index=0)

# Convert year filter
selected_year = None if year_filter == "All" else year_filter

# Main dashboard content
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Overview", "🏷️ Products", "🌍 Geography", "👥 Customers", "📊 Analytics"])

with tab1:
    st.header("📈 Sales Overview")
    
    # Fetch KPIs
    kpis = fetch_data("/kpis")
    if kpis:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="💰 Total Sales",
                value=format_currency(kpis["total_sales"]),
                delta=f"{kpis['yoy_growth']:.1f}% YoY"
            )
        
        with col2:
            st.metric(
                label="📦 Total Orders",
                value=format_number(kpis["total_orders"])
            )
        
        with col3:
            st.metric(
                label="📊 Total Quantity",
                value=format_number(kpis["total_quantity"])
            )
        
        with col4:
            st.metric(
                label="💵 Avg Order Value",
                value=format_currency(kpis["avg_order_value"])
            )
    
    # Sales over time chart
    st.subheader("📈 Sales Trend Over Time")
    sales_over_time = fetch_data("/sales_over_time", {"period": period, "year": selected_year})
    
    if sales_over_time:
        df_time = pd.DataFrame(sales_over_time["data"])
        df_time.columns = ["Date", "Sales"]
        
        fig = px.line(
            df_time, 
            x="Date", 
            y="Sales",
            title=f"Sales Trend by {period.title()}",
            markers=True
        )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Sales ($)",
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Order status distribution
    st.subheader("📋 Order Status Distribution")
    order_status = fetch_data("/order_status")
    
    if order_status:
        df_status = pd.DataFrame(order_status["data"])
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = px.pie(
                df_status, 
                values="count", 
                names="status",
                title="Order Status Distribution",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.dataframe(df_status, use_container_width=True)

with tab2:
    st.header("🏷️ Product Analysis")
    
    # Sales by product category
    st.subheader("📊 Sales by Product Line")
    category_sales = fetch_data("/sales_by_category")
    
    if category_sales:
        df_category = pd.DataFrame(category_sales["data"])
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = px.bar(
                df_category,
                x="PRODUCTLINE",
                y="SALES",
                title="Sales by Product Line",
                color="SALES",
                color_continuous_scale="Blues"
            )
            fig.update_layout(
                xaxis_title="Product Line",
                yaxis_title="Sales ($)",
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.dataframe(df_category, use_container_width=True)

with tab3:
    st.header("🌍 Geographic Analysis")
    
    # Sales by country
    st.subheader("🗺️ Sales by Country")
    country_sales = fetch_data("/sales_by_country", {"limit": 15})
    
    if country_sales:
        df_country = pd.DataFrame(country_sales["data"])
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = px.bar(
                df_country,
                x="COUNTRY",
                y="SALES",
                title="Top Countries by Sales",
                color="SALES",
                color_continuous_scale="Greens"
            )
            fig.update_layout(
                xaxis_title="Country",
                yaxis_title="Sales ($)",
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.dataframe(df_country, use_container_width=True)

with tab4:
    st.header("👥 Customer Analysis")
    
    # Top customers
    st.subheader("🏆 Top Customers")
    top_customers = fetch_data("/top_customers", {"limit": 15})
    
    if top_customers:
        df_customers = pd.DataFrame(top_customers["data"])
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = px.bar(
                df_customers,
                x="customer",
                y="total_sales",
                title="Top Customers by Sales",
                color="total_sales",
                color_continuous_scale="Purples"
            )
            fig.update_layout(
                xaxis_title="Customer",
                yaxis_title="Total Sales ($)",
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.dataframe(df_customers, use_container_width=True)

with tab5:
    st.header("📊 Advanced Analytics")
    
    # Data summary
    st.subheader("📋 Data Summary")
    data_summary = fetch_data("/data_summary")
    
    if data_summary:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Records", format_number(data_summary["total_records"]))
        
        with col2:
            st.metric("Unique Customers", format_number(data_summary["unique_customers"]))
        
        with col3:
            st.metric("Unique Countries", format_number(data_summary["unique_countries"]))
        
        with col4:
            st.metric("Product Lines", format_number(data_summary["unique_products"]))
        
        st.info(f"📅 Date Range: {data_summary['date_range']['start']} to {data_summary['date_range']['end']}")
    
    # Performance metrics
    st.subheader("⚡ Performance Metrics")
    
    # Calculate some additional metrics
    if kpis and data_summary:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            orders_per_customer = kpis["total_orders"] / data_summary["unique_customers"]
            st.metric("Orders per Customer", f"{orders_per_customer:.1f}")
        
        with col2:
            sales_per_customer = kpis["total_sales"] / data_summary["unique_customers"]
            st.metric("Sales per Customer", format_currency(sales_per_customer))
        
        with col3:
            quantity_per_order = kpis["total_quantity"] / kpis["total_orders"]
            st.metric("Quantity per Order", f"{quantity_per_order:.1f}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        📊 Sales Data Dashboard | Built with Streamlit & FastAPI | Assignment 3
    </div>
    """,
    unsafe_allow_html=True
)

# Auto-refresh option
if st.sidebar.checkbox("🔄 Auto-refresh (30s)"):
    time.sleep(30)
    st.rerun()
