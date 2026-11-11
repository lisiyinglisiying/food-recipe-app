# -*- coding: utf-8 -*-
"""
我的成长档案页面
================
记录学生在美食数字菜谱项目中的学习轨迹和成长历程

功能模块：
    1. 学习统计卡片 - 总作品数、总学习时长、获得徽章数、参与互动数
    2. 美食项目达成雷达图 - 4个能力维度（网页制作、数据分析、AI规范使用、资源整理）
    3. 项目式成长档案袋 - 时间线展示全套作品
    4. 单元闯关成长徽章 - 4个单元徽章
    5. 项目自评量表 - 每单元自评记录与迭代改进想法

页面入口：
    render() - 由 app.py 动态调用渲染
"""

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

# ===== 导入项目组件与工具 =====
from components.cards import stat_card
from components.header import render_section_title


# ============================================================
# 📊 模块一：学习统计卡片
# ============================================================
def render_stats_cards(user_info):
    """
    渲染顶部学习统计卡片
    展示：总作品数、总学习时长、获得徽章数、参与互动数

    参数:
        user_info: 当前登录用户信息字典
    """
    render_section_title(
        title="📊 我的学习数据",
        subtitle="看看你在美食数字菜谱项目中取得了多少进步！",
        icon="📈"
    )

    # 获取统计数据
    stats_data = _get_user_stats(user_info)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        stat_card(
            label="已完成作品",
            value=str(stats_data["total_works"]),
            icon="🎨",
            trend="+2 本周",
            trend_type="up"
        )

    with col2:
        stat_card(
            label="累计学习时长",
            value=f"{stats_data['total_hours']}小时",
            icon="⏱️",
            trend="+3h 本周",
            trend_type="up"
        )

    with col3:
        stat_card(
            label="获得徽章",
            value=str(stats_data["total_badges"]),
            icon="🏅",
            trend="+1 本周",
            trend_type="up"
        )

    with col4:
        stat_card(
            label="参与互动",
            value=str(stats_data["total_interactions"]),
            icon="💬",
            trend="+5 本周",
            trend_type="up"
        )

    st.markdown("<br>", unsafe_allow_html=True)


def _get_user_stats(user_info):
    """
    获取用户统计数据（优先从存储读取，失败则使用演示数据）

    返回:
        dict: 包含各项统计数据
    """
    try:
        from utils.storage import get_works_by_user
        from utils.obe_tracker import get_student_portfolio

        if user_info and user_info.get("id"):
            works = get_works_by_user(user_info["id"])
            portfolio = get_student_portfolio(user_info["id"])
            works_summary = portfolio.get("works_summary", {})
            badges_summary = portfolio.get("badges_summary", {})

            return {
                "total_works": works_summary.get("total_count", len(works)),
                "total_hours": works_summary.get("total_count", 0) * 2 + 6,
                "total_badges": badges_summary.get("total_count", 0),
                "total_interactions": len(works) * 2 + 8,
            }
    except Exception:
        pass  # 获取失败时使用默认演示数据

    # 默认演示数据（适合低龄学生）
    return {
        "total_works": 8,
        "total_hours": 24,
        "total_badges": 3,
        "total_interactions": 25,
    }


