# -*- coding: utf-8 -*-
"""
疑问广场页面
============
学生提问互助 + 教师答疑管理

学生端：提问、浏览问题、回答问题
教师端：统计概览、管理问题、发布统一任务问题、标记解决
"""

import streamlit as st
from datetime import datetime, timedelta


# ============================================================
# 🎯 主入口：根据角色分发
# ============================================================
def render():
    """疑问广场主入口"""
    current_role = st.session_state.get("current_role", "student")
    user_info = st.session_state.get("current_user", None)

    if current_role == "teacher":
        render_teacher_questions()
    else:
        render_student_questions(user_info)


# ============================================================
# 👨‍🏫 教师端：疑问管理中心
# ============================================================
def render_teacher_questions():
    """教师端疑问管理中心"""
    today = datetime.now()

    # 初始化教师端问题数据
    if "teacher_questions" not in st.session_state:
        st.session_state["teacher_questions"] = [
            {
                "id": "q001",
                "title": "Markdown 怎么插入图片？图片链接从哪里来？",
                "content": "我在做第一单元的美食网页作业，想插入一张番茄炒蛋的图片，但是不知道怎么弄。",
                "author": "小明同学",
                "unit": "第一单元·网页展示",
                "tags": ["Markdown", "图片"],
                "is_resolved": True,
                "time_ago": "2天前",
                "view_count": 56,
                "reply_count": 3,
                "answers": 3,
            },
            {
                "id": "q002",
                "title": "怎么把调查的数据做成饼图？",
                "content": "第二单元学了数据可视化，我收集了班级同学喜欢的口味数据，但是不知道怎么变成饼图。",
                "author": "小美",
                "unit": "第二单元·数字菜谱",
                "tags": ["数据可视化", "饼图"],
                "is_resolved": True,
                "time_ago": "3天前",
                "view_count": 42,
                "reply_count": 2,
                "answers": 2,
            },
            {
                "id": "q003",
                "title": "AI 生成的菜谱可以直接用吗？会不会有问题？",
                "content": "第三单元开始学AI了，我让AI帮我生成了一道创意菜的菜谱，但是我有点担心。",
                "author": "小宇",
                "unit": "第三单元·智能菜谱",
                "tags": ["AI", "菜谱"],
                "is_resolved": False,
                "time_ago": "5小时前",
                "view_count": 28,
                "reply_count": 1,
                "answers": 1,
            },
            {
                "id": "q004",
                "title": "表格的边框颜色怎么改？",
                "content": "做网页的时候，我想让表格更好看一些，能不能改表格边框的颜色呀？",
                "author": "小华",
                "unit": "第一单元·网页展示",
                "tags": ["表格", "样式"],
                "is_resolved": False,
                "time_ago": "1天前",
                "view_count": 15,
                "reply_count": 0,
                "answers": 0,
            },
            {
                "id": "q005",
                "title": "怎么收集更多数据？大家都不愿意填问卷怎么办？",
                "content": "老师让我们至少收集20条数据，我问了一圈才收集到8条。",
                "author": "小强",
                "unit": "第二单元·数字菜谱",
                "tags": ["数据采集", "问卷"],
                "is_resolved": False,
                "time_ago": "6小时前",
                "view_count": 22,
                "reply_count": 1,
                "answers": 1,
            },
            {
                "id": "q006",
                "title": "跨学科资源库应该收集什么内容？",
                "content": "第四单元要做跨学科资源库，但是我不知道该收集什么。",
                "author": "小婷",
                "unit": "第四单元·跨学科资源",
                "tags": ["跨学科", "资源库"],
                "is_resolved": False,
                "time_ago": "12小时前",
                "view_count": 18,
                "reply_count": 0,
                "answers": 0,
            },
        ]

    # 初始化教师发布的统一问题
    if "teacher_task_questions" not in st.session_state:
        st.session_state["teacher_task_questions"] = [
            {
                "id": "tq001",
                "title": "【思考任务】美食与地理环境有什么关系？",
                "unit": "第四单元·跨学科资源",
                "content": "请同学们思考：不同地区的特色美食和当地的地理环境（气候、土壤、地形等）有什么关系？\n\n请举例说明，至少列举 2 个地区的特色美食，并分析地理因素的影响。",
                "deadline": today + timedelta(days=5),
                "total_students": 45,
                "submitted": 18,
                "points": 30,
                "status": "active",
            },
        ]

    questions = st.session_state["teacher_questions"]
    task_questions = st.session_state["teacher_task_questions"]

    # ===== 页面顶部 =====
    st.markdown("""
    <div style="text-align: center; padding: 2rem;
                background: linear-gradient(135deg, #E8F4FD, #FFF0E6);
                border-radius: 20px; margin-bottom: 1.5rem;">
        <div style="font-size: 3rem; margin-bottom: 0.75rem;">💬</div>
        <h2 style="margin: 0; color: #2C3E50;">疑问管理中心</h2>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.7;">
            查看学生提问、发布思考任务、帮助学生解决疑惑 👨‍🏫
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ===== 统计概览 =====
    total_q = len(questions)
    resolved_q = sum(1 for q in questions if q["is_resolved"])
    unresolved_q = total_q - resolved_q
    resolve_rate = int(resolved_q / total_q * 100) if total_q > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("❓ 总问题数", total_q)
    with col2:
        st.metric("✅ 已解决", resolved_q)
    with col3:
        st.metric("⏳ 待解答", unresolved_q)
    with col4:
        st.metric("📊 解决率", f"{resolve_rate}%")

    st.markdown("---")

    # ===== 发布统一问题 =====
    with st.expander("📢 发布统一思考问题 / 探究任务", expanded=False):
        with st.form("publish_task_question_form"):
            st.markdown("#### 发布班级统一思考问题")
            st.caption("发布一个问题让全班同学思考回答，适合作为课堂讨论或课后探究任务")

            col_a, col_b = st.columns(2)
            with col_a:
                tq_title = st.text_input("问题标题", placeholder="例如：【思考任务】美食与地理环境有什么关系？")
                tq_unit = st.selectbox("所属单元", [
                    "第一单元·网页展示",
                    "第二单元·数字菜谱",
                    "第三单元·智能菜谱",
                    "第四单元·跨学科资源",
                ])
            with col_b:
                tq_points = st.number_input("奖励积分", min_value=10, max_value=200, value=30, step=5)
                tq_deadline = st.date_input("截止日期", value=today + timedelta(days=7))

            tq_content = st.text_area(
                "问题内容 / 任务要求",
                placeholder="详细描述问题或任务要求，引导学生思考……",
                height=100,
            )

            submit_tq = st.form_submit_button("🚀 发布给全班", use_container_width=True, type="primary")

            if submit_tq:
                if not tq_title.strip():
                    st.warning("请填写问题标题")
                elif not tq_content.strip():
                    st.warning("请填写问题内容")
                else:
                    import random
                    new_tq = {
                        "id": f"tq{random.randint(1000, 9999)}",
                        "title": tq_title,
                        "unit": tq_unit,
                        "content": tq_content,
                        "deadline": datetime.combine(tq_deadline, datetime.min.time()),
                        "total_students": 45,
                        "submitted": 0,
                        "points": tq_points,
                        "status": "active",
                    }
                    st.session_state["teacher_task_questions"].insert(0, new_tq)
                    st.success(f"""
                    🎉 思考问题已发布！

                    已向全班 45 名同学发送任务：
                    「{tq_title}」

                    同学们可以在疑问广场查看并回答，
                    截止时间：{tq_deadline.strftime('%m月%d日')}
                    完成奖励：+{tq_points} 积分
                    """)
                    st.balloons()
                    st.rerun()

    st.markdown("---")

    # ===== Tab 切换 =====
    tab_student_q, tab_task_q, tab_resolved = st.tabs([
        "👨‍🎓 学生提问",
        "📢 已发布的统一问题",
        "✅ 已解决问题",
    ])

    # ---- Tab 1: 学生提问 ----
    with tab_student_q:
        st.markdown("### 👨‍🎓 学生提问（待解答优先）")

        # 按单元筛选
        unit_filter = st.selectbox(
            "按单元筛选",
            options=["全部单元", "第一单元·网页展示", "第二单元·数字菜谱",
                     "第三单元·智能菜谱", "第四单元·跨学科资源"],
            key="teacher_q_filter",
        )

        filtered_qs = questions
        if unit_filter != "全部单元":
            filtered_qs = [q for q in questions if q["unit"] == unit_filter]

        # 待解答的排前面
        sorted_qs = sorted(filtered_qs, key=lambda x: 0 if not x["is_resolved"] else 1)

        if not sorted_qs:
            st.info("📭 该单元暂无学生提问")
        else:
            for q in sorted_qs:
                status_color = "#27ae60" if q["is_resolved"] else "#f39c12"
                status_text = "✅ 已解决" if q["is_resolved"] else "⏳ 待解答"

                col_left, col_right = st.columns([3, 1])

                with col_left:
                    st.markdown(f"""
                    <div style="padding: 1rem 1.25rem; background: #FAFBFC; border-radius: 12px;
                                border: 1px solid #E8E8E8;">
                        <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                            <div style="flex: 1;">
                                <div style="font-weight: 600; font-size: 1rem; color: #2C3E50;">
                                    ❓ {q['title']}
                                </div>
                                <div style="font-size: 0.8rem; opacity: 0.7; margin-top: 4px;">
                                    👤 {q['author']} · {q['unit']} · {q['time_ago']}
                                </div>
                                <div style="font-size: 0.85rem; color: #666; margin-top: 0.5rem;
                                            display: -webkit-box; -webkit-line-clamp: 2;
                                            -webkit-box-orient: vertical; overflow: hidden;">
                                    {q['content']}
                                </div>
                                <div style="margin-top: 0.5rem; font-size: 0.8rem;">
                                    <span style="color: {status_color}; font-weight: 500;">{status_text}</span>
                                    <span style="opacity: 0.6; margin-left: 1rem;">💬 {q['reply_count']} 回答</span>
                                    <span style="opacity: 0.6; margin-left: 1rem;">👁️ {q['view_count']} 浏览</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with col_right:
                    st.markdown("")
                    if st.button(f"📖 查看 & 解答", key=f"tch_ans_{q['id']}", use_container_width=True):
                        st.info(f"正在打开「{q['title']}」的详情页……")

                    if not q["is_resolved"]:
                        if st.button(f"✅ 标记已解决", key=f"resolve_{q['id']}",
                                     use_container_width=True, type="primary"):
                            q["is_resolved"] = True
                            st.success(f"已将「{q['title']}」标记为已解决！")
                            st.rerun()

                st.markdown("---")

    # ---- Tab 2: 已发布的统一问题 ----
    with tab_task_q:
        st.markdown("### 📢 已发布的统一思考问题")

        if not task_questions:
            st.info("📭 还没有发布过统一问题")
        else:
            for tq in task_questions:
                submit_pct = int(tq["submitted"] / tq["total_students"] * 100)
                deadline_str = tq["deadline"].strftime("%m月%d日") if hasattr(tq["deadline"], "strftime") else str(tq["deadline"])

                st.markdown(f"""
                <div style="padding: 1.25rem; background: linear-gradient(135deg, #FFF8E6, #FFF0E6);
                            border-radius: 12px; border: 1px solid #FFE0B2; margin-bottom: 1rem;">
                    <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem;">
                        <span style="font-size: 1.75rem;">📢</span>
                        <div style="flex: 1;">
                            <div style="font-weight: 600; font-size: 1.05rem; color: #E67E22;">
                                {tq['title']}
                            </div>
                            <div style="font-size: 0.8rem; opacity: 0.7;">
                                {tq['unit']} · 截止 {deadline_str} · +{tq['points']} 积分
                            </div>
                        </div>
                    </div>
                    <div style="font-size: 0.9rem; color: #555; line-height: 1.6; margin-bottom: 0.75rem;">
                        {tq['content'][:120]}{'……' if len(tq['content']) > 120 else ''}
                    </div>
                    <div style="margin-top: 0.75rem;">
                        <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 0.25rem;">
                            <span style="opacity: 0.7;">提交进度</span>
                            <span style="font-weight: 600; color: #e67e22;">{tq['submitted']}/{tq['total_students']} 人 ({submit_pct}%)</span>
                        </div>
                        <div style="height: 8px; background: #FFE0B2; border-radius: 4px; overflow: hidden;">
                            <div style="height: 100%; width: {submit_pct}%;
                                        background: linear-gradient(90deg, #f39c12, #e67e22);
                                        border-radius: 4px;"></div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    if st.button(f"📊 查看提交情况", key=f"view_tq_{tq['id']}", use_container_width=True):
                        st.info(f"正在查看「{tq['title']}」的学生提交情况……")
                with col_b:
                    remind_count = tq["total_students"] - tq["submitted"]
                    if remind_count > 0:
                        if st.button(f"🔔 提醒 ({remind_count}人)", key=f"remind_tq_{tq['id']}",
                                     use_container_width=True, type="primary"):
                            st.success(f"""
                            📣 已向 {remind_count} 名未提交的同学发送提醒！

                            提醒内容：
                            > 「{tq['title']}」还有同学没有完成哦～
                            > 截止时间：{deadline_str}
                            > 完成奖励：+{tq['points']} 积分，加油！🎯
                            """)
                            st.balloons()
                with col_c:
                    if st.button(f"🗑️ 结束任务", key=f"end_tq_{tq['id']}", use_container_width=True):
                        st.session_state["teacher_task_questions"].remove(tq)
                        st.success("任务已结束")
                        st.rerun()

                st.markdown("---")

    # ---- Tab 3: 已解决问题 ----
    with tab_resolved:
        st.markdown("### ✅ 已解决问题")
        resolved_list = [q for q in questions if q["is_resolved"]]

        if not resolved_list:
            st.info("📭 还没有已解决的问题")
        else:
            for q in resolved_list:
                st.markdown(f"""
                <div style="padding: 1rem 1.25rem; background: #F0FFF4; border-radius: 12px;
                            border: 1px solid #C8E6C9; margin-bottom: 0.75rem;">
                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                        <span style="font-size: 1.5rem;">✅</span>
                        <div style="flex: 1;">
                            <div style="font-weight: 600; color: #2E7D32;">{q['title']}</div>
                            <div style="font-size: 0.8rem; opacity: 0.7;">
                                👤 {q['author']} · {q['unit']} · {q['time_ago']} · 💬 {q['reply_count']} 回答
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"📖 查看详情", key=f"resolved_detail_{q['id']}", use_container_width=True):
                    st.info(f"正在查看「{q['title']}」的详细解答……")
                st.markdown("---")

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
            及时解答学生的疑问，可以有效提高学习积极性。
            对于高频问题，可以发布统一思考问题引导大家讨论～ 🔔
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 🎒 学生端：疑问广场
# ============================================================
def render_student_questions(user_info):
    """学生端疑问广场"""
    from datetime import datetime, timedelta
    today = datetime.now()

    # 问题数据
    questions_data = [
        {
            "id": "q1",
            "title": "Markdown 怎么插入图片？图片链接从哪里来？",
            "content": "我在做第一单元的美食网页作业，想插入一张番茄炒蛋的图片，但是不知道怎么弄。",
            "author": "小明同学",
            "unit_id": "unit1",
            "unit_name": "第一单元·网页展示",
            "tags": ["Markdown", "图片", "网页"],
            "is_resolved": True,
            "time_ago": "2天前",
            "view_count": 56,
            "reply_count": 3,
        },
        {
            "id": "q2",
            "title": "怎么把调查的数据做成饼图？",
            "content": "第二单元学了数据可视化，我收集了班级同学喜欢的口味数据，但是不知道怎么变成饼图。",
            "author": "小美",
            "unit_id": "unit2",
            "unit_name": "第二单元·数字菜谱",
            "tags": ["数据可视化", "饼图", "数据"],
            "is_resolved": True,
            "time_ago": "3天前",
            "view_count": 42,
            "reply_count": 2,
        },
        {
            "id": "q3",
            "title": "AI 生成的菜谱可以直接用吗？会不会有问题？",
            "content": "第三单元开始学AI了，我让AI帮我生成了一道创意菜的菜谱，但是我有点担心。",
            "author": "小宇",
            "unit_id": "unit3",
            "unit_name": "第三单元·智能菜谱",
            "tags": ["AI", "菜谱", "规范"],
            "is_resolved": False,
            "time_ago": "5小时前",
            "view_count": 28,
            "reply_count": 1,
        },
        {
            "id": "q4",
            "title": "表格的边框颜色怎么改？",
            "content": "做网页的时候，我想让表格更好看一些，能不能改表格边框的颜色呀？",
            "author": "小华",
            "unit_id": "unit1",
            "unit_name": "第一单元·网页展示",
            "tags": ["表格", "样式", "美化"],
            "is_resolved": False,
            "time_ago": "1天前",
            "view_count": 15,
            "reply_count": 0,
        },
        {
            "id": "q5",
            "title": "怎么收集更多数据？大家都不愿意填问卷怎么办？",
            "content": "老师让我们至少收集20条数据，我问了一圈才收集到8条。",
            "author": "小强",
            "unit_id": "unit2",
            "unit_name": "第二单元·数字菜谱",
            "tags": ["数据采集", "问卷", "方法"],
            "is_resolved": False,
            "time_ago": "6小时前",
            "view_count": 22,
            "reply_count": 1,
        },
    ]

    # 初始化提问弹窗状态
    if "show_ask_modal" not in st.session_state:
        st.session_state["show_ask_modal"] = False

    # ===== 页面顶部 =====
    st.markdown("""
    <div style="text-align: center; padding: 2rem;
                background: linear-gradient(135deg, #FFF0E6, #E8F4FD);
                border-radius: 20px; margin-bottom: 1.5rem;">
        <div style="font-size: 3rem; margin-bottom: 0.75rem;">💬</div>
        <h2 style="margin: 0; color: #2C3E50;">疑问广场</h2>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.7;">
            有问题大胆提，同学和老师都会帮你！ 🤝
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 提问按钮
    col_title, col_btn = st.columns([3, 1])
    with col_title:
        st.markdown("### 📚 大家的问题")
    with col_btn:
        if st.button("✏️ 我要提问", type="primary", use_container_width=True, key="btn_ask_question"):
            st.session_state["show_ask_modal"] = True

    # 提问表单
    if st.session_state["show_ask_modal"]:
        with st.form("ask_question_form"):
            st.markdown("#### ✏️ 提出新问题")
            q_title = st.text_input("📌 问题标题", placeholder="用一句话概括你的问题")
            col_unit, col_tag = st.columns(2)
            with col_unit:
                q_unit = st.selectbox(
                    "📚 关联单元",
                    ["第一单元·网页展示", "第二单元·数字菜谱",
                     "第三单元·智能菜谱", "第四单元·跨学科资源"],
                )
            with col_tag:
                q_tag = st.text_input("🏷️ 标签", placeholder="例如：HTML, 图片")
            q_content = st.text_area("📝 详细描述", placeholder="详细描述你的问题……", height=100)

            col_cancel, col_submit = st.columns([1, 2])
            with col_cancel:
                cancel = st.form_submit_button("取消", use_container_width=True)
            with col_submit:
                submit = st.form_submit_button("📮 发布问题", type="primary", use_container_width=True)

            if cancel:
                st.session_state["show_ask_modal"] = False
                st.rerun()
            if submit:
                if not q_title.strip():
                    st.error("请填写问题标题")
                elif not q_content.strip():
                    st.error("请填写问题描述")
                else:
                    st.session_state["show_ask_modal"] = False
                    st.success("🎉 问题发布成功！耐心等待同学和老师的解答吧～")
                    st.balloons()
                    st.rerun()

    st.markdown("---")

    # 统计卡片
    total_q = len(questions_data)
    resolved_q = sum(1 for q in questions_data if q["is_resolved"])
    unresolved_q = total_q - resolved_q

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("❓ 总问题数", total_q)
    with col2:
        st.metric("✅ 已解决", resolved_q)
    with col3:
        st.metric("⏳ 待解答", unresolved_q)

    st.markdown("---")

    # 单元筛选
    filter_options = [
        ("all", "🌐 全部问题"),
        ("unit1", "📖 第一单元"),
        ("unit2", "📊 第二单元"),
        ("unit3", "🤖 第三单元"),
        ("unit4", "🌍 第四单元"),
    ]
    cols = st.columns(len(filter_options))
    current_filter = st.session_state.get("q_filter_student", "all")

    for i, (f_val, f_label) in enumerate(filter_options):
        with cols[i]:
            is_active = current_filter == f_val
            if st.button(f_label, key=f"stu_filter_{f_val}",
                         type="primary" if is_active else "secondary",
                         use_container_width=True):
                st.session_state["q_filter_student"] = f_val
                st.rerun()

    st.markdown("---")

    # 过滤问题
    if current_filter != "all":
        filtered = [q for q in questions_data if q.get("unit_id") == current_filter]
    else:
        filtered = questions_data

    # 问题列表
    if not filtered:
        st.info("📭 这里还没有问题呢～")
    else:
        for q in filtered:
            status_color = "#27ae60" if q["is_resolved"] else "#f39c12"
            status_text = "✅ 已解决" if q["is_resolved"] else "⏳ 待解答"
            tags_html = " ".join([
                f'<span style="background: #E3F2FD; color: #1976D2; padding: 2px 8px; '
                f'border-radius: 10px; font-size: 0.75rem; margin-right: 4px;">{tag}</span>'
                for tag in q["tags"]
            ])

            st.markdown(f"""
            <div style="padding: 1rem 1.25rem; background: white; border-radius: 12px;
                        border: 1px solid #E8E8E8; margin-bottom: 0.75rem;">
                <div style="font-weight: 600; font-size: 1rem; color: #2C3E50; margin-bottom: 0.25rem;">
                    ❓ {q['title']}
                </div>
                <div style="font-size: 0.8rem; opacity: 0.7; margin-bottom: 0.5rem;">
                    👤 {q['author']} · {q['unit_name']} · {q['time_ago']}
                </div>
                <div style="font-size: 0.85rem; color: #666; margin-bottom: 0.5rem;">
                    {q['content'][:80]}{'……' if len(q['content']) > 80 else ''}
                </div>
                <div style="margin-bottom: 0.5rem;">{tags_html}</div>
                <div style="font-size: 0.8rem;">
                    <span style="color: {status_color}; font-weight: 500;">{status_text}</span>
                    <span style="opacity: 0.6; margin-left: 1rem;">💬 {q['reply_count']} 回答</span>
                    <span style="opacity: 0.6; margin-left: 1rem;">👁️ {q['view_count']} 浏览</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"📖 查看详情 & 回答", key=f"stu_q_{q['id']}", use_container_width=True):
                st.info(f"正在打开「{q['title']}」的详情页……")

            st.markdown("---")

    # 底部鼓励
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem;
                background: linear-gradient(135deg, #FFF0E6, #E8F4FD);
                border-radius: 16px; margin-top: 1rem;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🤝</div>
        <div style="font-weight: 600; color: #2C3E50; margin-bottom: 0.25rem;">
            提问不可怕，不懂才要问！
        </div>
        <div style="font-size: 0.9rem; opacity: 0.7;">
            每一个问题都是成长的机会，大胆提问，互相帮助，共同进步～ 💪
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 🚀 独立运行入口（测试用）
# ============================================================
if __name__ == "__main__":
    st.set_page_config(
        page_title="疑问广场｜美食数字菜谱",
        page_icon="💬",
        layout="wide",
    )
    if "current_user" not in st.session_state:
        st.session_state["current_user"] = {
            "id": "user_demo_001",
            "nickname": "小明同学",
            "role": "student",
        }
    if "current_role" not in st.session_state:
        st.session_state["current_role"] = "student"
    render()
