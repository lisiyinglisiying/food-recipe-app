# -*- coding: utf-8 -*-
"""
侧边导航栏组件模块
==================
提供 Streamlit 应用的侧边栏导航功能
包含：成长档案、任务中心、疑问广场、帮助说明 四个入口
支持：深色/浅色模式切换、字体大小调节、护眼模式

使用方式:
    from components.sidebar import render_sidebar
    result = render_sidebar()
"""

import streamlit as st


# 导航菜单项配置
NAV_ITEMS = [
    {
        "key": "growth",
        "label": "我的成长档案",
        "icon": "📊",
        "description": "查看学习进度与成就徽章"
    },
    {
        "key": "tasks",
        "label": "任务中心",
        "icon": "📋",
        "description": "完成项目任务，获取积分"
    },
    {
        "key": "questions",
        "label": "疑问广场",
        "icon": "💬",
        "description": "提问与解答，互助学习"
    },
    {
        "key": "help",
        "label": "帮助说明",
        "icon": "❓",
        "description": "使用指南与常见问题"
    },
]


def render_sidebar(
    current_page: str = "growth",
    dark_mode: bool = False,
    font_scale: str = "正常",
    eye_care: bool = False
) -> dict:
    """
    渲染侧边导航栏

    参数:
        current_page: 当前选中的页面 key
        dark_mode: 是否深色模式（用于初始化）
        font_scale: 字体大小级别
        eye_care: 是否护眼模式

    返回:
        dict: 包含以下键的字典
            - "page": 用户选择的页面 key
            - "dark_mode": 深色模式开关状态
            - "font_scale": 字体大小
            - "eye_care": 护眼模式状态
    """

    with st.sidebar:
        # ======= Logo / 品牌区域 =======
        _render_brand()

        # ======= 分隔线 =======
        st.markdown('<div class="ms-divider"></div>', unsafe_allow_html=True)

        # ======= 导航菜单 =======
        st.markdown("### 🧭 导航菜单")
        selected_page = _render_nav_menu(current_page)

        # ======= 分隔线 =======
        st.markdown('<div class="ms-divider"></div>', unsafe_allow_html=True)

        # ======= 用户信息 =======
        _render_user_info()

        # ======= 分隔线 =======
        st.markdown('<div class="ms-divider"></div>', unsafe_allow_html=True)

        # ======= 设置区域 =======
        st.markdown("### ⚙️ 显示设置")
        settings = _render_settings(dark_mode, font_scale, eye_care)

        # ======= 底部信息 =======
        st.markdown("---")
        st.caption("🍳 美食数字菜谱项目 v1.0")
        st.caption("信息科技智能助教")

    return {
        "page": selected_page,
        "dark_mode": settings["dark_mode"],
        "font_scale": settings["font_scale"],
        "eye_care": settings["eye_care"],
    }


def _render_brand():
    """渲染侧边栏顶部的品牌 Logo 区域"""
    brand_html = """
    <div style="text-align: center; padding: 1rem 0;">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🍳</div>
        <h3 style="margin: 0; background: linear-gradient(135deg, #3498db, #e67e22); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   background-clip: text;">
            美食数字菜谱
        </h3>
        <p style="font-size: 0.85rem; opacity: 0.7; margin: 0.25rem 0 0 0;">
            信息科技智能助教
        </p>
    </div>
    """
    st.markdown(brand_html, unsafe_allow_html=True)


def _render_nav_menu(current_page: str) -> str:
    """
    渲染导航菜单项

    参数:
        current_page: 当前选中的页面 key

    返回:
        str: 用户选择的页面 key
    """
    selected = current_page

    for item in NAV_ITEMS:
        is_active = (selected == item["key"])

        # 使用原生 button 实现导航交互
        btn_label = f"{item['icon']}  {item['label']}"
        if st.button(
            btn_label,
            key=f"nav_{item['key']}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
            help=item["description"]
        ):
            selected = item["key"]
            st.session_state["current_page"] = item["key"]

    # 同步 session state
    if "current_page" in st.session_state:
        selected = st.session_state["current_page"]

    return selected


def _render_user_info():
    """渲染用户信息卡片"""
    st.markdown("### 👤 我的账户")

    user_html = """
    <div class="ms-user-info">
        <div class="ms-avatar">小</div>
        <div style="flex: 1;">
            <div style="font-weight: 600; font-size: 0.95rem;">小明同学</div>
            <div style="font-size: 0.8rem; opacity: 0.7;">七年级(3)班</div>
            <div style="font-size: 0.75rem; margin-top: 0.25rem;">
                <span class="ms-badge ms-badge-orange">Lv.5 厨艺新秀</span>
            </div>
        </div>
    </div>
    <div style="margin-top: 0.75rem; display: flex; gap: 0.5rem; justify-content: space-between;">
        <div style="text-align: center; flex: 1; padding: 0.5rem; 
                    background: rgba(52, 152, 219, 0.1); border-radius: 8px;">
            <div style="font-size: 1.1rem; font-weight: bold; color: #3498db;">1280</div>
            <div style="font-size: 0.7rem; opacity: 0.7;">积分</div>
        </div>
        <div style="text-align: center; flex: 1; padding: 0.5rem; 
                    background: rgba(230, 126, 34, 0.1); border-radius: 8px;">
            <div style="font-size: 1.1rem; font-weight: bold; color: #e67e22;">8</div>
            <div style="font-size: 0.7rem; opacity: 0.7;">徽章</div>
        </div>
        <div style="text-align: center; flex: 1; padding: 0.5rem; 
                    background: rgba(39, 174, 96, 0.1); border-radius: 8px;">
            <div style="font-size: 1.1rem; font-weight: bold; color: #27ae60;">23</div>
            <div style="font-size: 0.7rem; opacity: 0.7;">任务</div>
        </div>
    </div>
    """
    st.markdown(user_html, unsafe_allow_html=True)


def _render_settings(dark_mode: bool, font_scale: str, eye_care: bool) -> dict:
    """
    渲染显示设置区域

    参数:
        dark_mode: 深色模式初始值
        font_scale: 字体大小初始值
        eye_care: 护眼模式初始值

    返回:
        dict: 设置项字典
    """
    # 深色/浅色模式切换
    dark_mode_val = st.toggle(
        "🌙 深色模式",
        value=dark_mode,
        key="sidebar_dark_mode",
        help="切换深色/浅色主题"
    )

    # 字体大小选择
    font_options = ["小", "正常", "大", "特大"]
    font_index = font_options.index(font_scale) if font_scale in font_options else 1
    font_scale_val = st.select_slider(
        "🔠 字体大小",
        options=font_options,
        value=font_options[font_index],
        key="sidebar_font_scale"
    )

    # 护眼模式
    eye_care_val = st.toggle(
        "👁️ 护眼模式",
        value=eye_care,
        key="sidebar_eye_care",
        help="开启暖色背景，降低蓝光刺激"
    )

    return {
        "dark_mode": dark_mode_val,
        "font_scale": font_scale_val,
        "eye_care": eye_care_val,
    }


def get_page_title(page_key: str) -> str:
    """
    根据页面 key 获取页面标题

    参数:
        page_key: 页面标识符

    返回:
        str: 页面标题
    """
    for item in NAV_ITEMS:
        if item["key"] == page_key:
            return item["label"]
    return "首页"
