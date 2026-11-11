# -*- coding: utf-8 -*-
"""
components 包 - UI 组件模块
=============================
美食数字菜谱项目 - Streamlit UI 组件库

包含模块:
    - style:    全局样式注入
    - sidebar:  侧边导航栏
    - header:   顶部标题栏
    - cards:    各类卡片组件

使用示例:
    from components import inject_global_style, render_sidebar, render_header, unit_card
"""

from .style import inject_global_style, inject_component_css
from .sidebar import render_sidebar, get_page_title
from .header import render_header, render_user_info_bar, render_breadcrumb, render_section_title
from .cards import unit_card, work_card, task_card, question_card, stat_card

__all__ = [
    "inject_global_style",
    "inject_component_css",
    "render_sidebar",
    "get_page_title",
    "render_header",
    "render_user_info_bar",
    "render_breadcrumb",
    "render_section_title",
    "unit_card",
    "work_card",
    "task_card",
    "question_card",
    "stat_card",
]
