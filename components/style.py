# -*- coding: utf-8 -*-
"""
全局样式注入模块
================
使用 streamlit 的 markdown + unsafe_allow_html 注入自定义 CSS
提供美食科技风格的统一视觉样式

主色调：浅蓝 #E8F4FD + 浅暖橙 #FFF3E6
特色：圆角卡片、柔和 hover 动效、深色模式、字体放大、护眼模式
"""

import streamlit as st


def inject_global_style(dark_mode: bool = False, font_scale: str = "正常", eye_care: bool = False):
    """
    注入全局自定义 CSS 样式

    参数:
        dark_mode: 是否启用深色模式
        font_scale: 字体放大级别 - "小" / "正常" / "大" / "特大"
        eye_care: 是否启用护眼模式（降低蓝光，暖色背景）
    """

    # 根据字体大小级别设置基础字号
    font_sizes = {
        "小": "14px",
        "正常": "16px",
        "大": "18px",
        "特大": "20px"
    }
    base_font_size = font_sizes.get(font_scale, "16px")

    # 根据模式选择配色方案
    if dark_mode:
        # 深色模式配色
        primary_bg = "#1a1a2e"        # 主背景 - 深蓝灰
        secondary_bg = "#16213e"      # 次级背景
        card_bg = "#0f3460"           # 卡片背景
        accent_blue = "#4a90d9"       # 蓝色强调
        accent_orange = "#e94560"     # 橙色/红色强调（深色模式调整）
        text_primary = "#eaeaea"      # 主要文字
        text_secondary = "#a0a0a0"    # 次要文字
        border_color = "#2a2a4a"      # 边框色
        hover_bg = "#1f4068"          # 悬停背景
    else:
        # 浅色模式 - 美食科技风
        if eye_care:
            # 护眼模式 - 偏暖米黄色
            primary_bg = "#fdf6e3"    # 护眼米黄背景
            secondary_bg = "#f5e6c8"  # 次级背景
            card_bg = "#fffef5"       # 卡片背景
        else:
            primary_bg = "#E8F4FD"    # 浅蓝主背景 - 美食科技风
            secondary_bg = "#FFF3E6"  # 浅暖橙次级背景
            card_bg = "#ffffff"       # 卡片白色背景

        accent_blue = "#3498db"       # 蓝色强调
        accent_orange = "#e67e22"     # 暖橙强调
        text_primary = "#2c3e50"      # 主要文字 - 深蓝灰
        text_secondary = "#7f8c8d"    # 次要文字 - 灰
        border_color = "#dce4eb"      # 边框色
        hover_bg = "#d6eaf8"          # 悬停背景

    # 构建 CSS 样式
    css = f"""
    <style>
    /* ========== 全局基础样式 ========== */
    .stApp {{
        background-color: {primary_bg};
        font-size: {base_font_size};
    }}

    /* ========== 主内容区域 ========== */
    .main .block-container {{
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }}

    /* ========== 侧边栏样式 ========== */
    section[data-testid="stSidebar"] {{
        background-color: {secondary_bg};
        border-right: 1px solid {border_color};
        width: 260px !important;
    }}

    section[data-testid="stSidebar"] > div:first-child {{
        background-color: {secondary_bg};
    }}

    /* ========== 标题文字样式 ========== */
    h1, h2, h3, h4, h5, h6 {{
        color: {text_primary} !important;
        font-weight: 600;
    }}

    p, span, div {{
        color: {text_primary};
    }}

    /* ========== 通用卡片样式 ========== */
    .ms-card {{
        background-color: {card_bg};
        border-radius: 16px;
        padding: 1.25rem;
        border: 1px solid {border_color};
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 1rem;
    }}

    .ms-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
        border-color: {accent_blue};
    }}

    /* ========== 大卡片（单元入口） ========== */
    .ms-card-large {{
        background: linear-gradient(135deg, {card_bg} 0%, {secondary_bg} 100%);
        border-radius: 20px;
        padding: 1.75rem;
        border: 2px solid {border_color};
        position: relative;
        overflow: hidden;
    }}

    .ms-card-large::before {{
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, {accent_blue}22 0%, transparent 70%);
        border-radius: 50%;
    }}

    .ms-card-large:hover {{
        border-color: {accent_orange};
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 12px 32px rgba(230, 126, 34, 0.2);
    }}

    /* ========== 进度条样式 ========== */
    .ms-progress-bar {{
        width: 100%;
        height: 8px;
        background-color: {border_color};
        border-radius: 4px;
        overflow: hidden;
        margin: 0.5rem 0;
    }}

    .ms-progress-fill {{
        height: 100%;
        background: linear-gradient(90deg, {accent_blue}, {accent_orange});
        border-radius: 4px;
        transition: width 0.5s ease;
    }}

    /* ========== 徽章样式 ========== */
    .ms-badge {{
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 500;
        margin-right: 0.5rem;
        margin-bottom: 0.25rem;
    }}

    .ms-badge-blue {{
        background-color: {accent_blue}22;
        color: {accent_blue};
    }}

    .ms-badge-orange {{
        background-color: {accent_orange}22;
        color: {accent_orange};
    }}

    .ms-badge-green {{
        background-color: #27ae6022;
        color: #27ae60;
    }}

    .ms-badge-red {{
        background-color: #e74c3c22;
        color: #e74c3c;
    }}

    /* ========== 按钮样式 ========== */
    .stButton > button {{
        border-radius: 10px;
        padding: 0.5rem 1.25rem;
        font-weight: 500;
        transition: all 0.2s ease;
        border: 1px solid {border_color};
        background-color: {card_bg};
        color: {text_primary};
    }}

    .stButton > button:hover {{
        background-color: {hover_bg};
        border-color: {accent_blue};
        transform: translateY(-1px);
    }}

    .stButton > button:active {{
        transform: translateY(0);
    }}

    /* 主按钮样式 */
    .ms-btn-primary button {{
        background: linear-gradient(135deg, {accent_blue}, {accent_orange}) !important;
        color: white !important;
        border: none !important;
    }}

    .ms-btn-primary button:hover {{
        box-shadow: 0 4px 12px rgba(52, 152, 219, 0.4);
        transform: translateY(-2px);
    }}

    /* ========== 输入框样式 ========== */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {{
        border-radius: 10px;
        border: 1px solid {border_color};
        background-color: {card_bg};
        color: {text_primary};
        transition: all 0.2s ease;
    }}

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {{
        border-color: {accent_blue};
        box-shadow: 0 0 0 3px {accent_blue}22;
    }}

    /* ========== Tab 样式 ========== */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.5rem;
        background-color: {secondary_bg};
        padding: 0.5rem;
        border-radius: 12px;
    }}

    .stTabs [data-baseweb="tab"] {{
        height: 2.5rem;
        border-radius: 8px;
        padding: 0 1.25rem;
        font-weight: 500;
        color: {text_secondary};
        transition: all 0.2s ease;
    }}

    .stTabs [data-baseweb="tab"]:hover {{
        color: {accent_blue};
        background-color: {hover_bg};
    }}

    .stTabs [aria-selected="true"] {{
        background-color: {card_bg} !important;
        color: {accent_blue} !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }}

    /* ========== 侧边栏导航项 ========== */
    .ms-nav-item {{
        display: flex;
        align-items: center;
        padding: 0.75rem 1rem;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.2s ease;
        margin-bottom: 0.25rem;
        color: {text_primary};
        text-decoration: none;
    }}

    .ms-nav-item:hover {{
        background-color: {hover_bg};
        transform: translateX(4px);
    }}

    .ms-nav-item.active {{
        background-color: {accent_blue}22;
        color: {accent_blue};
        font-weight: 600;
    }}

    .ms-nav-icon {{
        font-size: 1.25rem;
        margin-right: 0.75rem;
        width: 24px;
        text-align: center;
    }}

    /* ========== 用户信息卡片 ========== */
    .ms-user-info {{
        display: flex;
        align-items: center;
        padding: 0.75rem;
        background-color: {card_bg};
        border-radius: 12px;
        border: 1px solid {border_color};
    }}

    .ms-avatar {{
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: linear-gradient(135deg, {accent_blue}, {accent_orange});
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 1.25rem;
        margin-right: 0.75rem;
    }}

    /* ========== 作品展示卡片 ========== */
    .ms-work-card {{
        background-color: {card_bg};
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid {border_color};
        transition: all 0.3s ease;
    }}

    .ms-work-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    }}

    .ms-work-thumbnail {{
        width: 100%;
        height: 160px;
        background: linear-gradient(135deg, {secondary_bg}, {accent_blue}33);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
    }}

    .ms-work-body {{
        padding: 1rem;
    }}

    /* ========== 任务卡片 ========== */
    .ms-task-card {{
        background-color: {card_bg};
        border-radius: 12px;
        padding: 1rem;
        border-left: 4px solid {accent_blue};
        transition: all 0.2s ease;
    }}

    .ms-task-card.completed {{
        border-left-color: #27ae60;
        opacity: 0.8;
    }}

    .ms-task-card.urgent {{
        border-left-color: #e74c3c;
    }}

    /* ========== 疑问卡片 ========== */
    .ms-question-card {{
        background-color: {card_bg};
        border-radius: 12px;
        padding: 1rem 1.25rem;
        border: 1px solid {border_color};
        transition: all 0.2s ease;
    }}

    .ms-question-card:hover {{
        border-color: {accent_orange};
        background-color: {accent_orange}08;
    }}

    /* ========== 标签/Tag 样式 ========== */
    .ms-tag {{
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        font-size: 0.8em;
        background-color: {secondary_bg};
        color: {text_secondary};
        margin-right: 0.4rem;
    }}

    /* ========== 分隔线 ========== */
    .ms-divider {{
        height: 1px;
        background-color: {border_color};
        margin: 1rem 0;
    }}

    /* ========== 头部标题栏 ========== */
    .ms-header {{
        background: linear-gradient(135deg, {accent_blue} 0%, {accent_orange} 100%);
        padding: 1rem 1.5rem;
        border-radius: 0 0 20px 20px;
        color: white;
        margin-bottom: 1.5rem;
    }}

    .ms-header h1 {{
        color: white !important;
        font-size: 1.5rem;
        margin: 0;
    }}

    .ms-header .subtitle {{
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.9rem;
        margin-top: 0.25rem;
    }}

    /* ========== 身份切换 Tab ========== */
    .ms-role-tabs {{
        display: flex;
        gap: 0.25rem;
        background-color: rgba(255, 255, 255, 0.2);
        padding: 0.25rem;
        border-radius: 10px;
    }}

    .ms-role-tab {{
        padding: 0.5rem 1rem;
        border-radius: 8px;
        cursor: pointer;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 500;
        transition: all 0.2s ease;
        white-space: nowrap;
    }}

    .ms-role-tab:hover {{
        color: white;
    }}

    .ms-role-tab.active {{
        background-color: white;
        color: {accent_blue};
    }}

    /* ========== 深色模式切换开关 ========== */
    .ms-theme-toggle {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.75rem 1rem;
        background-color: {card_bg};
        border-radius: 10px;
        border: 1px solid {border_color};
        margin-top: 1rem;
    }}

    /* ========== 星级评价 ========== */
    .ms-rating {{
        color: #f1c40f;
        font-size: 1rem;
    }}

    /* ========== 滚动条美化 ========== */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}

    ::-webkit-scrollbar-track {{
        background: {secondary_bg};
    }}

    ::-webkit-scrollbar-thumb {{
        background: {border_color};
        border-radius: 4px;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: {text_secondary};
    }}

    /* ========== 动画效果 ========== */
    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    .ms-animate-fadein {{
        animation: fadeInUp 0.5s ease forwards;
    }}

    /* ========== 响应式调整 ========== */
    @media (max-width: 768px) {{
        .ms-card-large {{
            padding: 1.25rem;
        }}

        .main .block-container {{
            padding-left: 1rem;
            padding-right: 1rem;
        }}
    }}

    /* ========== Streamlit 原生组件覆盖 ========== */
    /* 隐藏 Streamlit 默认的菜单和页脚 */
    #MainMenu {{
        visibility: hidden;
    }}

    footer {{
        visibility: hidden;
    }}

    /* 调整 expander 样式 */
    .streamlit-expanderHeader {{
        background-color: {secondary_bg};
        border-radius: 10px;
        padding: 0.75rem 1rem;
    }}

    .streamlit-expanderContent {{
        background-color: {card_bg};
        border-radius: 0 0 10px 10px;
        padding: 1rem;
        border: 1px solid {border_color};
        border-top: none;
    }}

    /* metric 组件样式 */
    [data-testid="stMetric"] {{
        background-color: {card_bg};
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid {border_color};
    }}

    [data-testid="stMetricLabel"] {{
        color: {text_secondary};
    }}

    [data-testid="stMetricValue"] {{
        color: {accent_blue};
        font-size: 2rem !important;
    }}

    </style>
    """

    # 注入 CSS
    st.markdown(css, unsafe_allow_html=True)


def inject_component_css(css_code: str):
    """
    注入额外的组件级 CSS（按需使用）

    参数:
        css_code: 自定义 CSS 代码字符串
    """
    st.markdown(f"<style>{css_code}</style>", unsafe_allow_html=True)
