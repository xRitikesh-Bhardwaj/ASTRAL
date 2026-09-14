from fastapi import APIRouter
from fastapi.responses import Response
from reports.report_generator import generate_report, export_report_csv

router = APIRouter(prefix="/api/reports", tags=["Reports"])

@router.get("/daily")
def get_daily_report():
    return generate_report("daily")

@router.get("/weekly")
def get_weekly_report():
    return generate_report("weekly")

@router.get("/monthly")
def get_monthly_report():
    return generate_report("monthly")

@router.get("/export-csv")
def download_csv_report():
    csv_data = export_report_csv()
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=ASTRAL_Executive_Report.csv"}
    )
