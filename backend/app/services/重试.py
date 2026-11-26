from __future__ import annotations
from app.db import 连接
from app.services import 投递, 签名目录


def 批量重试待投(限制: int = 20) -> dict:
    conn = 连接()
    try:
        rows = conn.execute(
            "SELECT 事件号 FROM 事件 WHERE 状态 IN ('待投','投递中') ORDER BY 入队时 LIMIT ?",
            (限制,),
        ).fetchall()
    finally:
        conn.close()
    outs = []
    for r in rows:
        try:
            outs.append(投递.投递一次(r["事件号"]))
        except ValueError as e:
            outs.append({"事件号": r["事件号"], "错误": str(e)})
    return {"条数": len(outs), "结果": outs, "签名规": 签名目录.签名规()}
