# -*- coding: utf-8 -*-
"""
utils 包 - 数据与学习分析工具
=============================
补全模块（原项目打包遗漏），提供：
    - storage:     作品/任务等记录的轻量持久化（JSON 文件）
    - obe_tracker: 基于作品数据的素养评分与学习档案汇总
"""

from .storage import (  # noqa: F401
    create_work,
    get_works_by_user,
    query,
    get_by_id,
)
from .obe_tracker import (  # noqa: F401
    get_student_portfolio,
    calculate_literacy_scores,
)

__all__ = [
    "create_work",
    "get_works_by_user",
    "query",
    "get_by_id",
    "get_student_portfolio",
    "calculate_literacy_scores",
]
