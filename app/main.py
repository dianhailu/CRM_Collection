from fastapi import FastAPI

from .database import Base, engine
from .routers import accounts, auth, communications, dashboard, debtors, payments, tasks

Base.metadata.create_all(bind=engine)

app = FastAPI(title="催收系统 API", version="1.0.0")

app.include_router(auth.router)
app.include_router(debtors.router)
app.include_router(accounts.router)
app.include_router(communications.router)
app.include_router(payments.router)
app.include_router(tasks.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    return {"message": "催收系统运行中", "docs": "/docs"}
