from fastapi import APIRouter, Depends
from app.database import SessionDep
from app import crud, schemas
from app.authorization import check_api_key
import logging

router = APIRouter(
    prefix = "/reports",
    tags = ["Report"]
)

logger = logging.getLogger("FleetRent")

@router.get("/monthly", response_model=schemas.MonthlyReportResponse)
def get_monthly_report(year: int, month: int, db: SessionDep, _: str = Depends(check_api_key)):
    logger.info(f"Financial report generated for year-month: {year}-{month}")
    return crud.get_monthly_report(db=db, year=year, month=month)