from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_current_user, get_db
from ..models import Account, Communication, User
from ..schemas import CommunicationCreate, CommunicationOut

router = APIRouter(prefix="/communications", tags=["communications"])


@router.post("", response_model=CommunicationOut)
def create_communication(
    comm_in: CommunicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = db.query(Account).filter(Account.id == comm_in.account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    comm = Communication(**comm_in.model_dump(), user_id=current_user.id)
    db.add(comm)
    db.commit()
    db.refresh(comm)
    return comm


@router.get("/account/{account_id}", response_model=list[CommunicationOut])
def list_communications(account_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Communication).filter(Communication.account_id == account_id).order_by(Communication.id.desc()).all()
