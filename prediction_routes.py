from fastapi import APIRouter
from ml.revenue_prediction import predict_revenue
from ml.churn_prediction import predict_churn
from ml.anomaly_detection import detect_anomalies

router = APIRouter(prefix="/api", tags=["Predictions"])

@router.get("/predictions/revenue")
def get_revenue_predictions():
    return predict_revenue()

@router.get("/predictions/churn")
def get_churn_predictions():
    return predict_churn()

@router.get("/anomalies")
def get_anomalies():
    return detect_anomalies()
