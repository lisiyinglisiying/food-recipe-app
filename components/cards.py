# -*- coding: utf-8 -*-
"""
卡片组件模块
============
提供多种卡片组件：
- 单元入口大卡片（显示进度、徽章）
- 作品展示卡片（缩略图、版本、评价）
- 任务卡片
- 疑问卡片
- 统计卡片（辅助）

使用方式:
    from components.cards import unit_card, work_card, task_card, question_card
"""

import streamlit as st


# ============================================================
# 1. 单元入口大卡片
# ============================================================

def unit_card(
    unit_title: str,
    unit_subtitle: str = "",
    progress: float = 0.0,
    badges: list = None,
    unit_icon: str = "📚",
    is_locked: bool = False,
    card_key: str = ""
) -> bool:
    """
    渲染单元入口大卡片

    参数:
        unit_title: 单元标题
        unit_subtitle: 单元副标题/简介
        progress: 学习进度（0-1 之间的浮点数）
        badges: 徽章列表，每项为 dict: {"text": "徽章名", "type": "blue/orange/green/red"}
        unit_icon: 单元图标 emoji
        is_locked: 是否锁定（未解锁）
        card_key: 卡片唯一标识（用于 button key）

    返回:
        bool: 卡片是否被点击
    """
    if badges is None:
        badges = []

    progress_percent = int(min(max(progress, 0), 1) * 100)

    # 构建徽章 HTML
    badge_html_parts = []
    for b in badges:
        btype = b.get("type", "blue")
        badge_html_parts.append(
            f'<span class="ms-badge ms-badge-{btype}">{b["text"]}</span>'
        )
    badge_html = "".join(badge_html_parts)

    # 锁定状态遮罩
    lock_overlay = ""
    if is_locked:
        lock_overlay = '''
        <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; 
                    background: rgba(0,0,0,0.5); border-radius: 20px; z-index: 10;
                    display: flex; flex-direction: column; align-items: center; 
                    justify-content: center; color: white; backdrop-filter: blur(2px);">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🔒</div>
            <div style="font-weight: 600;">单元未解锁</div>
            <div style="font-size: 0.85rem; opacity: 0.8;">完成前序单元后解锁</div>
        </div>
        '''

    # 副标题 HTML
    subtitle_html = ""
    if unit_subtitle:
        subtitle_html = f'<p style="margin: 0 0 0.75rem 0; opacity: 0.7; font-size: 0.9rem;">{unit_subtitle}</p>'

    card_html = f'''
    <div class="ms-card-large" style="position: relative; cursor: {'pointer' if not is_locked else 'not-allowed'};">
        {lock_overlay}
        <div style="display: flex; align-items: flex-start; gap: 1rem; position: relative; z-index: 5;">
            <div style="font-size: 3rem; flex-shrink: 0;">{unit_icon}</div>
            <div style="flex: 1; min-width: 0;">
                <h3 style="margin: 0 0 0.25rem 0; font-size: 1.25rem;">{unit_title}</h3>
                {subtitle_html}
                <div style="margin-bottom: 0.75rem;">
                    {badge_html}
                </div>
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <div style="flex: 1;">
                        <div class="ms-progress-bar">
                            <div class="ms-progress-fill" style="width: {progress_percent}%;"></div>
                        </div>
                    </div>
                    <span style="font-size: 0.85rem; font-weight: 600; 
                                white-space: nowrap;">{progress_percent}%</span>
                </div>
                <div style="font-size: 0.8rem; opacity: 0.6; margin-top: 0.25rem;">
                    学习进度
                </div>
            </div>
            <div style="flex-shrink: 0; font-size: 1.5rem; opacity: 0.5;">→</div>
        </div>
    </div>
    '''

    st.markdown(card_html, unsafe_allow_html=True)

    # 使用 button 实现点击交互
    if not is_locked:
        button_key = f"unit_card_{card_key}" if card_key else f"unit_card_{unit_title}"
        clicked = st.button(
            f"进入「{unit_title}」",
            key=button_key,
            use_container_width=True,
            type="primary"
        )
        return clicked

    return False


# ============================================================
# 2. 作品展示卡片
# ============================================================

