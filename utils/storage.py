# -*- coding: utf-8 -*-
"""
utils.storage - 轻量数据存储层
==============================
为学生作品、任务、疑问等记录提供持久化能力。

设计取舍：
    - 使用单个 JSON 文件存储，零外部依赖，部署时无需额外的数据库服务；
    - 写入采用「临时文件 + 原子替换」，避免进程中断导致数据损坏；
    - 通过线程锁串行化读写，规避 Streamlit 多线程下的竞态；
    - 存储目录可用环境变量 APP_DATA_DIR 覆盖，便于在托管平台上挂载持久卷。

数据结构（单文件）:
    {
      "works": [ {...}, ... ],
      "tasks": [...],
      "questions": [...]
    }
"""

import json
import os
import threading
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# ============================================================
# 存储位置与并发控制
# ============================================================
_BASE_DIR = Path(
    os.environ.get("APP_DATA_DIR")
    or (Path(__file__).resolve().parent.parent / "data")
)
_DB_FILE = _BASE_DIR / "db.json"

_LOCK = threading.RLock()

# 允许的表名，避免任意写入造成结构污染
_TABLES = ("works", "tasks", "questions", "assessments")


def _now() -> str:
    """统一的时间戳格式"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _ensure_dir() -> None:
    """确保存储目录存在"""
    _BASE_DIR.mkdir(parents=True, exist_ok=True)


def _load() -> Dict[str, List[Dict[str, Any]]]:
    """读取整个数据库；文件缺失或损坏时返回空结构，保证页面不崩"""
    _ensure_dir()
    if not _DB_FILE.exists():
        return {name: [] for name in _TABLES}
    try:
        with open(_DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {name: [] for name in _TABLES}

    if not isinstance(data, dict):
        return {name: [] for name in _TABLES}
    # 兼容老文件缺表的情况
    for name in _TABLES:
        data.setdefault(name, [])
    return data


def _save(data: Dict[str, List[Dict[str, Any]]]) -> None:
    """原子写入，先写临时文件再替换，避免半截文件"""
    _ensure_dir()
    tmp = _DB_FILE.with_suffix(".json.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, _DB_FILE)


def _check_table(table: str) -> str:
    if table not in _TABLES:
        raise ValueError(f"未知的数据表：{table}（可用：{', '.join(_TABLES)}）")
    return table


# ============================================================
# 写入接口
# ============================================================
def create_work(
    user_id: str,
    unit_id: str,
    title: str,
    content: str,
    description: str = "",
    tags: Optional[List[str]] = None,
    **extra: Any,
) -> Dict[str, Any]:
    """
    新建一条学生作品记录。

    参数:
        user_id:     提交者 ID
        unit_id:     所属单元标识，如 "unit1"
        title:       作品标题
        content:     作品正文（Markdown 原文）
        description: 作品说明，默认记录为第几版
        tags:        标签列表
        **extra:     其它需要一并保存的字段

    返回:
        dict: 写入的完整记录（含生成的 id）
    """
    record = {
        "id": f"work_{uuid.uuid4().hex[:12]}",
        "user_id": str(user_id),
        "unit_id": str(unit_id),
        "title": title or "未命名作品",
        "content": content or "",
        "description": description,
        "tags": list(tags or []),
        "word_count": len(content or ""),
        "submitted_at": _now(),
        "created_at": _now(),
    }
    record.update(extra)

    with _LOCK:
        data = _load()
        data["works"].insert(0, record)
        _save(data)
    return record


def insert(table: str, record: Dict[str, Any]) -> Dict[str, Any]:
    """通用插入，供任务、疑问等其它表使用"""
    table = _check_table(table)
    row = dict(record)
    row.setdefault("id", f"{table[:-1]}_{uuid.uuid4().hex[:12]}")
    row.setdefault("created_at", _now())

    with _LOCK:
        data = _load()
        data[table].insert(0, row)
        _save(data)
    return row


# ============================================================
# 读取接口
# ============================================================
def get_works_by_user(user_id: str) -> List[Dict[str, Any]]:
    """按用户取作品列表，按提交时间倒序（新的在前）"""
    with _LOCK:
        data = _load()
    works = [w for w in data["works"] if str(w.get("user_id")) == str(user_id)]
    works.sort(key=lambda w: w.get("submitted_at", ""), reverse=True)
    return works


def query(table: str, **filters: Any) -> List[Dict[str, Any]]:
    """
    按等值条件查询某张表。

    用法:
        query("works", user_id="user_demo_001")
        query("works", unit_id="unit1", user_id="user_demo_001")
        query("works")            # 不带条件 = 全部
    """
    table = _check_table(table)
    with _LOCK:
        data = _load()
    rows = data.get(table, [])
    if not filters:
        return list(rows)
    return [
        r for r in rows
        if all(str(r.get(k)) == str(v) for k, v in filters.items())
    ]


def get_by_id(table: str, record_id: str) -> Optional[Dict[str, Any]]:
    """按主键取单条记录，找不到返回 None"""
    table = _check_table(table)
    with _LOCK:
        data = _load()
    for row in data.get(table, []):
        if str(row.get("id")) == str(record_id):
            return row
    return None


def count(table: str, **filters: Any) -> int:
    """统计条数"""
    return len(query(table, **filters))
