# 催收系统（完整功能版）

这是一个可直接运行的催收系统后端（FastAPI + SQLite），包含真实项目常见的核心模块：

- 用户与角色权限（管理员/组长/催收员）
- 债务人档案管理（基础资料、状态、风险等级）
- 账户与案件管理（本金、利息、罚息、逾期天数、案件阶段）
- 跟进记录（电话/短信/微信/上门等）
- 还款登记与自动余额计算
- 承诺还款（PTP）管理
- 催收任务分配与完成状态跟踪
- 统计看板（回款、跟进次数、任务完成率）

## 1. 快速启动

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

打开接口文档：`http://127.0.0.1:8000/docs`

## 2. 首次使用流程

1. 注册管理员用户：`POST /auth/register`
2. 登录获取 token：`POST /auth/token`
3. 在 Swagger 顶部 `Authorize` 粘贴：`Bearer <token>`
4. 开始维护债务人、账户、催收记录与还款数据

## 3. 核心模块说明

### 3.1 债务人（Debtor）
- 姓名、证件号、联系方式、地址
- 风险等级（L/M/H）
- 当前状态（新案/跟进中/承诺还款/已结清/失联）

### 3.2 催收账户（Account）
- 对应债务人
- 本金、利息、罚息
- 自动计算总应还、已还、未还
- 逾期天数、案件阶段、分配催收员

### 3.3 跟进记录（Communication Log）
- 沟通方式、结果、下次联系时间、备注
- 与账户关联，可形成完整催收轨迹

### 3.4 还款与承诺（Payment / PTP）
- 记录每笔还款，自动更新账户余额
- 支持承诺还款日期与金额，便于催收提醒

### 3.5 催收任务（Task）
- 标题、优先级、截止时间、状态
- 负责人、创建人、关联账户

### 3.6 报表看板（Dashboard）
- 指定时间范围统计回款总额
- 跟进次数统计
- 任务完成率统计

## 4. 目录结构

```text
app/
  main.py
  database.py
  models.py
  schemas.py
  security.py
  dependencies.py
  services.py
  routers/
    auth.py
    debtors.py
    accounts.py
    communications.py
    payments.py
    tasks.py
    dashboard.py
tests/
  test_api.py
```

## 5. 默认设计说明

- 使用 SQLite，方便本地快速演示。
- 采用 JWT 鉴权，接口按角色做权限控制。
- 在生产环境可替换为 PostgreSQL + Redis + 定时任务系统（Celery/Arq）。

## 6. 后续可扩展项（已预留）

- 自动外呼系统接入
- 短信网关与模板管理
- 法务流程（诉前函件、诉讼节点）
- 质检与录音管理
- 组织架构与多租户