def work_card(
    work_title: str,
    version: str = "v1.0",
    rating: float = 0.0,
    thumbnail_emoji: str = "🍜",
    author: str = "",
    tags: list = None,
    is_featured: bool = False,
    card_key: str = ""
) -> bool:
    """
    渲染作品展示卡片

    参数:
        work_title: 作品名称
        version: 版本号
        rating: 评分（0-5 星）
        thumbnail_emoji: 缩略图 emoji 图标
        author: 作者名
        tags: 标签列表
        is_featured: 是否精选作品
        card_key: 卡片唯一标识

    返回:
        bool: 卡片是否被点击
    """
    if tags is None:
        tags = []

    # 星级显示
    full_stars = int(rating)
    has_half = (rating - full_stars) >= 0.5
    stars_parts = []
    for i in range(5):
        if i < full_stars:
            stars_parts.append("★")
        elif i == full_stars and has_half:
            stars_parts.append("☆")
        else:
            stars_parts.append('<span style="opacity: 0.3;">★</span>')
    stars_html = "".join(stars_parts)

    # 标签 HTML
    tags_html = "".join([f'<span class="ms-tag">{tag}</span>' for tag in tags])

    # 精选标识
    featured_badge = ""
    if is_featured:
        featured_badge = '''
        <div style="position: absolute; top: 0.75rem; right: 0.75rem; 
                    background: linear-gradient(135deg, #f1c40f, #e67e22);
                    color: white; padding: 0.25rem 0.6rem; border-radius: 20px;
                    font-size: 0.75rem; font-weight: 600; z-index: 5;">
            ⭐ 精选
        </div>
        '''

    # 作者信息
    author_html = ""
    if author:
        author_html = f'<div style="font-size: 0.8rem; opacity: 0.7; margin-bottom: 0.5rem;">👤 {author}</div>'

    card_html = f'''
    <div class="ms-work-card" style="position: relative; cursor: pointer;">
        {featured_badge}
        <div class="ms-work-thumbnail">
            <span style="font-size: 4rem;">{thumbnail_emoji}</span>
        </div>
        <div class="ms-work-body">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;
                        margin-bottom: 0.5rem;">
                <h4 style="margin: 0; font-size: 1rem; flex: 1;">{work_title}</h4>
                <span style="font-size: 0.75rem; opacity: 0.6; background: rgba(0,0,0,0.05);
                            padding: 0.2rem 0.5rem; border-radius: 4px; flex-shrink: 0;
                            margin-left: 0.5rem;">{version}</span>
            </div>
            <div class="ms-rating" style="margin-bottom: 0.5rem;">
                {stars_html}
                <span style="font-size: 0.85rem; opacity: 0.7; margin-left: 0.5rem;">{rating:.1f}</span>
            </div>
            {author_html}
            <div style="margin-top: 0.5rem;">
                {tags_html}
            </div>
        </div>
    </div>
    '''

    st.markdown(card_html, unsafe_allow_html=True)

    button_key = f"work_card_{card_key}" if card_key else f"work_card_{work_title}"
    clicked = st.button(
        "查看作品详情",
        key=button_key,
        use_container_width=True
    )
    return clicked


# ============================================================
# 3. 任务卡片
# ============================================================

def task_card(
    task_title: str,
    task_description: str = "",
    task_type: str = "normal",
    status: str = "pending",
    points: int = 0,
    deadline: str = "",
    task_icon: str = "📝",
    card_key: str = ""
) -> bool:
    """
    渲染任务卡片

    参数:
        task_title: 任务标题
        task_description: 任务描述
        task_type: 任务类型 - "normal"（普通）/ "challenge"（挑战）/ "daily"（每日）
        status: 任务状态 - "pending"（进行中）/ "completed"（已完成）/ "urgent"（紧急）
        points: 奖励积分
        deadline: 截止时间文字
        task_icon: 任务图标 emoji
        card_key: 卡片唯一标识

    返回:
        bool: 卡片是否被点击
    """
    # 状态样式
    status_class = ""
    status_text = ""
    status_color = ""

    if status == "completed":
        status_class = "completed"
        status_text = "✓ 已完成"
        status_color = "#27ae60"
    elif status == "urgent":
        status_class = "urgent"
        status_text = "🔥 紧急"
        status_color = "#e74c3c"
    else:
        status_text = "进行中"
        status_color = "#3498db"

    # 任务类型标签
    type_labels = {
        "normal": ("普通任务", "blue"),
        "challenge": ("挑战任务", "orange"),
        "daily": ("每日任务", "green"),
    }
    type_label, type_color = type_labels.get(task_type, ("普通任务", "blue"))

    # 描述 HTML
    desc_html = ""
    if task_description:
        desc_html = f'<p style="margin: 0 0 0.75rem 0; opacity: 0.7; font-size: 0.85rem; line-height: 1.5;">{task_description}</p>'

    # 截止时间 HTML
    deadline_html = ""
    if deadline:
        deadline_html = f'<span style="opacity: 0.7;">⏰ {deadline}</span>'

    card_html = f'''
    <div class="ms-task-card {status_class}" style="cursor: pointer;">
        <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
            <div style="font-size: 1.5rem; flex-shrink: 0;">{task_icon}</div>
            <div style="flex: 1; min-width: 0;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;
                            margin-bottom: 0.5rem; flex-wrap: wrap; gap: 0.5rem;">
                    <h4 style="margin: 0; font-size: 1rem;">{task_title}</h4>
                    <span class="ms-badge ms-badge-{type_color}" style="margin: 0;">{type_label}</span>
                </div>
                {desc_html}
                <div style="display: flex; justify-content: space-between; align-items: center;
                            font-size: 0.85rem; flex-wrap: wrap; gap: 0.5rem;">
                    <div>
                        {deadline_html}
                    </div>
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <span style="color: #e67e22; font-weight: 600;">+{points} 积分</span>
                        <span style="color: {status_color}; font-weight: 500;">{status_text}</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    '''

    st.markdown(card_html, unsafe_allow_html=True)

    button_key = f"task_card_{card_key}" if card_key else f"task_card_{task_title}"
    button_text = "查看详情" if status != "completed" else "再次查看"
    clicked = st.button(
        button_text,
        key=button_key,
        use_container_width=True
    )
    return clicked


