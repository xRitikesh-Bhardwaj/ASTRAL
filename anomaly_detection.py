import sqlite3
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "database", "astral.db"))

def detect_anomalies():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM daily_metrics ORDER BY date DESC LIMIT 60", conn)
    conn.close()
    
    if len(df) == 0:
        return {"anomalies": []}
        
    X = df[['revenue', 'orders', 'new_customers', 'profit']].copy()
    
    model = IsolationForest(contamination=0.08, random_state=42)
    preds = model.fit_predict(X)  # -1 indicates anomaly
    
    anomalies = []
    mean_rev = df['revenue'].mean()
    mean_orders = df['orders'].mean()
    
    for idx, pred in enumerate(preds):
        if pred == -1:
            row = df.iloc[idx]
            rev = float(row['revenue'])
            orders = int(row['orders'])
            
            if rev < mean_rev * 0.75:
                severity = "High"
                issue = "Significant daily revenue drop detected."
                impact = f"Revenue fell {round((1 - rev/mean_rev)*100, 1)}% below the 60-day average."
            elif rev > mean_rev * 1.30:
                severity = "Positive"
                issue = "Unusually high revenue spike recorded."
                impact = f"Revenue exceeded standard 60-day baseline by {round((rev/mean_rev - 1)*100, 1)}%."
            else:
                severity = "Medium"
                issue = "Abnormal ratio between order volume and net profit."
                impact = "Marginal order volatility detected on this business date."
                
            anomalies.append({
                "date": row['date'],
                "day_of_week": row['day_of_week'],
                "revenue": round(rev, 2),
                "orders": orders,
                "severity": severity,
                "issue": issue,
                "impact": impact
            })
            
    return {
        "model_used": "IsolationForest",
        "total_anomalies_found": len(anomalies),
        "anomalies": anomalies
    }

if __name__ == "__main__":
    res = detect_anomalies()
    print("Found anomalies:", res['total_anomalies_found'])