# ============================================================
# 🎯 模块二：美食项目达成雷达图
# ============================================================
def render_radar_chart(user_info):
    """
    渲染美食项目达成雷达图
    4个维度：网页制作能力、数据分析能力、AI规范使用能力、资源整理能力
    使用 plotly 绘制雷达图，低龄友好的配色和标注

    参数:
        user_info: 当前登录用户信息
    """
    render_section_title(
        title="🎯 美食项目能力雷达图",
        subtitle="四大能力维度，看看你的强项在哪里？",
        icon="🕸️"
    )

    # 获取雷达图数据
    radar_data = _get_radar_data(user_info)

    # 两栏布局
    col_chart, col_detail = st.columns([2, 1])

    with col_chart:
        # 使用 plotly 绘制雷达图
        fig = go.Figure()

        categories = radar_data["categories"]
        scores = radar_data["scores"]
        target_scores = [100] * len(categories)

        # 当前能力曲线
        fig.add_trace(go.Scatterpolar(
            r=scores + [scores[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name='我的能力',
            fillcolor='rgba(74, 144, 217, 0.3)',
            line=dict(color='#4A90D9', width=3),
            marker=dict(size=8, color='#4A90D9'),
            hovertemplate='<b>%{theta}</b><br>得分：%{r} 分<extra></extra>',
        ))

        # 目标参考线
        fig.add_trace(go.Scatterpolar(
            r=target_scores + [target_scores[0]],
            theta=categories + [categories[0]],
            fill='none',
            name='目标',
            line=dict(color='#FF9F6B', width=2, dash='dash'),
            marker=dict(size=4, color='#FF9F6B'),
            hovertemplate='<b>%{theta}</b><br>目标：%{r} 分<extra></extra>',
        ))

        # 雷达图布局
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickvals=[20, 40, 60, 80, 100],
                    ticktext=['20分', '40分', '60分', '80分', '100分'],
                    gridcolor='#E0E0E0',
                    tickfont=dict(size=10, color='#7F8C8D'),
                ),
                angularaxis=dict(
                    tickfont=dict(size=13, color='#2C3E50', family='Microsoft YaHei'),
                    gridcolor='#E0E0E0',
                    linecolor='#BDC3C7',
                ),
                bgcolor='#FAFAFA',
            ),
            showlegend=True,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1,
                font=dict(size=12, family='Microsoft YaHei'),
            ),
            height=480,
            margin=dict(l=40, r=40, t=60, b=40),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )

        st.plotly_chart(fig, use_container_width=True)
        st.caption("💡 小提示：完成每个单元的任务和作品，你的能力值就会提升哦！")

    with col_detail:
        # 各项能力详情
        st.markdown("#### 📋 能力详情")

        ability_details = radar_data["details"]
        for ability in ability_details:
            score = ability["score"]
            level = ability["level"]
            level_color = ability["level_color"]

            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {ability['color']}15, {ability['color']}08);
                        border-radius: 12px; padding: 1rem; margin-bottom: 0.75rem;
                        border-left: 4px solid {ability['color']};">
                <div style="display: flex; justify-content: space-between; align-items: center;
                            margin-bottom: 0.5rem;">
                    <div style="font-weight: 600; font-size: 1rem;">
                        {ability['icon']} {ability['name']}
                    </div>
                    <span style="font-size: 1.25rem; font-weight: bold; color: {ability['color']};">
                        {score}分
                    </span>
                </div>
                <div style="height: 8px; background: rgba(0,0,0,0.1); border-radius: 4px;
                            margin-bottom: 0.5rem; overflow: hidden;">
                    <div style="height: 100%; width: {score}%; 
                                background: linear-gradient(90deg, {ability['color']}, {ability['color']}CC);
                                border-radius: 4px;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem;">
                    <span style="opacity: 0.7;">{ability['description']}</span>
                    <span style="color: {level_color}; font-weight: 500;">{level}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # 总体评价
        total_score = sum(radar_data["scores"]) / len(radar_data["scores"])
        if total_score >= 80:
            overall_comment = "🌟 太棒了！你是全能型美食数字小达人！"
            overall_color = "#27ae60"
        elif total_score >= 60:
            overall_comment = "👍 很不错！继续努力，均衡发展哦～"
            overall_color = "#3498db"
        elif total_score >= 40:
            overall_comment = "🌱 加油！每个能力都在成长中！"
            overall_color = "#f39c12"
        else:
            overall_comment = "💪 刚开始学习，一步一步来！"
            overall_color = "#e74c3c"

        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: {overall_color}15;
                    border-radius: 12px; border: 2px solid {overall_color}30;">
            <div style="font-weight: 600; color: {overall_color}; font-size: 1.05rem;">
                {overall_comment}
            </div>
            <div style="font-size: 0.85rem; opacity: 0.7; margin-top: 0.25rem;">
                综合能力得分：{total_score:.0f} 分
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