# ============================================================
# 4. 疑问卡片
# ============================================================

def question_card(
    question_title: str,
    question_content: str = "",
    author: str = "匿名同学",
    reply_count: int = 0,
    view_count: int = 0,
    tags: list = None,
    is_resolved: bool = False,
    time_ago: str = "",
    card_key: str = ""
) -> bool:
    """
    渲染疑问卡片

    参数:
        question_title: 问题标题
        question_content: 问题内容（摘要）
        author: 提问者
        reply_count: 回答数量
        view_count: 浏览数量
        tags: 标签列表
        is_resolved: 是否已解决
        time_ago: 发布时间描述（如 "2小时前"）
        card_key: 卡片唯一标识

    返回:
        bool: 卡片是否被点击
    """
    if tags is None:
        tags = []

    # 标签 HTML
    tags_html = "".join([f'<span class="ms-tag">{tag}</span>' for tag in tags])

    # 解决状态标识
    if is_resolved:
        resolved_badge = '<span class="ms-badge ms-badge-green">✓ 已解决</span>'
    else:
        resolved_badge = '<span class="ms-badge ms-badge-orange">待解答</span>'

    # 问题内容截断
    content_display = question_content
    if len(content_display) > 80:
        content_display = content_display[:80] + "..."

    # 内容 HTML
    content_html = ""
    if content_display:
        content_html = f'<p style="margin: 0 0 0.75rem 0; opacity: 0.75; font-size: 0.9rem; line-height: 1.6; padding-left: 1.5rem;">{content_display}</p>'

    # 时间 HTML
    time_html = f' · {time_ago}' if time_ago else ''

    card_html = f'''
    <div class="ms-question-card" style="cursor: pointer;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;
                    margin-bottom: 0.5rem; gap: 0.5rem;">
            <h4 style="margin: 0; font-size: 1rem; flex: 1;">
                <span style="margin-right: 0.5rem;">❓</span>
                {question_title}
            </h4>
            {resolved_badge}
        </div>
        {content_html}
        <div style="margin-bottom: 0.75rem; padding-left: 1.5rem;">
            {tags_html}
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center;
                    font-size: 0.8rem; opacity: 0.7; flex-wrap: wrap; gap: 0.5rem;">
            <div>
                👤 {author}{time_html}
            </div>
            <div style="display: flex; gap: 1rem;">
                <span>💬 {reply_count} 回答</span>
                <span>👁️ {view_count} 浏览</span>
            </div>
        </div>
    </div>
    '''

    st.markdown(card_html, unsafe_allow_html=True)

    button_key = f"question_card_{card_key}" if card_key else f"question_card_{question_title}"
    clicked = st.button(
        "查看问题详情",
        key=button_key,
        use_container_width=True
    )
    return clicked


# ============================================================
# 5. 统计卡片（辅助组件）
# ============================================================

def stat_card(
    label: str,
    value: str,
    icon: str = "📊",
    trend: str = "",
    trend_type: str = "up",
    card_key: str = ""
):
    """
    渲染统计数据卡片

    参数:
        label: 标签文字
        value: 数值
        icon: 图标 emoji
        trend: 趋势描述文字（如 "+12%"）
        trend_type: 趋势类型 - "up"（上升）/ "down"（下降）/ "neutral"（持平）
        card_key: 卡片唯一标识
    """
    # 趋势颜色
    trend_colors = {
        "up": "#27ae60",
        "down": "#e74c3c",
        "neutral": "#7f8c8d",
    }
    trend_color = trend_colors.get(trend_type, "#7f8c8d")

    # 趋势图标
    trend_icons = {
        "up": "↑",
        "down": "↓",
        "neutral": "→",
    }
    trend_icon = trend_icons.get(trend_type, "→")

    # 趋势 HTML
    trend_html = ""
    if trend:
        trend_html = f'''<div style="margin-top: 0.5rem; font-size: 0.85rem; color: {trend_color};">
            {trend_icon} {trend}
        </div>'''

    card_html = f'''
    <div class="ms-card" style="text-align: center;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
        <div style="font-size: 2rem; font-weight: bold; 
                    background: linear-gradient(135deg, #3498db, #e67e22);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                    background-clip: text;
                    margin-bottom: 0.25rem;">
            {value}
        </div>
        <div style="font-size: 0.9rem; opacity: 0.7;">{label}</div>
        {trend_html}
    </div>
    '''

    st.markdown(card_html, unsafe_allow_html=True)
