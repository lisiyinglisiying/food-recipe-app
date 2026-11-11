# -*- coding: utf-8 -*-
"""
任务中心页面
============
展示和管理美食数字菜谱项目中的所有学习任务

功能模块：
    1. 任务进度统计 - 已完成/进行中/未开始数量
    2. 任务分类Tab - 全部任务、单元任务、挑战任务、已完成
    3. 任务卡片列表 - 任务名称、所属单元、截止时间、奖励积分、完成状态
    4. 任务详情展开 - 任务要求、提交入口、相关资源
    5. 一键下发教材配套项目任务单（教师端可见）

页面入口：
    render() - 由 app.py 动态调用渲染
"""

import streamlit as st
from datetime import datetime, timedelta

# ===== 导入项目组件与工具 =====
from components.cards import task_card, stat_card
from components.header import render_section_title


# ============================================================
# 👨‍🏫 教师端：任务管理面板
# ============================================================
def render_teacher_tasks():
    """
    教师端任务管理页面
    功能：新建任务、任务列表、完成情况统计、一键提醒
    """
    from datetime import datetime, timedelta
    today = datetime.now()

    # 初始化教师端任务数据
    if "teacher_tasks" not in st.session_state:
        st.session_state["teacher_tasks"] = [
            {
                "id": "t001",
                "title": "基础任务：我的第一份美食网页",
                "unit": "第一单元·网页展示",
                "type": "unit",
                "points": 50,
                "deadline": today + timedelta(days=7),
                "total_students": 45,
                "completed": 28,
                "not_started": 12,
                "pending": 5,
                "status": "active",
            },
            {
                "id": "t002",
                "title": "进阶任务：多页面美食网站",
                "unit": "第一单元·网页展示",
                "type": "unit",
                "points": 80,
                "deadline": today + timedelta(days=14),
                "total_students": 45,
                "completed": 15,
                "not_started": 20,
                "pending": 10,
                "status": "active",
            },
            {
                "id": "t003",
                "title": "挑战任务：创意美食站点",
                "unit": "第一单元·网页展示",
                "type": "challenge",
                "points": 150,
                "deadline": today + timedelta(days=21),
                "total_students": 45,
                "completed": 3,
                "not_started": 35,
                "pending": 7,
                "status": "active",
            },
            {
                "id": "t004",
                "title": "基础任务：设计美食调查问卷",
                "unit": "第二单元·数字菜谱",
                "type": "unit",
                "points": 50,
                "deadline": today - timedelta(days=2),
                "total_students": 45,
                "completed": 42,
                "not_started": 1,
                "pending": 2,
                "status": "active",
            },
        ]

    # ===== 页面顶部 =====
    st.markdown("""
    <div style="text-align: center; padding: 2rem;
                background: linear-gradient(135deg, #E8F4FD, #FFF0E6);
                border-radius: 20px; margin-bottom: 1.5rem;">
        <div style="font-size: 3rem; margin-bottom: 0.75rem;">📋</div>
        <h2 style="margin: 0; color: #2C3E50;">任务管理中心</h2>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.7;">
            发布任务、追踪进度、一键提醒，轻松管理班级学习 👨‍🏫
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ===== 统计概览 =====
    tasks = st.session_state["teacher_tasks"]
    total_tasks = len(tasks)
    total_students = 45  # 假设班级总人数
    total_completed = sum(t["completed"] for t in tasks)
    total_pending = sum(t["pending"] for t in tasks)
    total_not_started = sum(t["not_started"] for t in tasks)
    overall_pct = int(total_completed / (total_tasks * total_students) * 100) if total_tasks > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📚 总任务数", total_tasks)
    with col2:
        st.metric("✅ 已完成人次", total_completed)
    with col3:
        st.metric("⏳ 进行中", total_pending)
    with col4:
        st.metric("📊 整体完成率", f"{overall_pct}%")

    st.markdown("---")

    # ===== 新建任务 =====
    with st.expander("➕ 新建任务 / 派发任务", expanded=False):
        with st.form("new_task_form"):
            st.markdown("#### 任务基本信息")
            col_a, col_b = st.columns(2)
            with col_a:
                new_title = st.text_input("任务名称", placeholder="例如：基础任务：我的第一份美食网页")
                new_unit = st.selectbox("所属单元", [
                    "第一单元·网页展示",
                    "第二单元·数字菜谱",
                    "第三单元·智能菜谱",
                    "第四单元·跨学科资源",
                ])
                new_type = st.selectbox("任务类型", ["单元任务", "挑战任务"])
            with col_b:
                new_points = st.number_input("奖励积分", min_value=10, max_value=500, value=50, step=10)
                new_deadline = st.date_input("截止日期", value=today + timedelta(days=7))
                new_icon = st.selectbox("任务图标", ["🌱", "🌿", "🏆", "📋", "📊", "🍽️", "🤖", "🎨", "🌍"])

            st.markdown("#### 任务描述")
            new_desc = st.text_area("任务简介", placeholder="简单描述一下这个任务要做什么……", height=60)

            st.markdown("#### 任务要求")
            new_req = st.text_area("详细要求", placeholder="列出任务的具体要求和评分标准……", height=100)

            submit_new = st.form_submit_button("🚀 发布任务", use_container_width=True, type="primary")

            if submit_new:
                if not new_title.strip():
                    st.warning("请填写任务名称")
                else:
                    import random
                    new_task = {
                        "id": f"t{random.randint(1000, 9999)}",
                        "title": new_title,
                        "unit": new_unit,
                        "type": "challenge" if "挑战" in new_type else "unit",
                        "points": new_points,
                        "deadline": datetime.combine(new_deadline, datetime.min.time()),
                        "total_students": 45,
                        "completed": 0,
                        "not_started": 45,
                        "pending": 0,
                        "status": "active",
                        "icon": new_icon,
                        "description": new_desc,
                        "requirements": new_req,
                    }
                    st.session_state["teacher_tasks"].insert(0, new_task)
                    st.success(f"🎉 任务「{new_title}」已发布！全班 45 名同学已收到通知～")
                    st.balloons()
                    st.rerun()

    st.markdown("---")

    # ===== 任务列表 + 完成情况 =====
    st.markdown("### 📋 任务列表 & 完成情况")

    # Tab 分类
    tab_all, tab_active, tab_expired = st.tabs([
        "📚 全部任务",
        "🟢 进行中",
        "🔴 已截止",
    ])

    def _render_teacher_task_cards(task_list, scope="all"):
        # scope 用于区分 tab，避免重复 widget key
        if not task_list:
            st.info("📭 暂无任务")
            return

        for idx, task in enumerate(task_list):
            with st.container():
                # 任务卡片头部
                type_tag = "🏆 挑战" if task["type"] == "challenge" else "📖 单元"
                completed_pct = int(task["completed"] / task["total_students"] * 100)

                col_left, col_right = st.columns([3, 1])

                with col_left:
                    st.markdown(f"""
                    <div style="padding: 1rem; background: #FAFBFC; border-radius: 12px;
                                border: 1px solid #E8E8E8;">
                        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;">
                            <span style="font-size: 1.5rem;">{task.get('icon', '📋')}</span>
                            <div style="flex: 1;">
                                <div style="font-weight: 600; font-size: 1rem;">{task['title']}</div>
                                <div style="font-size: 0.8rem; opacity: 0.7;">{task['unit']} · {type_tag}</div>
                            </div>
                            <span style="background: rgba(52, 152, 219, 0.1); color: #3498db;
                                         padding: 4px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: 500;">
                                +{task['points']} 积分
                            </span>
                        </div>
                        <div style="margin-top: 0.75rem;">
                            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 0.25rem;">
                                <span style="opacity: 0.7;">完成进度</span>
                                <span style="font-weight: 600; color: #27ae60;">{task['completed']}/{task['total_students']} 人 ({completed_pct}%)</span>
                            </div>
                            <div style="height: 8px; background: #E8E8E8; border-radius: 4px; overflow: hidden;">
                                <div style="height: 100%; width: {completed_pct}%;
                                            background: linear-gradient(90deg, #27ae60, #2ecc71);
                                            border-radius: 4px; transition: width 0.3s ease;"></div>
                            </div>
                        </div>
                        <div style="display: flex; gap: 1rem; margin-top: 0.75rem; font-size: 0.8rem;">
                            <span style="color: #27ae60;">✅ 已完成 {task['completed']} 人</span>
                            <span style="color: #f39c12;">⏳ 进行中 {task['pending']} 人</span>
                            <span style="color: #e74c3c;">📋 未开始 {task['not_started']} 人</span>
                            <span style="opacity: 0.6; margin-left: auto;">
                                截止：{task['deadline'].strftime('%m月%d日') if hasattr(task['deadline'], 'strftime') else task['deadline']}
                            </span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with col_right:
                    # 操作按钮
                    st.markdown("")
                    remind_count = task["pending"] + task["not_started"]
                    if remind_count > 0:
                        if st.button(f"🔔 提醒 ({remind_count}人)",
                                     key=f"remind_{scope}_{task['id']}",
                                     use_container_width=True,
                                     type="primary"):
                            st.success(f"""
                            📣 已向 {remind_count} 名未完成的同学发送提醒！

                            提醒内容：
                            > 亲爱的同学，「{task['title']}」还有同学没有完成哦～
                            > 截止时间：{task['deadline'].strftime('%m月%d日') if hasattr(task['deadline'], 'strftime') else task['deadline']}
                            > 加油完成，获得 +{task['points']} 积分奖励！🎯
                            """)
                            st.balloons()
                    else:
                        st.success("🎉 全部完成！")

                    if st.button(f"📊 查看详情", key=f"detail_{scope}_{task['id']}", use_container_width=True):
                        st.info(f"正在打开「{task['title']}」的详细完成情况……")

                st.markdown("---")

    with tab_all:
        _render_teacher_task_cards(tasks, "all")

    with tab_active:
        active_tasks = [t for t in tasks if t["status"] == "active"]
        _render_teacher_task_cards(active_tasks, "active")

    with tab_expired:
        expired_tasks = [t for t in tasks if hasattr(t["deadline"], "__lt__") and t["deadline"] < datetime.now()]
        _render_teacher_task_cards(expired_tasks, "expired")

    # 底部提示
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem;
                background: linear-gradient(135deg, #E8F4FD, #FFF0E6);
                border-radius: 16px; margin-top: 1rem;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">💡</div>
        <div style="font-weight: 600; color: #2C3E50; margin-bottom: 0.25rem;">
            教师小贴士
        </div>
        <div style="font-size: 0.9rem; opacity: 0.7; max-width: 600px; margin: 0 auto;">
            定期提醒未完成的同学，可以有效提高任务完成率哦！
            建议在截止日前 3 天和截止日当天各提醒一次～ 🔔
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 🎯 主函数：页面入口
# ============================================================
def render():
    """
    任务中心页面主入口
    根据角色分别渲染学生端或教师端
    """
    user_info = st.session_state.get("current_user", None)
    current_role = st.session_state.get("current_role", "student")

    if current_role == "teacher":
        # 教师端：任务管理面板
        render_teacher_tasks()
    else:
        # 学生端：任务列表 + 进度
        _render_student_tasks(user_info)


# ============================================================
# 🎒 学生端：任务中心
# ============================================================
def _render_student_tasks(user_info):
    """
    学生端任务中心页面
    """
    from datetime import datetime, timedelta

    user_name = user_info.get("nickname", "同学") if user_info else "同学"
    today = datetime.now()

    # 学生端任务数据
    tasks_data = [
        {
            "id": "task_u1_1",
            "title": "基础任务：我的第一份美食网页",
            "description": "学习 Markdown 基础语法，制作一份简单的美食介绍网页。",
            "type": "unit",
            "unit_name": "第一单元·网页展示",
            "icon": "🌱",
            "status": "completed",
            "points": 50,
            "deadline": today - timedelta(days=10),
        },
        {
            "id": "task_u1_2",
            "title": "进阶任务：多页面美食网站",
            "description": "制作包含多道菜的美食网站，添加食材清单和制作步骤。",
            "type": "unit",
            "unit_name": "第一单元·网页展示",
            "icon": "🌿",
            "status": "completed",
            "points": 80,
            "deadline": today - timedelta(days=3),
        },
        {
            "id": "task_u1_3",
            "title": "挑战任务：创意美食站点",
            "description": "设计一个有主题、有风格的完整美食网站，展现你的创意才华！",
            "type": "challenge",
            "unit_name": "第一单元·网页展示",
            "icon": "🏆",
            "status": "pending",
            "points": 150,
            "deadline": today + timedelta(days=7),
        },
        {
            "id": "task_u2_1",
            "title": "基础任务：设计美食调查问卷",
            "description": "学习数据采集方法，设计一份关于班级美食喜好的调查问卷。",
            "type": "unit",
            "unit_name": "第二单元·数字菜谱",
            "icon": "📋",
            "status": "completed",
            "points": 50,
            "deadline": today - timedelta(days=5),
        },
        {
            "id": "task_u2_2",
            "title": "进阶任务：菜谱数据可视化",
            "description": "收集调查数据，用图表展示口味分布、食材频次等信息。",
            "type": "unit",
            "unit_name": "第二单元·数字菜谱",
            "icon": "📊",
            "status": "pending",
            "points": 80,
            "deadline": today + timedelta(days=2),
        },
        {
            "id": "task_u2_3",
            "title": "挑战任务：食堂菜单优化方案",
            "description": "用你收集的菜谱数据，为学校食堂设计一份优化建议。",
            "type": "challenge",
            "unit_name": "第二单元·数字菜谱",
            "icon": "🍽️",
            "status": "not_started",
            "points": 120,
            "deadline": today + timedelta(days=14),
        },
        {
            "id": "task_u3_1",
            "title": "基础任务：AI 美食初体验",
            "description": "体验 AI 工具的基本功能，了解 AI 能帮我们做什么。",
            "type": "unit",
            "unit_name": "第三单元·智能菜谱",
            "icon": "🤖",
            "status": "pending",
            "points": 50,
            "deadline": today + timedelta(days=10),
        },
        {
            "id": "task_u3_2",
            "title": "挑战任务：AI 创意美食设计师",
            "description": "用 AI 辅助设计一道创意美食，完成从构思到呈现的全过程。",
            "type": "challenge",
            "unit_name": "第三单元·智能菜谱",
            "icon": "🎨",
            "status": "not_started",
            "points": 150,
            "deadline": today + timedelta(days=21),
        },
    ]

    # 页面顶部
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem;
                background: linear-gradient(135deg, #FFF0E6, #E8F4FD);
                border-radius: 20px; margin-bottom: 2rem;">
        <div style="font-size: 3rem; margin-bottom: 0.75rem;">📋</div>
        <h2 style="margin: 0; color: #2C3E50;">任务中心</h2>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.7;">
            完成任务赢积分，升级你的美食数字技能！ 🎮
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 统计卡片
    completed_count = sum(1 for t in tasks_data if t["status"] == "completed")
    in_progress_count = sum(1 for t in tasks_data if t["status"] == "pending")
    not_started_count = sum(1 for t in tasks_data if t["status"] == "not_started")
    total_points = sum(t["points"] for t in tasks_data if t["status"] == "completed")
    total_count = len(tasks_data)
    progress_pct = int(completed_count / total_count * 100) if total_count > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("✅ 已完成", completed_count, f"+{total_points}积分")
    with col2:
        st.metric("⏳ 进行中", in_progress_count)
    with col3:
        st.metric("📋 未开始", not_started_count)
    with col4:
        st.metric("🎯 完成进度", f"{progress_pct}%", f"{completed_count}/{total_count}")

    st.markdown("---")

    # 任务分类Tab
    tab_all, tab_unit, tab_challenge, tab_completed = st.tabs([
        "📚 全部任务", "📖 单元任务", "🏆 挑战任务", "✅ 已完成",
    ])

    def _render_student_cards(task_list, scope="all"):
        # scope 用于区分 tab，避免同一任务在多个 tab 中产生重复的 widget key
        if not task_list:
            st.info("📭 这里还没有任务呢～")
            return
        for i, task in enumerate(task_list):
            type_tag = "🏆 挑战任务" if task["type"] == "challenge" else "📖 单元任务"
            status_colors = {
                "completed": ("#27ae60", "✅ 已完成"),
                "pending": ("#f39c12", "⏳ 进行中"),
                "not_started": ("#95a5a6", "📋 未开始"),
            }
            color, status_text = status_colors.get(task["status"], ("#95a5a6", "未知"))
            deadline_str = task["deadline"].strftime("%m月%d日") if hasattr(task["deadline"], "strftime") else str(task["deadline"])

            st.markdown(f"""
            <div style="padding: 1rem 1.25rem; background: white; border-radius: 12px;
                        border: 1px solid #E8E8E8; margin-bottom: 0.75rem;">
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <span style="font-size: 1.75rem;">{task.get('icon', '📋')}</span>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; font-size: 1rem; color: #2C3E50;">{task['title']}</div>
                        <div style="font-size: 0.8rem; opacity: 0.7; margin-top: 2px;">
                            {task.get('unit_name', '')} · {type_tag}
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="background: rgba(52, 152, 219, 0.1); color: #3498db;
                                    padding: 4px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: 600;
                                    display: inline-block;">
                            +{task['points']} 积分
                        </div>
                        <div style="font-size: 0.75rem; color: {color}; margin-top: 4px; font-weight: 500;">
                            {status_text}
                        </div>
                    </div>
                </div>
                <div style="font-size: 0.85rem; color: #666; margin-top: 0.5rem;">
                    {task.get('description', '')}
                </div>
                <div style="font-size: 0.75rem; opacity: 0.6; margin-top: 0.5rem;">
                    📅 截止：{deadline_str}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if task["status"] != "completed":
                if st.button(f"📝 去完成", key=f"go_{scope}_{task['id']}", use_container_width=True):
                    st.info(f"正在打开「{task['title']}」……")

    with tab_all:
        _render_student_cards(tasks_data, "all")
    with tab_unit:
        _render_student_cards([t for t in tasks_data if t["type"] == "unit"], "unit")
    with tab_challenge:
        _render_student_cards([t for t in tasks_data if t["type"] == "challenge"], "challenge")
    with tab_completed:
        _render_student_cards([t for t in tasks_data if t["status"] == "completed"], "completed")

    # 底部提示
    st.markdown(f"""
    <div style="text-align: center; padding: 1.5rem;
                background: linear-gradient(135deg, #E8F4FD, #FFF0E6);
                border-radius: 16px; margin-top: 1rem;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">💡</div>
        <div style="font-weight: 600; color: #2C3E50; margin-bottom: 0.25rem;">
            小提示
        </div>
        <div style="font-size: 0.9rem; opacity: 0.7; max-width: 600px; margin: 0 auto;">
            每天完成一点小任务，积累起来就是大进步！
            完成任务不仅能获得积分，还能解锁更多徽章哦～ 🏅
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 🚀 独立运行入口（测试用）
# ============================================================
if __name__ == "__main__":
    st.set_page_config(
        page_title="任务中心｜美食数字菜谱",
        page_icon="📋",
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
    if "current_role" not in st.session_state:
        st.session_state["current_role"] = "student"

    render()
