"""租户密钥读轨审计。"""
from __future__ import annotations

from app.services import ten as core
from app.services import ten_cutover as cutover
from app.services import ten_dualwrite as dual


def audit_summary() -> dict:
    return {
        "title": "租户密钥审计",
        "core": core.dashboard(),
        "cutover": cutover.board(),
        "dualwrite": dual.dual_board(),
        "half": core.half_fix_display(),
    }
