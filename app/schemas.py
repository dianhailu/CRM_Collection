from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    username: str
    full_name: str
    role: str = "collector"
    password: str = Field(min_length=6)


class UserOut(BaseModel):
    id: int
    username: str
    full_name: str
    role: str

    model_config = ConfigDict(from_attributes=True)


class DebtorCreate(BaseModel):
    name: str
    id_number: str
    phone: str
    email: str | None = None
    address: str | None = None
    risk_level: str = "M"
    status: str = "新案"


class DebtorOut(DebtorCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AccountCreate(BaseModel):
    debtor_id: int
    contract_no: str
    principal: Decimal = Decimal("0")
    interest: Decimal = Decimal("0")
    penalty: Decimal = Decimal("0")
    overdue_days: int = 0
    stage: str = "M1"
    status: str = "跟进中"
    assigned_to_user_id: int | None = None


class AccountOut(AccountCreate):
    id: int
    created_at: datetime
    total_due: Decimal
    total_paid: Decimal
    balance: Decimal

    model_config = ConfigDict(from_attributes=True)


class CommunicationCreate(BaseModel):
    account_id: int
    channel: str
    result: str
    notes: str | None = None
    next_contact_at: datetime | None = None


class CommunicationOut(BaseModel):
    id: int
    account_id: int
    user_id: int
    channel: str
    result: str
    notes: str | None
    next_contact_at: datetime | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaymentCreate(BaseModel):
    account_id: int
    amount: Decimal = Field(gt=0)
    paid_at: date
    method: str = "bank_transfer"
    remarks: str | None = None


class PaymentOut(PaymentCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PromiseCreate(BaseModel):
    account_id: int
    promised_amount: Decimal = Field(gt=0)
    promised_date: date


class PromiseOut(PromiseCreate):
    id: int
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskCreate(BaseModel):
    account_id: int
    title: str
    description: str | None = None
    priority: str = "medium"
    due_date: date | None = None
    assigned_to_user_id: int | None = None


class TaskOut(BaseModel):
    id: int
    account_id: int
    title: str
    description: str | None
    priority: str
    due_date: date | None
    status: str
    assigned_to_user_id: int | None
    created_by_user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DashboardSummary(BaseModel):
    date_from: date
    date_to: date
    payment_total: Decimal
    communication_count: int
    completed_task_count: int
    total_task_count: int
    task_completion_rate: float
