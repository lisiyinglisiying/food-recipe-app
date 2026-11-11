# -*- coding: utf-8 -*-
"""
帮助说明页面
============
提供使用指南、常见问题解答、联系方式等帮助信息

功能模块：
    1. 使用指南 - 如何使用各单元功能
    2. 常见问题FAQ
    3. 联系老师方式
    4. 关于本助教

页面入口：
    render() - 由 app.py 动态调用渲染
"""

import streamlit as st

# ===== 导入项目组件与工具 =====
from components.header import render_section_title


# ============================================================
# 📖 模块一：使用指南
# ============================================================
def render_usage_guide():
    """
    渲染使用指南
    介绍如何使用各单元功能
    """
    render_section_title(
        title="📖 使用指南",
        subtitle="快速了解美食数字菜谱智能助教的使用方法",
        icon="🧭"
    )

    # 快速上手步骤
    st.markdown("#### 🚀 快速上手（4步开启学习之旅）")

    steps = [
        {
            "step": "第一步",
            "icon": "🔐",
            "title": "登录账号",
            "content": "使用老师给你的账号密码登录，登录后就可以看到所有学习内容啦。",
            "color": "#4A90D9",
        },
        {
            "step": "第二步",
            "icon": "🏠",
            "title": "选择单元",
            "content": "从首页选择你要学习的单元，每个单元都有有趣的美食主题任务。",
            "color": "#FF9F6B",
        },
        {
            "step": "第三步",
            "icon": "🎯",
            "title": "完成任务",
            "content": "跟着任务指引一步步完成学习，提交作品，获得积分和徽章！",
            "color": "#67C28A",
        },
        {
            "step": "第四步",
            "icon": "📊",
            "title": "查看成长",
            "content": "在「成长档案」里查看你的学习进度、获得的徽章和作品集。",
            "color": "#9B59B6",
        },
    ]

    step_cols = st.columns(4)
    for i, step in enumerate(steps):
        with step_cols[i]:
            st.markdown(f"""
            <div style="text-align: center; padding: 1.5rem 1rem;
                        background: linear-gradient(180deg, {step['color']}15, {step['color']}05);
                        border-radius: 16px; height: 100%;">
                <div style="width: 50px; height: 50px; margin: 0 auto 0.75rem;
                            border-radius: 50%; background: {step['color']};
                            display: flex; align-items: center; justify-content: center;
                            font-size: 1.5rem; color: white;">
                    {step['icon']}
                </div>
                <div style="font-weight: 600; color: {step['color']}; margin-bottom: 0.25rem;">
                    {step['step']}
                </div>
                <div style="font-weight: 500; margin-bottom: 0.5rem;">
                    {step['title']}
                </div>
                <div style="font-size: 0.85rem; opacity: 0.7; line-height: 1.6;">
                    {step['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # 各单元功能介绍
    st.markdown("#### 📚 各单元功能介绍")

    unit_guides = [
        {
            "unit": "第一单元·用网页展示美食",
            "icon": "🌐",
            "color": "#4A90D9",
            "features": [
                ("✏️ Markdown沙箱", "左边写代码，右边实时预览，边学边练超有趣"),
                ("📤 作品提交", "一键提交你的美食网页作品，还能保存多个版本"),
                ("✅ 合规自查", "图片版权、隐私保护，做一个守规矩的小设计师"),
                ("🎯 分层任务", "基础版、进阶版、挑战版，选适合你的难度"),
                ("📊 互评量规", "看看同学的作品，互相学习一起进步"),
            ],
        },
        {
            "unit": "第二单元·有趣的数字菜谱",
            "icon": "📊",
            "color": "#FF9F6B",
            "features": [
                ("📋 表单生成器", "自定义问卷字段，生成专属美食调查问卷"),
                ("📝 数据录入", "表格形式录入数据，支持添加和删除行"),
                ("📊 数据可视化", "一键生成饼图、柱状图，让数据说话"),
                ("💡 思辨任务", "思考数据能解决什么真实问题"),
                ("❌ 错题诊断", "识别数据处理中的常见误区"),
            ],
        },
        {
            "unit": "第三单元·智能的数字菜谱",
            "icon": "🤖",
            "color": "#67C28A",
            "features": [
                ("🤖 AI体验", "体验AI生成菜谱、推荐美食等神奇功能"),
                ("💬 提示词技巧", "学习如何和AI对话，获得更好的结果"),
                ("📜 使用规范", "了解AI使用的边界和注意事项"),
                ("🎨 创意项目", "用AI辅助完成创意美食设计项目"),
            ],
        },
        {
            "unit": "第四单元·跨学科主题资源库",
            "icon": "📚",
            "color": "#9B59B6",
            "features": [
                ("🌍 美食与地理", "探索不同地区的美食特色"),
                ("📜 美食与历史", "了解传统美食的历史故事"),
                ("🔬 美食与科学", "美食背后的科学原理"),
                ("📦 资源整理", "学会收集、整理和分享数字资源"),
            ],
        },
    ]

    # 使用 tabs 切换各单元
    tab_titles = [f"{u['icon']} {u['unit']}" for u in unit_guides]
    tabs = st.tabs(tab_titles)

    for tab, unit in zip(tabs, unit_guides):
        with tab:
            for icon, desc in unit["features"]:
                st.markdown(f"- **{icon} {desc}**")

    st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# ❓ 模块二：常见问题 FAQ
# ============================================================
def render_faq():
    """
    渲染常见问题 FAQ
    """
    render_section_title(
        title="❓ 常见问题 FAQ",
        subtitle="大家最常问的问题都在这里，看看有没有你的答案！",
        icon="💡"
    )

    faq_list = [
        {
            "category": "📱 账号与登录",
            "questions": [
                {
                    "q": "忘记密码怎么办？",
                    "a": "别着急！可以找老师帮你重置密码，或者点击登录页面的「忘记密码」按钮，按照提示操作就可以啦。",
                },
                {
                    "q": "可以修改昵称吗？",
                    "a": "目前昵称是由老师统一设置的，如果需要修改，可以告诉老师帮你调整哦。",
                },
                {
                    "q": "怎么退出登录？",
                    "a": "点击左侧边栏底部的「🚪 退出登录」按钮就可以啦。退出后需要重新登录才能继续使用。",
                },
            ],
        },
        {
            "category": "🎨 作品与提交",
            "questions": [
                {
                    "q": "提交的作品可以修改吗？",
                    "a": "当然可以！每次修改后重新提交，系统会保存为新版本，你可以查看所有历史版本。就像写作文打草稿一样，越改越好～",
                },
                {
                    "q": "作品提交后老师多久会批改？",
                    "a": "老师通常会在 1-3 天内批改完成。如果比较急的话，可以在疑问广场提醒一下老师。",
                },
                {
                    "q": "积分和徽章有什么用？",
                    "a": "积分和徽章是你学习成果的证明！完成任务、提交作品、帮助同学都能获得积分。集齐徽章说明你已经掌握了这项技能，很厉害哦！",
                },
            ],
        },
        {
            "category": "💬 互动与互助",
            "questions": [
                {
                    "q": "怎么在疑问广场提问？",
                    "a": "进入「疑问广场」页面，点击右上角的「✏️ 我要提问」按钮，填写问题标题、内容和相关单元就可以发布啦。",
                },
                {
                    "q": "回答别人的问题有奖励吗？",
                    "a": "有的！帮助同学解答问题可以获得积分奖励，还能解锁「热心伙伴」徽章哦。帮助别人也是在巩固自己的知识～",
                },
                {
                    "q": "可以评价同学的作品吗？",
                    "a": "可以！在每个单元的「互评量规」功能里，你可以选择同学的作品进行评价，用专业的眼光给出真诚的建议。",
                },
            ],
        },
        {
            "category": "⚙️ 设置与显示",
            "questions": [
                {
                    "q": "深色模式怎么开？",
                    "a": "在左侧边栏的「显示设置」里，找到「🌙 深色模式」的开关，打开就可以啦。晚上学习用深色模式更护眼哦～",
                },
                {
                    "q": "字太小了怎么办？",
                    "a": "在左侧边栏的「显示设置」里，可以调节字体大小，有小、正常、大、特大四个档位，选一个你觉得舒服的就好。",
                },
                {
                    "q": "护眼模式是什么？",
                    "a": "护眼模式会把页面背景调成暖暖的米黄色，减少蓝光刺激，长时间学习也不容易累。长时间用电脑的时候推荐打开哦！",
                },
            ],
        },
        {
            "category": "🔧 技术问题",
            "questions": [
                {
                    "q": "页面加载不出来怎么办？",
                    "a": "试试刷新一下页面（按 F5 或点浏览器的刷新按钮）。如果还是不行，可以换个浏览器试试，推荐使用 Chrome 或 Edge 浏览器。",
                },
                {
                    "q": "图片显示不出来怎么办？",
                    "a": "检查一下图片链接是不是复制完整了，还有就是有些网站的图片不允许外链。推荐使用 Unsplash、Pexels 等免费图库的图片。",
                },
                {
                    "q": "提交作业失败怎么办？",
                    "a": "别着急！先检查一下网络连接，然后试试重新提交。如果还是不行，可以截图告诉老师，老师会帮你解决的。",
                },
            ],
        },
    ]

    # 分类 tabs
    tab_titles = [cat["category"] for cat in faq_list]
    tabs = st.tabs(tab_titles)

    for tab, category in zip(tabs, faq_list):
        with tab:
            for i, qa in enumerate(category["questions"]):
                with st.expander(f"❓ {qa['q']}", expanded=(i == 0)):
                    st.markdown(f"**💡 答案：** {qa['a']}")

    st.markdown("<br>", unsafe_allow_html=True)

    # 没有找到答案？
    st.markdown(f"""
    <div style="text-align: center; padding: 1.5rem;
                background: linear-gradient(135deg, #FFF0E6, #E8F4FD);
                border-radius: 16px;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🤔</div>
        <div style="font-weight: 600; color: #2C3E50; margin-bottom: 0.25rem;">
            没找到你的问题？
        </div>
        <div style="font-size: 0.9rem; opacity: 0.7; margin-bottom: 1rem;">
            可以去「疑问广场」提问，或者直接联系老师～
        </div>
        <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
            <span style="padding: 0.5rem 1.5rem; background: white;
                        border-radius: 25px; border: 1px solid #E9ECEF;
                        font-size: 0.9rem; cursor: pointer;">
                💬 去疑问广场提问
            </span>
            <span style="padding: 0.5rem 1.5rem; background: #4A90D9;
                        border-radius: 25px; color: white;
                        font-size: 0.9rem; cursor: pointer;">
                📧 联系老师
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# 📞 模块三：联系老师
# ============================================================
def render_contact_teacher():
    """
    渲染联系老师方式
    """
    render_section_title(
        title="📞 联系老师",
        subtitle="学习上有任何问题，都可以找老师帮忙哦～",
        icon="👨‍🏫"
    )

    col_info, col_form = st.columns([1, 1])

    with col_info:
        # 老师信息卡片
        st.markdown("#### 👨‍🏫 你的任课老师")

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #E8F4FD, #FFF0E6);
                    border-radius: 16px; padding: 1.5rem; text-align: center;">
            <div style="width: 80px; height: 80px; margin: 0 auto 1rem;
                        border-radius: 50%; background: linear-gradient(135deg, #4A90D9, #FF9F6B);
                        display: flex; align-items: center; justify-content: center;
                        font-size: 2.5rem; color: white;">
                李
            </div>
            <div style="font-weight: 600; font-size: 1.2rem; margin-bottom: 0.25rem;">
                李老师
            </div>
            <div style="font-size: 0.9rem; opacity: 0.7; margin-bottom: 1rem;">
                信息科技老师
            </div>
            <div style="display: flex; flex-direction: column; gap: 0.5rem;
                        text-align: left; font-size: 0.9rem;">
                <div style="padding: 0.5rem 0.75rem; background: white;
                            border-radius: 8px;">
                    📧 邮箱：teacher_li@example.com
                </div>
                <div style="padding: 0.5rem 0.75rem; background: white;
                            border-radius: 8px;">
                    💬 微信：meishu_ta_li
                </div>
                <div style="padding: 0.5rem 0.75rem; background: white;
                            border-radius: 8px;">
                    📍 办公室：科技楼 302 室
                </div>
                <div style="padding: 0.5rem 0.75rem; background: white;
                            border-radius: 8px;">
                    ⏰ 答疑时间：每周三、周五 16:00-17:00
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.info("""
        💡 小提示：

        - 提问前可以先看看 FAQ 和疑问广场，也许已经有答案了哦
        - 描述问题的时候尽量详细，这样老师能更快帮你解决
        - 也可以在疑问广场提问，同学和老师都会帮你
        """)

    with col_form:
        # 在线留言表单
        st.markdown("#### ✉️ 给老师留言")
        st.caption("填写下面的表单，老师会尽快回复你～")

        with st.form("contact_form"):
            contact_name = st.text_input("👤 你的姓名", placeholder="请输入你的名字")
            contact_type = st.selectbox(
                "📋 问题类型",
                options=["学习问题", "技术问题", "账号问题", "作业问题", "其他建议"],
                index=0
            )
            contact_content = st.text_area(
                "📝 留言内容",
                placeholder="详细描述你的问题或建议……",
                height=150
            )
            contact_contact = st.text_input(
                "📞 联系方式（选填）",
                placeholder="可以填你的邮箱或微信，方便老师联系你"
            )

            st.markdown("---")

            submitted = st.form_submit_button("📮 发送留言", type="primary",
                                                use_container_width=True)

            if submitted:
                if not contact_name.strip():
                    st.error("⚠️ 请填写你的姓名")
                elif not contact_content.strip():
                    st.error("⚠️ 请填写留言内容")
                else:
                    st.success(f"""
                    🎉 留言发送成功！

                    亲爱的 {contact_name}，你的留言已经发送给李老师了，
                    老师会尽快回复你的～

                    问题类型：{contact_type}
                    """)
                    st.balloons()

    st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# 🌟 模块四：关于本助教
# ============================================================
def render_about():
    """
    渲染关于本助教的信息
    """
    render_section_title(
        title="🌟 关于本助教",
        subtitle="了解美食数字菜谱智能助教的故事",
        icon="🍳"
    )

    col_about, col_info = st.columns([2, 1])

    with col_about:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #E8F4FD, #FFF0E6);
                    border-radius: 20px; padding: 2rem; text-align: center;
                    margin-bottom: 1.5rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🍳</div>
            <h3 style="margin: 0 0 0.5rem 0; color: #2C3E50;">
                美食数字菜谱智能助教
            </h3>
            <p style="margin: 0; opacity: 0.7;">
                信息科技智能助教｜七年级下册
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 📖 项目介绍")
        st.markdown("""
        美食数字菜谱智能助教是一个面向七年级学生的信息科技学习平台。

        我们以"美食"为主题，将网页制作、数据分析、人工智能、跨学科资源整合
        等信息科技知识融入有趣的美食项目中，让同学们在"做美食数字菜谱"的
        过程中，自然而然地学会各种信息科技技能。

        🌟 **我们的理念：**
        - **做中学** - 通过完成真实的项目来学习知识
        - **低门槛** - 每个同学都能轻松上手，获得成就感
        - **高 ceiling** - 有足够的挑战空间，学有余力的同学可以继续深入
        - **有温度** - 美食是有温度的，技术也应该有温度

        🎯 **我们希望：**
        每一个同学都能在这里找到学习的乐趣，
        成为会用技术、善用技术、用好技术的数字小达人！
        """)

        st.markdown("#### 🎓 学习目标")

        goals = [
            ("🌐", "信息意识", "能够自觉、有效地获取、评估、鉴别、使用信息"),
            ("💻", "计算思维", "能够运用计算机科学的思维方式解决问题"),
            ("🤝", "数字化学习与创新", "能够利用数字工具和资源进行学习和创新"),
            ("📜", "信息社会责任", "能够遵守信息伦理道德，安全、规范地使用信息技术"),
        ]

        for icon, title, desc in goals:
            st.markdown(f"- **{icon} {title}**：{desc}")

    with col_info:
        # 版本信息卡片
        st.markdown("#### 📋 版本信息")

        st.markdown(f"""
        <div style="background: #F8F9FA; border-radius: 12px; padding: 1rem;">
            <div style="margin-bottom: 0.75rem;">
                <div style="font-size: 0.8rem; opacity: 0.6; margin-bottom: 0.25rem;">当前版本</div>
                <div style="font-weight: 600; font-size: 1.1rem;">v1.0.0</div>
            </div>
            <div style="margin-bottom: 0.75rem;">
                <div style="font-size: 0.8rem; opacity: 0.6; margin-bottom: 0.25rem;">更新日期</div>
                <div>2024年3月</div>
            </div>
            <div style="margin-bottom: 0.75rem;">
                <div style="font-size: 0.8rem; opacity: 0.6; margin-bottom: 0.25rem;">适用年级</div>
                <div>七年级（下册）</div>
            </div>
            <div>
                <div style="font-size: 0.8rem; opacity: 0.6; margin-bottom: 0.25rem;">课程模块</div>
                <div>4个单元 · 18课时</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 👥 开发团队")

        st.markdown(f"""
        <div style="background: #F8F9FA; border-radius: 12px; padding: 1rem;">
            <div style="margin-bottom: 0.5rem;">
                <span style="font-weight: 500;">📚 课程设计</span><br>
                <span style="font-size: 0.85rem; opacity: 0.8;">信息科技教研组</span>
            </div>
            <div style="margin-bottom: 0.5rem;">
                <span style="font-weight: 500;">💻 技术开发</span><br>
                <span style="font-size: 0.85rem; opacity: 0.8;">教育技术中心</span>
            </div>
            <div style="margin-bottom: 0.5rem;">
                <span style="font-weight: 500;">🎨 美术设计</span><br>
                <span style="font-size: 0.85rem; opacity: 0.8;">创意设计团队</span>
            </div>
            <div>
                <span style="font-weight: 500;">🍳 美食顾问</span><br>
                <span style="font-size: 0.85rem; opacity: 0.8;">学校食堂大师傅</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 🙏 特别感谢")
        st.info("""
        感谢所有参与测试的同学们，
        你们的反馈让这个平台变得更好！ 💕
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    # 底部标语
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem;
                background: linear-gradient(135deg, #E8F4FD, #FFF0E6);
                border-radius: 20px;">
        <div style="font-size: 3rem; margin-bottom: 0.75rem;">🍳</div>
        <div style="font-weight: 600; font-size: 1.3rem; color: #2C3E50; margin-bottom: 0.5rem;">
            用代码烹饪美食，用科技点亮创意
        </div>
        <div style="font-size: 1rem; opacity: 0.7;">
            美食数字菜谱智能助教 · 陪伴每一个同学成长
        </div>
        <div style="margin-top: 1rem; font-size: 0.85rem; opacity: 0.5;">
            © 2024 信息科技智能助教 · 用心做教育
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 🎯 主函数：页面入口
# ============================================================
def render():
    """
    帮助说明页面主入口
    由 app.py 动态调用渲染
    """
    # 页面顶部
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem;
                background: linear-gradient(135deg, #E8F4FD, #FFF0E6);
                border-radius: 20px; margin-bottom: 2rem;">
        <div style="font-size: 3rem; margin-bottom: 0.75rem;">❓</div>
        <h2 style="margin: 0; color: #2C3E50;">帮助说明</h2>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.7;">
            有问题？来这里找找答案吧！ 🔍
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 快速导航
    st.markdown("#### 🚀 快速导航")
    nav_cols = st.columns(4)
    nav_items = [
        ("📖", "使用指南", "#使用指南"),
        ("❓", "常见问题", "#常见问题-faq"),
        ("📞", "联系老师", "#联系老师"),
        ("🌟", "关于我们", "#关于本助教"),
    ]
    for col, (icon, title, _) in zip(nav_cols, nav_items):
        with col:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem;
                        background: white; border-radius: 12px;
                        border: 1px solid #E9ECEF; cursor: pointer;
                        transition: all 0.2s ease;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                <div style="font-weight: 500;">{title}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # 模块一：使用指南
    render_usage_guide()

    # 模块二：常见问题
    render_faq()

    # 模块三：联系老师
    render_contact_teacher()

    # 模块四：关于本助教
    render_about()


# ============================================================
# 🚀 独立运行入口（测试用）
# ============================================================
if __name__ == "__main__":
    st.set_page_config(
        page_title="帮助说明｜美食数字菜谱",
        page_icon="❓",
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