def _get_radar_data(user_info):
    """
    获取雷达图数据（4个 IT 美食项目维度）

    返回:
        dict: 包含 categories, scores, details
    """
    try:
        from utils.obe_tracker import calculate_literacy_scores
        if user_info and user_info.get("id"):
            scores = calculate_literacy_scores(user_info["id"])
            web_score = max(int(scores.get("图像识读", 0)), 35)
            data_score = max(int(scores.get("审美判断", 0)), 45)
            ai_score = max(int(scores.get("创意实践", 0)), 25)
            resource_score = max(int(scores.get("文化理解", 0)), 20)
        else:
            raise ValueError("未登录")
    except Exception:
        # 默认演示数据
        web_score = 75
        data_score = 60
        ai_score = 40
        resource_score = 35

    def get_level(score):
        if score >= 80:
            return "优秀 ⭐", "#27ae60"
        elif score >= 60:
            return "良好 👍", "#3498db"
        elif score >= 40:
            return "进步中 🌱", "#f39c12"
        else:
            return "待加油 💪", "#e74c3c"

    categories = [
        "网页制作能力",
        "数据分析能力",
        "AI规范使用能力",
        "资源整理能力",
    ]

    scores = [web_score, data_score, ai_score, resource_score]

    details = [
        {
            "name": "网页制作能力",
            "icon": "🌐",
            "score": web_score,
            "color": "#4A90D9",
            "description": "用 Markdown/HTML 做美食网页",
            "level": get_level(web_score)[0],
            "level_color": get_level(web_score)[1],
        },
        {
            "name": "数据分析能力",
            "icon": "📊",
            "score": data_score,
            "color": "#FF9F6B",
            "description": "收集和可视化菜谱数据",
            "level": get_level(data_score)[0],
            "level_color": get_level(data_score)[1],
        },
        {
            "name": "AI规范使用能力",
            "icon": "🤖",
            "score": ai_score,
            "color": "#67C28A",
            "description": "正确使用 AI 工具辅助创作",
            "level": get_level(ai_score)[0],
            "level_color": get_level(ai_score)[1],
        },
        {
            "name": "资源整理能力",
            "icon": "📚",
            "score": resource_score,
            "color": "#9B59B6",
            "description": "整理和分享跨学科资源",
            "level": get_level(resource_score)[0],
            "level_color": get_level(resource_score)[1],
        },
    ]

    return {"categories": categories, "scores": scores, "details": details}


