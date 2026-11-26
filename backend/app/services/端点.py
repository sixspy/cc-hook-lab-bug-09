from __future__ import annotations
from app.db import 连接
from app.services import 校验
from app.services.时间 import 此刻


def 登记(body: dict) -> dict:
    端点键 = 校验.非空("端点键", body.get("端点键"))
    名称 = 校验.非空("名称", body.get("名称"))
    url = 校验.非空("回调URL", body.get("回调URL"))
    版本 = str(body.get("密钥版本") or "v1")
    说明 = str(body.get("说明") or "")
    conn = 连接()
    try:
        if conn.execute("SELECT 1 FROM 投递端点 WHERE 端点键=?", (端点键,)).fetchone():
            raise ValueError("端点键已存在")
        conn.execute(
            "INSERT INTO 投递端点(端点键,名称,回调URL,密钥版本,启用,说明) VALUES (?,?,?,?,1,?)",
            (端点键, 名称, url, 版本, 说明),
        )
        conn.execute("INSERT INTO 操作留痕(时刻,操作,事件号,详情) VALUES (?,?,?,?)",
                     (此刻(), "登记端点", "", 端点键))
        conn.commit()
        return dict(conn.execute("SELECT * FROM 投递端点 WHERE 端点键=?", (端点键,)).fetchone())
    finally:
        conn.close()


def 改启用(端点键: str, 启用: bool) -> dict:
    conn = 连接()
    try:
        if not conn.execute("SELECT 1 FROM 投递端点 WHERE 端点键=?", (端点键,)).fetchone():
            raise ValueError("无此端点")
        conn.execute("UPDATE 投递端点 SET 启用=? WHERE 端点键=?", (1 if 启用 else 0, 端点键))
        conn.commit()
        return dict(conn.execute("SELECT * FROM 投递端点 WHERE 端点键=?", (端点键,)).fetchone())
    finally:
        conn.close()
