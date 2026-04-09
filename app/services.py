from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from .models import Account, Communication, Payment, Task


def account_totals(account: Account) -> tuple[Decimal, Decimal, Decimal]:
    total_due = Decimal(account.principal) + Decimal(account.interest) + Decimal(account.penalty)
    total_paid = sum((Decimal(p.amount) for p in account.payments), start=Decimal("0"))
    balance = total_due - total_paid
    return total_due, total_paid, balance


def dashboard_summary(db: Session, date_from: date, date_to: date) -> dict:
    payment_total = sum(
        (Decimal(p.amount) for p in db.query(Payment).filter(Payment.paid_at >= date_from, Payment.paid_at <= date_to).all()),
        start=Decimal("0"),
    )
    communication_count = (
        db.query(Communication)
        .filter(Communication.created_at >= date_from, Communication.created_at <= date_to)
        .count()
    )
    completed_task_count = (
        db.query(Task)
        .filter(Task.created_at >= date_from, Task.created_at <= date_to, Task.status == "done")
        .count()
    )
    total_task_count = db.query(Task).filter(Task.created_at >= date_from, Task.created_at <= date_to).count()
    rate = (completed_task_count / total_task_count) if total_task_count else 0.0

    return {
        "date_from": date_from,
        "date_to": date_to,
        "payment_total": payment_total,
        "communication_count": communication_count,
        "completed_task_count": completed_task_count,
        "total_task_count": total_task_count,
        "task_completion_rate": round(rate, 4),
    }
