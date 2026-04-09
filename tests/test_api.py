from datetime import date

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_full_flow():
    reg = client.post(
        "/auth/register",
        json={"username": "admin", "full_name": "系统管理员", "role": "admin", "password": "secret123"},
    )
    assert reg.status_code in (200, 400)

    token_resp = client.post("/auth/token", data={"username": "admin", "password": "secret123"})
    assert token_resp.status_code == 200
    token = token_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    debtor = client.post(
        "/debtors",
        headers=headers,
        json={
            "name": "张三",
            "id_number": "ID10001",
            "phone": "13800138000",
            "email": "zhangsan@example.com",
            "address": "上海市",
            "risk_level": "H",
            "status": "新案",
        },
    )
    assert debtor.status_code in (200, 400)

    debtors = client.get("/debtors", headers=headers)
    assert debtors.status_code == 200
    debtor_id = debtors.json()[0]["id"]

    account = client.post(
        "/accounts",
        headers=headers,
        json={
            "debtor_id": debtor_id,
            "contract_no": "CONTRACT-1001",
            "principal": "10000",
            "interest": "500",
            "penalty": "100",
            "overdue_days": 45,
            "stage": "M2",
            "status": "跟进中",
        },
    )
    assert account.status_code in (200, 400)

    accounts = client.get("/accounts", headers=headers)
    assert accounts.status_code == 200
    account_id = accounts.json()[0]["id"]

    pay = client.post(
        "/payments",
        headers=headers,
        json={"account_id": account_id, "amount": "300", "paid_at": str(date.today())},
    )
    assert pay.status_code == 200

    comm = client.post(
        "/communications",
        headers=headers,
        json={"account_id": account_id, "channel": "phone", "result": "承诺还款"},
    )
    assert comm.status_code == 200

    task = client.post(
        "/tasks",
        headers=headers,
        json={"account_id": account_id, "title": "三日内再次联系", "priority": "high"},
    )
    assert task.status_code == 200

    summary = client.get("/dashboard/summary", headers=headers)
    assert summary.status_code == 200
    assert "payment_total" in summary.json()
