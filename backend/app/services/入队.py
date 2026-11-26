from __future__ import annotations
import uuid
from app.db import 连接
from app.services import 校验
from app.services.时间 import 此刻


def 建事件(body: dict) -> dict:
    类型 = 校验.非空("事件类型", body.get("事件类型"))
    端点键 = 校验.非空("端点键", body.get("端点键"))
    摘要 = str(body.get("载荷摘要") or "")
    优先级 = str(body.get("优先级") or "普通")
    事件号 = str(body.get("事件号") or f"EVT-{uuid.uuid4().hex[:10]}")
    t = 此刻()
    conn = 连接()
    try:
        ep = conn.execute("SELECT * FROM 投递端点 WHERE 端点键=?", (端点键,)).fetchone()
        if not ep:
            raise ValueError("端点不存在")
        if int(ep["启用"]) != 1:
            raise ValueError("端点已停用，拒绝入队")
        if conn.execute("SELECT 1 FROM 事件 WHERE 事件号=?", (事件号,)).fetchone():
            raise ValueError("事件号已存在")
        conn.execute(
            "INSERT INTO 事件(事件号,事件类型,端点键,载荷摘要,优先级,状态,入队时,更新时) VALUES (?,?,?,?,?,?,?,?)",
            (事件号, 类型, 端点键, 摘要, 优先级, "待投", t, t),
        )
        conn.execute("INSERT INTO 操作留痕(时刻,操作,事件号,详情) VALUES (?,?,?,?)",
                     (t, "入队", 事件号, 类型))
        conn.commit()
        return dict(conn.execute("SELECT * FROM 事件 WHERE 事件号=?", (事件号,)).fetchone())
    finally:
        conn.close()
