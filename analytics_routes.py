from fastapi import APIRouter
import sqlite3
import pandas as pd
import os

router = APIRouter(prefix="/api", tags=["Analytics"])
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "database", "astral.db"))

@router.get("/analytics")
def get_analytics():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    df = pd.read_sql_query("SELECT * FROM daily_metrics ORDER BY date DESC LIMIT 30", conn)
    products_cursor = conn.cursor()
    products_cursor.execute("SELECT * FROM products ORDER BY revenue_generated DESC")
    products = [dict(row) for row in products_cursor.fetchall()]
    conn.close()
    
    cat_totals = {
        "Electronics": float(df['cat_electronics'].sum()),
        "Software": float(df['cat_software'].sum()),
        "Cloud Services": float(df['cat_cloud'].sum()),
        "Hardware": float(df['cat_hardware'].sum()),
        "Consulting": float(df['cat_consulting'].sum())
    }
    
    dates = [row['date'][5:] for _, row in df.iloc[::-1].iterrows()]
    revenues = [round(float(row['revenue'])/100000, 2) for _, row in df.iloc[::-1].iterrows()]
    orders = [int(row['orders']) for _, row in df.iloc[::-1].iterrows()]
    customers = [int(row['customers_active']) for _, row in df.iloc[::-1].iterrows()]
    
    return {
        "revenue_trend": {
            "labels": dates,
            "values": revenues
        },
        "order_trend": {
            "labels": dates,
            "values": orders
        },
        "customer_trend": {
            "labels": dates,
            "values": customers
        },
        "category_distribution": cat_totals,
        "top_products": products
    }
