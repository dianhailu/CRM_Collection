from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_current_user, get_db
from ..models import Account, Debtor
from ..schemas import AccountCreate, AccountOut
from ..services import account_totals

router = APIRouter(prefix="/accounts", tags=["accounts"])


def to_account_out(account: Account) -> AccountOut:
    total_due, total_paid, balance = account_totals(account)
    payload = {
        **account.__dict__,
        "total_due": total_due,
        "total_paid": total_paid,
        "balance": balance,
    }
    payload.pop("_sa_instance_state", None)
    return AccountOut(**payload)


@router.post("", response_model=AccountOut)
def create_account(
    account_in: AccountCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    debtor = db.query(Debtor).filter(Debtor.id == account_in.debtor_id).first()
    if not debtor:
        raise HTTPException(status_code=404, detail="Debtor not found")

    exists = db.query(Account).filter(Account.contract_no == account_in.contract_no).first()
    if exists:
        raise HTTPException(status_code=400, detail="Contract already exists")

    account = Account(**account_in.model_dump())
    db.add(account)
    db.commit()
    db.refresh(account)
    return to_account_out(account)


@router.get("", response_model=list[AccountOut])
def list_accounts(
    debtor_id: int | None = None,
    assigned_to_user_id: int | None = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    query = db.query(Account)
    if debtor_id:
        query = query.filter(Account.debtor_id == debtor_id)
    if assigned_to_user_id:
        query = query.filter(Account.assigned_to_user_id == assigned_to_user_id)

    accounts = query.order_by(Account.id.desc()).all()
    return [to_account_out(acc) for acc in accounts]
