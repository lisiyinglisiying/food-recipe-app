# -*- coding: utf-8 -*-
"""
utils.obe_tracker - OBE 学习成果追踪
====================================
把学生提交的作品数据折算为 OBE 素养评分与成长档案。

四个素养维度（对应项目三维目标）:
    图像识读 - 网页/图片结构理解，看作品数量与结构完整度
    审美判断 - 排版与内容组织，看标题层级、列表、表格等 Markdown 结构
    创意实践 - 动手产出量，看总字数与版本迭代
    文化理解 - 美食主题的文化表达，看标签丰富度与描述完整度

所有函数在无数据时返回合理的基础分，保证页面永远有内容可展示。
"""

import re
from typing import Any, Dict, List

from .storage import get_works_by_user

# 各维度的基础分（学生首次进入时的起点，避免雷达图出现空图）
_BASE = {
    "图像识读": 40,
    "审美判断": 45,
    "创意实践": 30,
    "文化理解": 35,
}


def _clamp(value: float, low: int = 0, high: int = 100) -> int:
    return int(max(low, min(high, round(value))))


def _structure_score(content: str) -> float:
    """
    依据 Markdown 结构丰富度打分（0-30）：
    标题、列表、图片、表格、强调等结构越多分越高。
    """
    if not content:
        return 0.0
    patterns = [
        r"^#{1,6}\s",        # 标题
        r"^\s*[-*+]\s",      # 无序列表
        r"^\s*\d+\.\s",      # 有序列表
        r"!\[.*?\]\(.*?\)",  # 图片
        r"^\s*\|.*\|\s*$",   # 表格
        r"\*\*.+?\*\*",      # 加粗
    ]
    hit = sum(1 for p in patterns if re.search(p, content, re.MULTILINE))
    return hit * 5.0


def calculate_literacy_scores(user_id: str) -> Dict[str, int]:
    """
    计算某学生的四维素养得分（0-100）。

    参数:
        user_id: 学生 ID

    返回:
        dict: {"图像识读": int, "审美判断": int, "创意实践": int, "文化理解": int}
    """
    works = get_works_by_user(user_id)

    if not works:
        return dict(_BASE)

    total_words = sum(int(w.get("word_count") or 0) for w in works)
    work_count = len(works)

    # 结构完整度：取所有作品的平均结构分
    avg_structure = sum(
        _structure_score(w.get("content", "")) for w in works
    ) / work_count

    # 标签丰富度：去重后的标签数量
    all_tags = {t for w in works for t in (w.get("tags") or [])}
    tag_bonus = min(len(all_tags) * 4, 20)

    # 描述完整度：有多少作品写了说明
    desc_ratio = sum(1 for w in works if w.get("description")) / work_count

    scores = {
        "图像识读": _BASE["图像识读"] + avg_structure * 0.8 + work_count * 2,
        "审美判断": _BASE["审美判断"] + avg_structure * 1.2 + tag_bonus * 0.5,
        "创意实践": _BASE["创意实践"] + min(total_words / 60.0, 40) + work_count * 2,
        "文化理解": _BASE["文化理解"] + tag_bonus + desc_ratio * 15,
    }
    return {k: _clamp(v) for k, v in scores.items()}


def _build_badges(works: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    根据作品表现推导成就徽章。

    返回:
        list: [{"name": 徽章名, "icon": 图标, "desc": 获得条件}, ...]
    """
    badges: List[Dict[str, str]] = []
    work_count = len(works)
    total_words = sum(int(w.get("word_count") or 0) for w in works)

    if work_count >= 1:
        badges.append({"name": "初次登场", "icon": "🌱", "desc": "提交第 1 份作品"})
    if work_count >= 3:
        badges.append({"name": "迭代高手", "icon": "🔁", "desc": "累计提交 3 份作品"})
    if work_count >= 5:
        badges.append({"name": "创作达人", "icon": "🏆", "desc": "累计提交 5 份作品"})
    if total_words >= 300:
        badges.append({"name": "下笔有神", "icon": "✍️", "desc": "作品累计 300 字以上"})
    if total_words >= 800:
        badges.append({"name": "长篇巨制", "icon": "📚", "desc": "作品累计 800 字以上"})
    if any((w.get("content") or "").count("![") >= 2 for w in works):
        badges.append({"name": "图文并茂", "icon": "🖼️", "desc": "作品中使用 2 张以上图片"})
    if any("|" in (w.get("content") or "") for w in works):
        badges.append({"name": "表格能手", "icon": "📊", "desc": "作品中使用表格排版"})
    return badges


def get_student_portfolio(user_id: str) -> Dict[str, Any]:
    """
    汇总某学生的学习档案。

    参数:
        user_id: 学生 ID

    返回:
        dict: 含 works_summary / badges_summary / timeline / scores 四部分
    """
    works = get_works_by_user(user_id)
    badges = _build_badges(works)

    total_words = sum(int(w.get("word_count") or 0) for w in works)
    by_unit: Dict[str, int] = {}
    for w in works:
        unit = w.get("unit_id") or "未分类"
        by_unit[unit] = by_unit.get(unit, 0) + 1

    timeline = [
        {
            "id": w.get("id"),
            "title": w.get("title", "未命名作品"),
            "unit_id": w.get("unit_id", ""),
            "submitted_at": w.get("submitted_at", ""),
            "word_count": w.get("word_count", 0),
            "tags": w.get("tags", []),
        }
        for w in works
    ]

    return {
        "user_id": str(user_id),
        "works_summary": {
            "total_count": len(works),
            "total_words": total_words,
            "by_unit": by_unit,
        },
        "badges_summary": {
            "total_count": len(badges),
            "badges": badges,
        },
        "timeline": timeline,
        "scores": calculate_literacy_scores(user_id),
    }
