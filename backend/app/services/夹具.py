from __future__ import annotations
import json
from pathlib import Path
from app.db import 夹具目录


def 列表() -> dict:
    files = []
    if 夹具目录.is_dir():
        for p in sorted(夹具目录.glob("*.json")):
            files.append(p.stem)
    return {"夹具": files}


def 读取(name: str) -> dict:
    p = 夹具目录 / f"{name}.json"
    if not p.is_file():
        # try Chinese names
        for q in 夹具目录.glob("*.json"):
            if q.stem == name or name in q.stem:
                p = q
                break
    if not p.is_file():
        raise FileNotFoundError(name)
    return json.loads(p.read_text(encoding="utf-8"))
