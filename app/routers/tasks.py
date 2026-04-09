from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_current_user, get_db, require_roles
from ..models import Account, Task, User
from ..schemas import TaskCreate, TaskOut

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskOut)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "leader")),
):
    account = db.query(Account).filter(Account.id == task_in.account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    task = Task(**task_in.model_dump(), created_by_user_id=current_user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("", response_model=list[TaskOut])
def list_tasks(
    assigned_to_user_id: int | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    query = db.query(Task)
    if assigned_to_user_id:
        query = query.filter(Task.assigned_to_user_id == assigned_to_user_id)
    if status:
        query = query.filter(Task.status == status)
    return query.order_by(Task.id.desc()).all()


@router.patch("/{task_id}/done", response_model=TaskOut)
def mark_done(task_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = "done"
    db.commit()
    db.refresh(task)
    return task
