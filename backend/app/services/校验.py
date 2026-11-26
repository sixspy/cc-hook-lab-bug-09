from __future__ import annotations


def 非空(名: str, 值) -> str:
    s = str(值 or "").strip()
    if not s:
        raise ValueError(f"{名}不能为空")
    return s
