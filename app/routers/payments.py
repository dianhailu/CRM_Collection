from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_current_user, get_db
from ..models import Account, Payment, PromiseToPay
from ..schemas import PaymentCreate, PaymentOut, PromiseCreate, PromiseOut

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("", response_model=PaymentOut)
def create_payment(
    payment_in: PaymentCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    account = db.query(Account).filter(Account.id == payment_in.account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    payment = Payment(**payment_in.model_dump())
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


@router.get("/account/{account_id}", response_model=list[PaymentOut])
def list_payments(account_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Payment).filter(Payment.account_id == account_id).order_by(Payment.id.desc()).all()


@router.post("/promise", response_model=PromiseOut)
def create_promise(
    promise_in: PromiseCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    account = db.query(Account).filter(Account.id == promise_in.account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    ptp = PromiseToPay(**promise_in.model_dump())
    db.add(ptp)
    db.commit()
    db.refresh(ptp)
    return ptp


@router.get("/promise/account/{account_id}", response_model=list[PromiseOut])
def list_promises(account_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(PromiseToPay).filter(PromiseToPay.account_id == account_id).order_by(PromiseToPay.id.desc()).all()
