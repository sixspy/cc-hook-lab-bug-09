from __future__ import annotations
from flask import session
from app.db import 连接


def 校验登录(账号: str, 密码: str) -> bool:
    conn = 连接()
    try:
        row = conn.execute("SELECT 密码哈希 FROM 用户 WHERE 账号=?", (账号,)).fetchone()
        return bool(row) and str(row["密码哈希"]) == str(密码)
    finally:
        conn.close()


def 写入会话(账号: str) -> None:
    session["用户"] = 账号
    session["已登录"] = True


def 已登录() -> bool:
    return bool(session.get("已登录"))


def 登出() -> None:
    session.clear()


def 当前用户() -> str:
    return str(session.get("用户") or "")
