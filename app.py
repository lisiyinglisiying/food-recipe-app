# -*- coding: utf-8 -*-
"""
美食数字菜谱 · 信息科技智能助教
================================
应用主入口（原项目 app.py 在打包时遗漏，此处依据各模块的 render() 约定重建）。

功能:
    - 统一侧边导航：第一单元 / 智能助教 / 成长档案 / 任务中心 / 疑问广场 / 帮助说明
    - 身份切换：学生端 / 教师端（驱动任务中心、疑问广场、智能助教的知识库切换）
    - 全局显示设置：深色模式、字体大小、护眼模式

运行:
    streamlit run app.py
"""

import streamlit as st

from components.style import inject_global_style

import ai_assistant
import growth
import questions
import tasks
import unit1_webpage
import help as help_page


# ============================================================
# 页面常量
# ============================================================
APP_TITLE = "美食数字菜谱 · 信息科技智能助教"

# (key, 图标, 侧边栏名称, 渲染函数)
PAGES = [
    ("unit1",     "🌐", "第一单元",   unit1_webpage.main),
    ("assistant", "🤖", "智能助教",   ai_assistant.render),
    ("growth",    "📊", "成长档案",   growth.render),
    ("tasks",     "📋", "任务中心",   tasks.render),
    ("questions", "💬", "疑问广场",   questions.render),
    ("help",      "❓", "帮助说明",   help_page.render),
]

ROLE_OPTIONS = {"student": "👩‍🎓 学生端", "teacher": "👨‍🏫 教师端"}


# ============================================================
# 会话状态初始化
# ============================================================
def _init_session() -> None:
    """首次访问时准备全局状态，保证各页面拿得到 user / role"""
    defaults = {
        "page": "unit1",
        "current_role": "student",
        "current_user": {
            "id": "user_demo_001",
            "nickname": "小明同学",
            "class_name": "七年级(3)班",
            "level": "Lv.5 厨艺新秀",
        },
        # unit1_webpage 直接读取的两个键
        "current_user_id": "user_demo_001",
        "current_username": "小明同学",
        # 显示设置
        "dark_mode": False,
        "font_scale": "正常",
        "eye_care": False,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


# ============================================================
# 侧边栏
# ============================================================
def _render_brand() -> None:
    st.markdown(
        """
        <div style="text-align:center; padding: 0.75rem 0 0.25rem 0;">
            <div style="font-size: 2.4rem; line-height:1;">🍳</div>
            <div style="font-size: 1.05rem; font-weight: 700; margin-top: 0.4rem;
                        background: linear-gradient(135deg, #3498db, #e67e22);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                        background-clip: text;">
                美食数字菜谱
            </div>
            <div style="font-size: 0.75rem; opacity: 0.65; margin-top: 0.2rem;">
                信息科技智能助教
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_sidebar() -> None:
    with st.sidebar:
        _render_brand()
        st.markdown("---")

        # ---- 身份切换 ----
        st.markdown("##### 👤 当前身份")
        role_key = st.radio(
            "身份",
            options=list(ROLE_OPTIONS.keys()),
            format_func=lambda k: ROLE_OPTIONS[k],
            index=0 if st.session_state["current_role"] == "student" else 1,
            label_visibility="collapsed",
            key="role_radio",
        )
        if role_key != st.session_state["current_role"]:
            st.session_state["current_role"] = role_key
            st.rerun()

        user = st.session_state["current_user"]
        st.caption(f"{user['nickname']} · {user['class_name']} · {user['level']}")

        st.markdown("---")

        # ---- 导航 ----
        st.markdown("##### 🧭 导航菜单")
        labels = [f"{icon}  {name}" for _, icon, name, _ in PAGES]
        keys = [key for key, _, _, _ in PAGES]
        current_index = keys.index(st.session_state["page"]) if st.session_state["page"] in keys else 0

        picked_label = st.radio(
            "导航",
            options=labels,
            index=current_index,
            label_visibility="collapsed",
            key="nav_radio",
        )
        picked_key = keys[labels.index(picked_label)]
        if picked_key != st.session_state["page"]:
            st.session_state["page"] = picked_key
            st.rerun()

        st.markdown("---")

        # ---- 显示设置 ----
        st.markdown("##### ⚙️ 显示设置")
        st.session_state["dark_mode"] = st.toggle(
            "🌙 深色模式", value=st.session_state["dark_mode"], key="toggle_dark"
        )
        st.session_state["font_scale"] = st.select_slider(
            "🔠 字体大小",
            options=["小", "正常", "大", "特大"],
            value=st.session_state["font_scale"],
            key="slider_font",
        )
        st.session_state["eye_care"] = st.toggle(
            "👁️ 护眼模式", value=st.session_state["eye_care"], key="toggle_eye"
        )

        st.markdown("---")
        st.caption("🍳 美食数字菜谱项目 v1.0")


# ============================================================
# 主流程
# ============================================================
def main() -> None:
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="🍳",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    _init_session()

    # 全局样式随设置实时生效
    inject_global_style(
        dark_mode=st.session_state["dark_mode"],
        font_scale=st.session_state["font_scale"],
        eye_care=st.session_state["eye_care"],
    )

    _render_sidebar()

    # 按当前页面分发渲染；单页出错不影响整体框架
    current = st.session_state["page"]
    renderer = next((fn for key, _, _, fn in PAGES if key == current), unit1_webpage.main)

    try:
        renderer()
    except Exception as exc:  # noqa: BLE001
        st.error("这个页面加载时出了点问题，已为你保留其它页面的访问。")
        with st.expander("查看错误详情（便于排查）"):
            st.exception(exc)


if __name__ == "__main__":
    main()
