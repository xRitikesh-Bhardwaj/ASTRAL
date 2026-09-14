import sqlite3
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "database", "astral.db"))

def predict_churn():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM customers", conn)
    conn.close()
    
    if len(df) == 0:
        return {"error": "No customer data available"}
        
    # Feature matrix: total_spent, orders_count, last_order_days_ago
    X = df[['total_spent', 'orders_count', 'last_order_days_ago']].copy()
    
    # Synthetic label generation for logistic regression training based on business heuristics
    # Churn occurs if last order > 35 days or low frequency vs recency
    y = ((X['last_order_days_ago'] > 35) | (X['orders_count'] < 15)).astype(int)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    model = LogisticRegression(random_state=42)
    model.fit(X_scaled, y)
    
    probs = model.predict_proba(X_scaled)[:, 1]
    
    customers_result = []
    high_count = 0
    med_count = 0
    low_count = 0
    
    for idx, row in df.iterrows():
        p = float(probs[idx])
        if p > 0.60:
            risk = "High Risk"
            high_count += 1
            action = "Offer dedicated executive account manager check-in & 15% renewal incentive."
        elif p > 0.30:
            risk = "Medium Risk"
            med_count += 1
            action = "Send automated product update newsletter & feature usage tips."
        else:
            risk = "Low Risk"
            low_count += 1
            action = "Account stable. Recommend upselling Enterprise Cloud Module."
            
        customers_result.append({
            "id": int(row['id']),
            "name": row['name'],
            "company": row['company'],
            "total_spent": float(row['total_spent']),
            "orders_count": int(row['orders_count']),
            "last_order_days_ago": int(row['last_order_days_ago']),
            "churn_probability": round(p * 100, 1),
            "risk_level": risk,
            "recommended_action": action
        })
        
    return {
        "model_used": "LogisticRegression",
        "total_customers": len(df),
        "high_risk_count": high_count,
        "medium_risk_count": med_count,
        "low_risk_count": low_count,
        "customers": customers_result
    }

if __name__ == "__main__":
    res = predict_churn()
    print("Churn summary:", res['high_risk_count'], "High risk customers")
