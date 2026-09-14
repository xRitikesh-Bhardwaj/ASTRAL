import sqlite3
import pandas as pd
import os
import hashlib

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "database", "astral.db"))
CSV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "business_data.csv"))

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'Executive Manager',
        company TEXT DEFAULT 'ASTRAL Global Enterprise'
    )
    """)
    
    # 2. Daily Metrics Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT UNIQUE NOT NULL,
        day_of_week TEXT,
        revenue REAL,
        orders INTEGER,
        customers_active INTEGER,
        new_customers INTEGER,
        profit REAL,
        cat_electronics REAL,
        cat_software REAL,
        cat_cloud REAL,
        cat_hardware REAL,
        cat_consulting REAL
    )
    """)

    # 3. Customers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        company TEXT NOT NULL,
        total_spent REAL,
        orders_count INTEGER,
        last_order_days_ago INTEGER,
        churn_risk_score REAL,
        risk_level TEXT
    )
    """)

    # 4. Products Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        sales_count INTEGER,
        revenue_generated REAL,
        growth_rate REAL
    )
    """)
    
    conn.commit()

    # Seed Default Executive User if not exists
    cursor.execute("SELECT id FROM users WHERE email = 'admin@astral.ai'")
    if not cursor.fetchone():
        cursor.execute("""
        INSERT INTO users (email, name, password_hash, role, company)
        VALUES ('admin@astral.ai', 'Vikramaditya Rao', ?, 'Executive Manager', 'ASTRAL Enterprise Solutions')
        """, (hash_password("astral2026"),))
        print("Default executive user created: admin@astral.ai / astral2026")

    # Seed Daily Metrics from CSV if table is empty
    cursor.execute("SELECT COUNT(*) FROM daily_metrics")
    count = cursor.fetchone()[0]
    if count == 0 and os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        df.to_sql("daily_metrics", conn, if_exists="append", index=False)
        print(f"Seeded {len(df)} rows into daily_metrics table!")

    # Seed Customers if empty
    cursor.execute("SELECT COUNT(*) FROM customers")
    if cursor.fetchone()[0] == 0:
        sample_customers = [
            ("Apex Global Technologies", "Apex Corp", 4580000.0, 42, 4, 0.12, "Low Risk"),
            ("Nexura Cyber Systems", "Nexura Inc", 3240000.0, 31, 12, 0.28, "Low Risk"),
            ("Vanguard Logistics", "Vanguard Group", 1890000.0, 18, 48, 0.74, "High Risk"),
            ("Orion Cloud Dynamics", "Orion Tech", 6120000.0, 58, 2, 0.08, "Low Risk"),
            ("Zenith Retail Chain", "Zenith Enterprise", 2980000.0, 24, 62, 0.88, "High Risk"),
            ("Synergy Energy Systems", "Synergy Corp", 5100000.0, 46, 9, 0.19, "Low Risk"),
            ("Starlight Media Works", "Starlight Inc", 1250000.0, 11, 41, 0.58, "Medium Risk"),
            ("Helix Health Tech", "Helix Bio", 4120000.0, 37, 15, 0.31, "Medium Risk"),
            ("Quantum Financials", "Quantum Capital", 8900000.0, 84, 1, 0.04, "Low Risk"),
            ("Nova Infra Developers", "Nova Infra", 1450000.0, 12, 54, 0.79, "High Risk"),
            ("Aegis Defense Labs", "Aegis Group", 3780000.0, 29, 21, 0.42, "Medium Risk"),
            ("Pinnacle Telecom", "Pinnacle Networks", 7340000.0, 67, 5, 0.11, "Low Risk")
        ]
        cursor.executemany("""
        INSERT INTO customers (name, company, total_spent, orders_count, last_order_days_ago, churn_risk_score, risk_level)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, sample_customers)
        print("Seeded sample customer records!")

    # Seed Products if empty
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        sample_products = [
            ("ASTRAL Enterprise Suite v4", "Enterprise Software", 1280, 47360000.0, 14.2),
            ("Cloud Infra Node Pro", "Cloud Services", 3420, 36410000.0, 18.5),
            ("Neural Edge Server 8000", "Electronics", 490, 69090000.0, 9.8),
            ("AI Business Twin Simulator", "Enterprise Software", 870, 28710000.0, 22.1),
            ("High Precision Sensor Gateway", "Hardware", 2150, 18275000.0, 7.4),
            ("Executive AI Assistant License", "Cloud Services", 4100, 15375000.0, 31.0),
            ("Strategic BI Consulting Package", "Consulting", 140, 10920000.0, 11.6)
        ]
        cursor.executemany("""
        INSERT INTO products (name, category, sales_count, revenue_generated, growth_rate)
        VALUES (?, ?, ?, ?, ?)
        """, sample_products)
        print("Seeded sample product records!")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
