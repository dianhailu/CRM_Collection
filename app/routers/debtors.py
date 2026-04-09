from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_current_user, get_db
from ..models import Debtor
from ..schemas import DebtorCreate, DebtorOut

router = APIRouter(prefix="/debtors", tags=["debtors"])


@router.post("", response_model=DebtorOut)
def create_debtor(
    debtor_in: DebtorCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    exists = db.query(Debtor).filter(Debtor.id_number == debtor_in.id_number).first()
    if exists:
        raise HTTPException(status_code=400, detail="Debtor already exists")

    debtor = Debtor(**debtor_in.model_dump())
    db.add(debtor)
    db.commit()
    db.refresh(debtor)
    return debtor


@router.get("", response_model=list[DebtorOut])
def list_debtors(
    q: str | None = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    query = db.query(Debtor)
    if q:
        query = query.filter(Debtor.name.contains(q))
    return query.order_by(Debtor.id.desc()).all()
