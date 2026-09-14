import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta
import sqlite3
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "database", "astral.db"))

def predict_revenue():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM daily_metrics ORDER BY date ASC", conn)
    conn.close()
    
    if len(df) < 14:
        return {"error": "Insufficient data for prediction"}
        
    df['date_dt'] = pd.to_datetime(df['date'])
    df['day_of_week_num'] = df['date_dt'].dt.dayofweek
    df['day_of_month'] = df['date_dt'].dt.day
    df['month'] = df['date_dt'].dt.month
    df['lag_1'] = df['revenue'].shift(1)
    df['lag_7'] = df['revenue'].shift(7)
    df['rolling_7_mean'] = df['revenue'].shift(1).rolling(window=7).mean()
    
    # Drop initial NaN rows created by lags
    clean_df = df.dropna().copy()
    
    features = ['day_of_week_num', 'day_of_month', 'month', 'lag_1', 'lag_7', 'rolling_7_mean']
    X = clean_df[features]
    y = clean_df['revenue']
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Predict next 7 days
    last_date = df['date_dt'].iloc[-1]
    forecast = []
    
    recent_revenues = list(df['revenue'].values)
    
    for i in range(1, 8):
        next_date = last_date + timedelta(days=i)
        dow = next_date.dayofweek
        dom = next_date.day
        month = next_date.month
        lag_1 = recent_revenues[-1]
        lag_7 = recent_revenues[-7]
        rolling_7 = float(np.mean(recent_revenues[-7:]))
        
        feat_vector = pd.DataFrame([[dow, dom, month, lag_1, lag_7, rolling_7]], columns=features)
        pred_rev = float(model.predict(feat_vector)[0])
        
        recent_revenues.append(pred_rev)
        
        # Upper and lower bounds for confidence range (±5%)
        forecast.append({
            "date": next_date.strftime("%Y-%m-%d"),
            "day_name": next_date.strftime("%a"),
            "predicted_revenue": round(pred_rev, 2),
            "lower_bound": round(pred_rev * 0.95, 2),
            "upper_bound": round(pred_rev * 1.05, 2)
        })
        
    # Historical data summary (last 14 days)
    history = []
    for _, row in df.tail(14).iterrows():
        history.append({
            "date": row['date'],
            "day_name": pd.to_datetime(row['date']).strftime("%a"),
            "actual_revenue": round(float(row['revenue']), 2)
        })
        
    total_forecasted = sum(item['predicted_revenue'] for item in forecast)
    
    return {
        "model_used": "RandomForestRegressor",
        "next_7_days_total": round(total_forecasted, 2),
        "forecast": forecast,
        "history": history
    }

if __name__ == "__main__":
    res = predict_revenue()
    print("Revenue prediction sample:", res['next_7_days_total'])