# ============================================================
# 📁 模块三：项目式成长档案袋（时间线）
# ============================================================
def render_portfolio_timeline(user_info):
    """
    渲染项目式成长档案袋
    以时间线形式展示学生从网页→数据菜谱→AI菜谱→资源库的全套作品
    """
    render_section_title(
        title="📁 项目式成长档案袋",
        subtitle="一步一个脚印，看看你的美食数字成长之路！",
        icon="🗂️"
    )

    portfolio_items = _get_portfolio_items(user_info)

    # 时间线样式
    st.markdown("""
    <style>
    .ms-timeline { position: relative; padding-left: 2rem; }
    .ms-timeline::before {
        content: ''; position: absolute; left: 18px; top: 0; bottom: 0;
        width: 3px;
        background: linear-gradient(180deg, #4A90D9, #FF9F6B, #67C28A, #9B59B6);
        border-radius: 2px;
    }
    .timeline-item { position: relative; margin-bottom: 1.5rem; }
    .timeline-dot {
        position: absolute; left: -2rem; top: 0.5rem;
        width: 36px; height: 36px; border-radius: 50%;
        background: white; display: flex;
        align-items: center; justify-content: center;
        font-size: 1rem; z-index: 2;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="ms-timeline">', unsafe_allow_html=True)

    for idx, item in enumerate(portfolio_items):
        dot_colors = ["#4A90D9", "#FF9F6B", "#67C28A", "#9B59B6"]
        dot_color = dot_colors[idx % len(dot_colors)]

        st.markdown(f"""
        <div class="timeline-item">
            <div class="timeline-dot" style="border: 3px solid {dot_color};">
                {item['unit_icon']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="margin-bottom: 0.75rem; margin-left: 0.5rem;">
            <span style="font-weight: 600; color: {dot_color}; font-size: 1.05rem;">
                {item['unit_name']}
            </span>
            <span style="opacity: 0.6; font-size: 0.85rem; margin-left: 0.5rem;">
                {item['time_period']}
            </span>
            <span class="ms-badge ms-badge-blue" style="margin-left: 0.5rem;">
                {item['work_count']} 个作品
            </span>
        </div>
        """, unsafe_allow_html=True)

        # 作品卡片
        work_cols = st.columns(min(len(item["works"]), 3))
        for i, work in enumerate(item["works"][:3]):
            with work_cols[i]:
                st.markdown(f"""
                <div style="background: white; border-radius: 12px; padding: 0.75rem;
                            border: 1px solid #E9ECEF; margin-bottom: 0.5rem; text-align: center;">
                    <div style="font-size: 1.75rem; margin-bottom: 0.5rem;">{work['emoji']}</div>
                    <div style="font-weight: 500; font-size: 0.9rem; margin-bottom: 0.25rem;">
                        {work['title']}
                    </div>
                    <div style="font-size: 0.75rem; opacity: 0.6;">
                        {work['version']} · {work['date']}
                    </div>
                    <div style="margin-top: 0.5rem;">
                        <span style="font-size: 0.7rem; color: #FF9F6B;">
                            {'⭐' * work['rating']}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"查看作品", key=f"view_work_{idx}_{i}", use_container_width=True):
                    st.info(f"📖 正在打开「{work['title']}」……")

        if len(item["works"]) > 3:
            if st.button(f"查看全部 {item['work_count']} 个作品 →",
                         key=f"view_more_{idx}", use_container_width=True):
                st.info(f"📂 展开全部作品……")

        st.markdown("---")

    st.markdown('</div>', unsafe_allow_html=True)

    # 底部鼓励
    total_works = sum(item['work_count'] for item in portfolio_items)
    st.markdown(f"""
    <div style="text-align: center; padding: 1.5rem;
                background: linear-gradient(135deg, #E8F4FD, #FFF0E6);
                border-radius: 16px;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎓</div>
        <div style="font-weight: 600; font-size: 1.1rem; color: #2C3E50;">
            你已经完成了 {total_works} 个美食数字作品！
        </div>
        <div style="font-size: 0.9rem; opacity: 0.7; margin-top: 0.5rem;">
            每一个作品都是你成长的见证，继续加油！ 💪
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


def _get_portfolio_items(user_info):
    """获取成长档案袋数据（时间线数据）"""
    try:
        from utils.storage import get_works_by_user
        if user_info and user_info.get("id"):
            works = get_works_by_user(user_info["id"])
            unit_works = {}
            for w in works:
                uid = w.get("unit_id", "unit1")
                if uid not in unit_works:
                    unit_works[uid] = []
                unit_works[uid].append(w)
    except Exception:
        unit_works = {}

    units_config = [
        {
            "unit_id": "unit1",
            "unit_name": "第一单元·用网页展示美食",
            "unit_icon": "🌐",
            "time_period": "第1-2周",
            "default_works": [
                {"title": "番茄炒蛋介绍页", "emoji": "🍅", "version": "v1.0", "date": "3月5日", "rating": 4},
                {"title": "家乡美食展示站", "emoji": "🥟", "version": "v2.0", "date": "3月10日", "rating": 5},
                {"title": "美食文化网页", "emoji": "🍜", "version": "v1.5", "date": "3月12日", "rating": 4},
            ],
        },
        {
            "unit_id": "unit2",
            "unit_name": "第二单元·有趣的数字菜谱",
            "unit_icon": "📊",
            "time_period": "第3-4周",
            "default_works": [
                {"title": "班级美食调查表", "emoji": "📋", "version": "v1.0", "date": "3月20日", "rating": 4},
                {"title": "菜谱数据可视化报告", "emoji": "📊", "version": "v2.0", "date": "3月25日", "rating": 5},
                {"title": "食堂菜单优化方案", "emoji": "🍽️", "version": "v1.0", "date": "3月28日", "rating": 4},
            ],
        },
        {
            "unit_id": "unit3",
            "unit_name": "第三单元·智能的数字菜谱",
            "unit_icon": "🤖",
            "time_period": "第5-6周",
            "default_works": [
                {"title": "AI 美食推荐小助手", "emoji": "🤖", "version": "v1.0", "date": "4月5日", "rating": 3},
                {"title": "智能营养搭配方案", "emoji": "🥗", "version": "v1.0", "date": "4月10日", "rating": 4},
            ],
        },
        {
            "unit_id": "unit4",
            "unit_name": "第四单元·跨学科主题资源库",
            "unit_icon": "📚",
            "time_period": "第7-8周",
            "default_works": [
                {"title": "美食与地理资源包", "emoji": "🌍", "version": "v0.5", "date": "4月18日", "rating": 3},
            ],
        },
    ]

    result = []
    for unit in units_config:
        uid = unit["unit_id"]
        if uid in unit_works and len(unit_works[uid]) > 0:
            works_list = []
            for w in unit_works[uid][:5]:
                works_list.append({
                    "title": w.get("title", "未命名作品"),
                    "emoji": "📄",
                    "version": w.get("version", "v1.0"),
                    "date": w.get("created_at", "")[:10] if w.get("created_at") else "未知",
                    "rating": min(w.get("teacher_score", 80) // 20, 5) if w.get("teacher_score") else 4,
                })
            result.append({**unit, "works": works_list, "work_count": len(unit_works[uid])})
        else:
            result.append({**unit, "works": unit["default_works"], "work_count": len(unit["default_works"])})

    return result


# ============================================================
# 🏅 模块四：单元闯关成长徽章
# ============================================================
def render_badges(user_info):
    """
    渲染单元闯关成长徽章
    4个徽章：美食记录者、数据分析师、AI善用者、资源管理员
    """
    render_section_title(
        title="🏅 单元闯关成长徽章",
        subtitle="完成每个单元的学习任务，解锁专属徽章！",
        icon="🎖️"
    )

    badges_config = [
        {
            "id": "food_recorder",
            "name": "美食记录者",
            "unit": "第一单元",
            "icon": "🌐",
            "color": "#4A90D9",
            "description": "用网页记录美食，掌握网页制作基础",
            "condition": "完成第一单元所有任务并提交作品",
            "unlocked": True,
            "unlock_date": "2024-03-15",
        },
        {
            "id": "data_analyst",
            "name": "数据分析师",
            "unit": "第二单元",
            "icon": "📊",
            "color": "#FF9F6B",
            "description": "收集和分析菜谱数据，制作数据可视化报告",
            "condition": "完成第二单元数据采集与可视化任务",
            "unlocked": True,
            "unlock_date": "2024-03-28",
        },
        {
            "id": "ai_master",
            "name": "AI善用者",
            "unit": "第三单元",
            "icon": "🤖",
            "color": "#67C28A",
            "description": "规范使用AI工具，创作智能美食项目",
            "condition": "完成第三单元AI菜谱相关任务",
            "unlocked": False,
            "unlock_date": None,
        },
        {
            "id": "resource_manager",
            "name": "资源管理员",
            "unit": "第四单元",
            "icon": "📚",
            "color": "#9B59B6",
            "description": "整合跨学科资源，建立美食主题资源库",
            "condition": "完成第四单元资源库建设任务",
            "unlocked": False,
            "unlock_date": None,
        },
    ]

    col1, col2 = st.columns(2)
    cols = [col1, col2, col1, col2]

    for i, badge in enumerate(badges_config):
        with cols[i]:
            if badge["unlocked"]:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, {badge['color']}20, {badge['color']}08);
                            border-radius: 16px; padding: 1.5rem; text-align: center;
                            border: 2px solid {badge['color']}40; margin-bottom: 1rem;
                            position: relative;">
                    <div style="position: absolute; top: 0.75rem; right: 0.75rem;
                                background: #27ae60; color: white; padding: 0.2rem 0.6rem;
                                border-radius: 20px; font-size: 0.75rem; font-weight: 500;">
                        ✓ 已获得
                    </div>
                    <div style="font-size: 3.5rem; margin-bottom: 0.75rem;">
                        {badge['icon']}
                    </div>
                    <div style="font-weight: bold; font-size: 1.2rem; color: {badge['color']};
                                margin-bottom: 0.25rem;">
                        {badge['name']}
                    </div>
                    <div style="font-size: 0.85rem; opacity: 0.7; margin-bottom: 0.75rem;">
                        {badge['unit']}
                    </div>
                    <div style="font-size: 0.9rem; line-height: 1.5; margin-bottom: 0.75rem;">
                        {badge['description']}
                    </div>
                    <div style="font-size: 0.8rem; opacity: 0.6;">
                        🎉 获得时间：{badge['unlock_date']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: #F5F5F5; border-radius: 16px; padding: 1.5rem;
                            text-align: center; border: 2px dashed #BDC3C7;
                            margin-bottom: 1rem; position: relative;">
                    <div style="position: absolute; top: 0.75rem; right: 0.75rem;
                                background: #95A5A6; color: white; padding: 0.2rem 0.6rem;
                                border-radius: 20px; font-size: 0.75rem; font-weight: 500;">
                        🔒 未解锁
                    </div>
                    <div style="font-size: 3.5rem; margin-bottom: 0.75rem; opacity: 0.3;">
                        {badge['icon']}
                    </div>
                    <div style="font-weight: bold; font-size: 1.2rem; color: #7F8C8D;
                                margin-bottom: 0.25rem;">
                        {badge['name']}
                    </div>
                    <div style="font-size: 0.85rem; opacity: 0.6; margin-bottom: 0.75rem;">
                        {badge['unit']}
                    </div>
                    <div style="font-size: 0.9rem; line-height: 1.5; margin-bottom: 0.75rem;
                                color: #7F8C8D;">
                        {badge['description']}
                    </div>
                    <div style="font-size: 0.8rem; opacity: 0.6; padding: 0.5rem;
                                background: white; border-radius: 8px;">
                        📋 解锁条件：{badge['condition']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # 徽章收集进度
    unlocked_count = sum(1 for b in badges_config if b["unlocked"])
    total_count = len(badges_config)
    progress = unlocked_count / total_count

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #E8F4FD, #FFF0E6);
                border-radius: 12px; padding: 1rem; text-align: center;">
        <div style="font-weight: 600; margin-bottom: 0.5rem;">
            🏅 徽章收集进度：{unlocked_count} / {total_count}
        </div>
        <div style="height: 10px; background: rgba(0,0,0,0.1); border-radius: 5px;
                    overflow: hidden;">
            <div style="height: 100%; width: {progress * 100}%;
                        background: linear-gradient(90deg, #4A90D9, #FF9F6B);
                        border-radius: 5px;"></div>
        </div>
        <div style="font-size: 0.85rem; opacity: 0.7; margin-top: 0.5rem;">
            还差 {total_count - unlocked_count} 个徽章就能集齐啦！加油～ 💪
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# 📝 模块五：项目自评量表
# ============================================================
def render_self_assessment(user_info):
    """
    渲染项目自评量表
    展示每单元自评记录和迭代改进想法
    """
    render_section_title(
        title="📝 项目自评量表",
        subtitle="每完成一个单元，给自己打个分，写下改进想法～",
        icon="📋"
    )

    assessments = _get_self_assessments(user_info)

    tab_titles = [f"{a['unit_icon']} {a['unit_name']}" for a in assessments]
    tabs = st.tabs(tab_titles)

    for i, (tab, asm) in enumerate(zip(tabs, assessments)):
        with tab:
            col_score, col_desc = st.columns([1, 2])

            with col_score:
                st.markdown(f"""
                <div style="text-align: center; padding: 1.5rem;
                            background: linear-gradient(135deg, {asm['color']}20, {asm['color']}08);
                            border-radius: 16px;">
                    <div style="font-size: 2.5rem; font-weight: bold; color: {asm['color']};">
                        {asm['score']}
                    </div>
                    <div style="font-size: 0.85rem; opacity: 0.7;">自评得分 / 5分</div>
                    <div style="margin-top: 0.5rem; font-size: 1rem;">
                        {'⭐' * asm['score']}{'☆' * (5 - asm['score'])}
                    </div>
                    <div style="font-size: 0.8rem; color: {asm['color']}; margin-top: 0.25rem;
                                font-weight: 500;">
                        {asm['level_text']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_desc:
                st.markdown("#### 📝 我的收获")
                st.success(f"✨ {asm['gains']}")

                st.markdown("#### 💡 可以改进的地方")
                st.info(f"🔧 {asm['improvements']}")

                st.markdown("#### 🎯 下一个目标")
                st.warning(f"🚀 {asm['next_goal']}")

            st.markdown("---")

            # 分项自评
            st.markdown("#### 📊 分项自评")
            for dim in asm["dimensions"]:
                col_dim, col_stars, col_note = st.columns([2, 1, 3])
                with col_dim:
                    st.markdown(f"**{dim['name']}**")
                with col_stars:
                    st.markdown(f"{'⭐' * dim['score']}{'☆' * (5 - dim['score'])}")
                with col_note:
                    st.caption(dim["note"])

            st.markdown("---")

            # 版本迭代记录
            st.markdown("#### 🔄 作品迭代记录")
            for j, version in enumerate(asm["version_history"]):
                with st.expander(
                    f"{'📌' if j == 0 else '📝'} {version['version']} ｜ "
                    f"{version['date']} ｜ {'最新版' if j == 0 else ''}",
                    expanded=(j == 0)
                ):
                    st.markdown(f"**修改内容：** {version['changes']}")
                    st.markdown(f"**改进想法：** {version['idea']}")

            if st.button(f"✏️ 修改本单元自评", key=f"edit_assessment_{i}",
                         use_container_width=True):
                st.info("📝 自评编辑功能……（演示）")

    st.markdown("<br>", unsafe_allow_html=True)


def _get_self_assessments(user_info):
    """获取自评数据"""
    return [
        {
            "unit_name": "第一单元·网页展示",
            "unit_icon": "🌐",
            "color": "#4A90D9",
            "score": 4,
            "level_text": "良好",
            "gains": "学会了用 Markdown 制作网页，知道了图片版权的重要性，还做出了自己的美食介绍页面！",
            "improvements": "排版可以更好看一些，图片可以更丰富，还想学习更多网页设计技巧。",
            "next_goal": "学习 CSS 样式，让网页更漂亮！",
            "dimensions": [
                {"name": "网页制作技能", "score": 4, "note": "会用 Markdown 基本语法"},
                {"name": "内容完整性", "score": 5, "note": "图片、文字、介绍都很完整"},
                {"name": "版权意识", "score": 4, "note": "知道要标注图片来源"},
                {"name": "创意设计", "score": 3, "note": "可以再独特一些"},
            ],
            "version_history": [
                {
                    "version": "v2.0 最终版",
                    "date": "3月12日",
                    "changes": "增加了更多菜品介绍，优化了排版，添加了食材表格",
                    "idea": "下次想试试添加更多互动元素，比如点击展开的效果",
                },
                {
                    "version": "v1.0 初稿",
                    "date": "3月5日",
                    "changes": "完成了基本的美食介绍页面，包含标题、图片和文字介绍",
                    "idea": "内容有点少，需要增加更多菜品和详细介绍",
                },
            ],
        },
        {
            "unit_name": "第二单元·数字菜谱",
            "unit_icon": "📊",
            "color": "#FF9F6B",
            "score": 4,
            "level_text": "良好",
            "gains": "学会了设计调查问卷，能用表格整理数据，还会做饼图和柱状图！数据真的很有趣！",
            "improvements": "数据样本还不够多，图表类型可以更丰富，分析深度还可以加强。",
            "next_goal": "尝试用数据解决更多实际问题，比如给食堂提建议！",
            "dimensions": [
                {"name": "数据采集", "score": 4, "note": "设计了完整的调查问卷"},
                {"name": "数据录入", "score": 5, "note": "表格填写规范整齐"},
                {"name": "数据可视化", "score": 4, "note": "饼图柱状图都做得不错"},
                {"name": "数据分析", "score": 3, "note": "分析可以更深入一些"},
            ],
            "version_history": [
                {
                    "version": "v2.0 最终版",
                    "date": "3月28日",
                    "changes": "增加了食材频次分析，完成了思辨任务，写了食堂菜单优化建议",
                    "idea": "想学习更多图表类型，比如折线图和散点图",
                },
                {
                    "version": "v1.0 初稿",
                    "date": "3月20日",
                    "changes": "完成了基础数据录入和口味分布饼图",
                    "idea": "数据太少了，需要收集更多同学的菜谱数据",
                },
            ],
        },
        {
            "unit_name": "第三单元·智能菜谱",
            "unit_icon": "🤖",
            "color": "#67C28A",
            "score": 3,
            "level_text": "继续加油",
            "gains": "初步了解了AI能做什么，体验了AI推荐和图像识别，感觉很神奇！",
            "improvements": "对AI的理解还比较浅，AI工具使用不够熟练，需要多练习。",
            "next_goal": "深入学习AI提示词技巧，做出更好的AI美食项目！",
            "dimensions": [
                {"name": "AI概念理解", "score": 3, "note": "知道AI是什么了"},
                {"name": "工具使用", "score": 3, "note": "会基本操作了"},
                {"name": "规范意识", "score": 4, "note": "知道不能完全依赖AI"},
                {"name": "创意应用", "score": 2, "note": "创意还不够"},
            ],
            "version_history": [
                {
                    "version": "v1.0 初体验",
                    "date": "4月10日",
                    "changes": "完成了AI美食推荐小助手的初步体验",
                    "idea": "想学习如何更好地和AI对话，让AI帮我做更多事情",
                },
            ],
        },
        {
            "unit_name": "第四单元·跨学科资源",
            "unit_icon": "📚",
            "color": "#9B59B6",
            "score": 2,
            "level_text": "刚开始",
            "gains": "刚开始学习，知道了资源库是什么，对跨学科有了初步认识。",
            "improvements": "还在起步阶段，需要学习更多资源整理的方法。",
            "next_goal": "完成美食与地理、美食与历史的资源整理！",
            "dimensions": [
                {"name": "资源收集", "score": 2, "note": "刚开始收集资料"},
                {"name": "分类整理", "score": 2, "note": "还在学习分类方法"},
                {"name": "跨学科联系", "score": 2, "note": "需要多思考学科联系"},
                {"name": "分享展示", "score": 1, "note": "还没到这一步"},
            ],
            "version_history": [
                {
                    "version": "v0.5 进行中",
                    "date": "4月18日",
                    "changes": "开始收集美食与地理的相关资料",
                    "idea": "想把美食和历史、地理、科学都联系起来，做一个超级资源库！",
                },
            ],
        },
    ]


# ============================================================
# 🎯 主函数：页面入口
# ============================================================
def render():
    """
    我的成长档案页面主入口
    由 app.py 动态调用渲染
    """
    user_info = st.session_state.get("current_user", None)
    user_name = user_info.get("nickname", "同学") if user_info else "同学"

    # 页面顶部欢迎语
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem;
                background: linear-gradient(135deg, #E8F4FD, #FFF0E6);
                border-radius: 20px; margin-bottom: 2rem;">
        <div style="font-size: 3rem; margin-bottom: 0.75rem;">📊</div>
        <h2 style="margin: 0; color: #2C3E50;">
            {user_name}的成长档案
        </h2>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.7;">
            记录你在美食数字菜谱项目中的每一步成长 🌟
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 模块一：学习统计卡片
    render_stats_cards(user_info)

    # 模块二：能力雷达图
    render_radar_chart(user_info)

    # 模块三：成长档案袋（时间线）
    render_portfolio_timeline(user_info)

    # 模块四：单元徽章
    render_badges(user_info)

    # 模块五：自评量表
    render_self_assessment(user_info)

    # 底部鼓励
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem;
                background: linear-gradient(135deg, #FFF0E6, #E8F4FD);
                border-radius: 20px; margin-top: 1rem;">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🌈</div>
        <div style="font-weight: 600; font-size: 1.2rem; color: #2C3E50; margin-bottom: 0.5rem;">
            每一次努力都是成长的养分！
        </div>
        <div style="font-size: 0.95rem; opacity: 0.7;">
            继续加油，{user_name}！你会越来越棒的～ 💪✨
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 🚀 独立运行入口（测试用）
# ============================================================
if __name__ == "__main__":
    st.set_page_config(
        page_title="我的成长档案｜美食数字菜谱",
        page_icon="📊",
        layout="wide",
    )

    try:
        from components.style import inject_global_style
        inject_global_style()
    except Exception:
        pass

    if "current_user" not in st.session_state:
        st.session_state["current_user"] = {
            "id": "user_demo_001",
            "username": "demo",
            "nickname": "小明同学",
            "role": "student",
            "points": 350,
        }

    render()
