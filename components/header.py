# -*- coding: utf-8 -*-
"""
顶部标题栏组件模块
==================
提供 Streamlit 应用的顶部标题栏
包含：主标题、学生端/教师端身份切换 Tab、用户信息显示

使用方式:
    from components.header import render_header
    render_header(title="信息科技智能助教", role="student")
"""

import streamlit as st


def render_header(
    title: str = "信息科技智能助教｜七年级下册・美食数字菜谱项目",
    subtitle: str = "用代码烹饪美食，用科技点亮创意",
    current_role: str = "student",
    show_role_tabs: bool = True
) -> str:
    """
    渲染顶部标题栏

    参数:
        title: 主标题文字
        subtitle: 副标题文字
        current_role: 当前身份 - "student"（学生端）或 "teacher"（教师端）
        show_role_tabs: 是否显示身份切换 Tab

    返回:
        str: 当前选中的身份 "student" 或 "teacher"
    """
    # 初始化 session state
    if "current_role" not in st.session_state:
        st.session_state["current_role"] = current_role

    # 顶部标题栏 HTML
    header_html = f'''
    <div class="ms-header">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
            <div style="flex: 1; min-width: 200px;">
                <h1 style="color: white !important; font-size: 1.5rem; margin: 0; 
                           display: flex; align-items: center; gap: 0.75rem;">
                    <span style="font-size: 2rem;">🍳</span>
                    {title}
                </h1>
                <p class="subtitle" style="color: rgba(255,255,255,0.9); font-size: 0.9rem; 
                                          margin-top: 0.25rem; margin-left: 3rem;">
                    {subtitle}
                </p>
            </div>
    '''

    # 如果显示身份切换 Tab，添加到右侧
    if show_role_tabs:
        student_active = "active" if st.session_state["current_role"] == "student" else ""
        teacher_active = "active" if st.session_state["current_role"] == "teacher" else ""

        header_html += f'''
            <div class="ms-role-tabs">
                <div class="ms-role-tab {student_active}" id="role-student">
                    👨‍🎓 学生端
                </div>
                <div class="ms-role-tab {teacher_active}" id="role-teacher">
                    👨‍🏫 教师端
                </div>
            </div>
        '''

    header_html += '''
        </div>
    </div>
    '''

    st.markdown(header_html, unsafe_allow_html=True)

    # 身份切换（使用原生 button 实现交互）
    if show_role_tabs:
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button(
                "👨‍🎓 学生端",
                key="header_role_student",
                type="primary" if st.session_state["current_role"] == "student" else "secondary",
                use_container_width=True
            ):
                st.session_state["current_role"] = "student"
                st.rerun()
        with col2:
            if st.button(
                "👨‍🏫 教师端",
                key="header_role_teacher",
                type="primary" if st.session_state["current_role"] == "teacher" else "secondary",
                use_container_width=True
            ):
                st.session_state["current_role"] = "teacher"
                st.rerun()

    return st.session_state["current_role"]


def render_user_info_bar(user_name: str = "小明同学",
                         user_class: str = "七年级(3)班",
                         user_avatar: str = "小",
                         notification_count: int = 3):
    """
    渲染用户信息栏（显示在右上角）

    参数:
        user_name: 用户名
        user_class: 班级信息
        user_avatar: 头像文字（单字）
        notification_count: 未读通知数量
    """
    # 通知徽章 HTML
    if notification_count > 0:
        badge_html = f'''<span style="position: absolute; top: 0; right: 0; 
                        background-color: #e74c3c; color: white; 
                        font-size: 0.7rem; width: 18px; height: 18px; 
                        border-radius: 50%; display: flex; 
                        align-items: center; justify-content: center;
                        font-weight: bold;">{notification_count}</span>'''
    else:
        badge_html = ""

    user_bar_html = f'''
    <div style="display: flex; align-items: center; gap: 1rem; justify-content: flex-end; 
                margin-bottom: 1rem; padding: 0.5rem 1rem;">
        <div style="position: relative; cursor: pointer; padding: 0.5rem; 
                    border-radius: 50%;">
            <span style="font-size: 1.25rem;">🔔</span>
            {badge_html}
        </div>
        <div class="ms-user-info" style="padding: 0.5rem 0.75rem; cursor: pointer;">
            <div class="ms-avatar" style="width: 36px; height: 36px; 
                                          font-size: 1rem; margin-right: 0.5rem;">
                {user_avatar}
            </div>
            <div>
                <div style="font-weight: 600; font-size: 0.9rem;">{user_name}</div>
                <div style="font-size: 0.75rem; opacity: 0.7;">{user_class}</div>
            </div>
        </div>
    </div>
    '''
    st.markdown(user_bar_html, unsafe_allow_html=True)


def render_breadcrumb(items: list):
    """
    渲染面包屑导航

    参数:
        items: 面包屑项列表，每项为 dict:
            - "label": 显示文字
            - "href": 链接（可选，None 表示当前页）
            - "icon": 图标 emoji（可选）

    示例:
        render_breadcrumb([
            {"label": "首页", "icon": "🏠", "href": "home"},
            {"label": "单元一", "icon": "📚", "href": "unit1"},
            {"label": "数字菜谱设计", "icon": "📝"},
        ])
    """
    breadcrumb_parts = []

    for i, item in enumerate(items):
        icon = item.get("icon", "")
        label = item["label"]
        is_last = (i == len(items) - 1)

        if is_last:
            part = f'<span style="font-weight: 600;">{icon} {label}</span>'
        else:
            part = f'<span style="opacity: 0.6; cursor: pointer;">{icon} {label}</span>'

        breadcrumb_parts.append(part)

        # 添加分隔符
        if not is_last:
            breadcrumb_parts.append('<span style="opacity: 0.4; margin: 0 0.5rem;">›</span>')

    breadcrumb_html = f'''
    <div style="padding: 0.75rem 0; font-size: 0.9rem; display: flex; align-items: center; flex-wrap: wrap;">
        {"".join(breadcrumb_parts)}
    </div>
    '''
    st.markdown(breadcrumb_html, unsafe_allow_html=True)


def render_section_title(title: str, subtitle: str = "", icon: str = "",
                          action_text: str = "", action_key: str = "") -> bool:
    """
    渲染区块标题（带可选操作按钮）

    参数:
        title: 主标题
        subtitle: 副标题（可选）
        icon: 标题图标 emoji（可选）
        action_text: 操作按钮文字（可选）
        action_key: 操作按钮的 key（可选，需与 action_text 同时提供）

    返回:
        bool: 操作按钮是否被点击（如果有操作按钮）
    """
    clicked = False

    col1, col2 = st.columns([3, 1])

    with col1:
        icon_html = f'<span style="font-size: 1.5rem;">{icon}</span>' if icon else ''
        subtitle_html = f'<p style="margin: 0.25rem 0 0 0; opacity: 0.7; font-size: 0.9rem; margin-left: 2.5rem;">{subtitle}</p>' if subtitle else ''

        title_html = f'''
        <div style="margin: 1rem 0 0.5rem 0;">
            <h3 style="margin: 0; display: flex; align-items: center; gap: 0.5rem;">
                {icon_html}
                {title}
            </h3>
            {subtitle_html}
        </div>
        '''
        st.markdown(title_html, unsafe_allow_html=True)

    with col2:
        if action_text and action_key:
            clicked = st.button(action_text, key=action_key, use_container_width=True)

    return clicked
