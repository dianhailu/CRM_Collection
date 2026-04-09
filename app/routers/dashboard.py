from datetime import date, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies import get_current_user, get_db
from ..schemas import DashboardSummary
from ..services import dashboard_summary

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def get_summary(
    date_from: date | None = None,
    date_to: date | None = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    today = date.today()
    date_to = date_to or today
    date_from = date_from or (today - timedelta(days=30))
    return dashboard_summary(db, date_from=date_from, date_to=date_to)
