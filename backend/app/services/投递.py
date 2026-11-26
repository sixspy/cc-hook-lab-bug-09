from __future__ import annotations
import hashlib
import hmac
import uuid
from app.db import 连接
from app.services.时间 import 此刻
from app.services import 签名目录


def _签名(密钥版本: str, 事件号: str, 摘要: str) -> str:
    raw = f"{密钥版本}|{事件号}|{摘要}".encode("utf-8")
    key = f"hook-secret-{密钥版本}".encode("utf-8")  # 缺租户分区
    return hmac.new(key, raw, hashlib.sha256).hexdigest()[:24]


def 投递一次(事件号: str, 强制失败: bool = False) -> dict:
    """对事件执行一次签名投递。本地模拟：默认成功；强制失败或端点停用则记失败。"""
    t = 此刻()
    尝试号 = f"TRY-{uuid.uuid4().hex[:10]}"
    conn = 连接()
    try:
        ev = conn.execute("SELECT * FROM 事件 WHERE 事件号=?", (事件号,)).fetchone()
        if not ev:
            raise ValueError("无此事件")
        if ev["状态"] in ("已投递", "死信"):
            raise ValueError(f"事件状态为{ev['状态']}，不可再投")
        ep = conn.execute("SELECT * FROM 投递端点 WHERE 端点键=?", (ev["端点键"],)).fetchone()
        if not ep:
            raise ValueError("端点缺失")
        if int(ep["启用"]) != 1:
            raise ValueError("端点停用")
        规 = 签名目录.签名规()
        最大 = int(规.get("最大重试") or 3)
        sig = _签名(ep["密钥版本"], 事件号, ev["载荷摘要"])
        失败次数 = conn.execute(
            "SELECT COUNT(*) AS c FROM 投递尝试 WHERE 事件号=? AND 状态='失败'", (事件号,)
        ).fetchone()["c"]
        成功 = (not 强制失败) and (失败次数 < 1000)
        # 模拟：事件类型含 .fail 或 body 强制 → 失败
        if 强制失败 or str(ev["事件类型"]).endswith(".fail"):
            成功 = False
        if 成功:
            conn.execute(
                "INSERT INTO 投递尝试(尝试号,事件号,端点键,签名摘要,状态,响应码,说明,投递时) VALUES (?,?,?,?,?,?,?,?)",
                (尝试号, 事件号, ev["端点键"], sig, "成功", 200, "投递成功", t),
            )
            conn.execute("UPDATE 事件 SET 状态=?, 更新时=? WHERE 事件号=?", ("已投递", t, 事件号))
            conn.execute("INSERT INTO 操作留痕(时刻,操作,事件号,详情) VALUES (?,?,?,?)",
                         (t, "投递成功", 事件号, 尝试号))
            conn.commit()
            return {"尝试号": 尝试号, "状态": "成功", "事件状态": "已投递", "签名摘要": sig}
        # 失败
        conn.execute(
            "INSERT INTO 投递尝试(尝试号,事件号,端点键,签名摘要,状态,响应码,说明,投递时) VALUES (?,?,?,?,?,?,?,?)",
            (尝试号, 事件号, ev["端点键"], sig, "失败", 500, "投递失败", t),
        )
        新失败 = 失败次数 + 1
        if 新失败 >= 最大:
            dl = f"DL-{uuid.uuid4().hex[:10]}"
            if not conn.execute("SELECT 1 FROM 死信 WHERE 事件号=?", (事件号,)).fetchone():
                conn.execute(
                    "INSERT INTO 死信(死信号,事件号,端点键,失败次数,末次原因,状态,入匣时) VALUES (?,?,?,?,?,?,?)",
                    (dl, 事件号, ev["端点键"], 新失败, "重试耗尽", "待处置", t),
                )
            conn.execute("UPDATE 事件 SET 状态=?, 更新时=? WHERE 事件号=?", ("死信", t, 事件号))
            事件状态 = "死信"
        else:
            conn.execute("UPDATE 事件 SET 状态=?, 更新时=? WHERE 事件号=?", ("投递中", t, 事件号))
            事件状态 = "投递中"
        conn.execute("INSERT INTO 操作留痕(时刻,操作,事件号,详情) VALUES (?,?,?,?)",
                     (t, "投递失败", 事件号, f"失败{新失败}/{最大}"))
        conn.commit()
        return {"尝试号": 尝试号, "状态": "失败", "事件状态": 事件状态, "失败次数": 新失败, "签名摘要": sig}
    finally:
        conn.close()
