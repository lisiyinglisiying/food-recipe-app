# -*- coding: utf-8 -*-
"""
第一单元：用网页展示美食
=========================
Markdown 网页制作沙箱 + 作品提交 + 合规自查 + 分层任务 + 互评量规

学习目标：
    1. 认识网页的基本结构（标题、图片、文字）
    2. 学会用 Markdown 编写简单的网页内容
    3. 了解图片版权与素材合规的基本知识
    4. 完成一份美食介绍网页作品

页面布局：
    左侧  - OBE 学习目标勾选清单
    中间  - 主操作区（沙箱/编辑器/提交面板）
    右侧  - 辅助侧边栏（微课视频、脚手架提示、自查清单、参考样例）
"""

import streamlit as st
from datetime import datetime

# ===== 导入项目工具模块 =====
from utils.storage import create_work, get_works_by_user, query, get_by_id
from components.cards import work_card, task_card, stat_card
from components.header import render_section_title


# ============================================================
# 🔧 初始化 Session State（页面首次加载时准备数据）
# ============================================================
def _init_session_state():
    """初始化页面需要的会话变量"""
    # 当前登录用户（演示用，实际项目中从 auth 模块获取）
    if "current_user_id" not in st.session_state:
        st.session_state["current_user_id"] = "user_demo_001"
    if "current_username" not in st.session_state:
        st.session_state["current_username"] = "小明同学"

    # Markdown 编辑器默认内容
    if "md_editor_content" not in st.session_state:
        st.session_state["md_editor_content"] = """# 🍜 我的拿手好菜：番茄炒蛋

> 一道简单又美味的家常菜，人人都能学会！

## 📸 成品展示

![番茄炒蛋](https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400)
*图片来源：Unsplash（免费可商用）*

## 🥘 菜品介绍

番茄炒蛋是中国家庭中最常见的一道家常菜。它色香味俱全，
营养丰富，制作方法也十分简单，是很多人学做饭的"第一道菜"。

### 🌟 菜品特色
- 🍅 酸甜可口，开胃下饭
- 🥚 营养丰富，蛋白质满满
- 👨‍🍳 做法简单，新手友好

### 📝 主要食材
| 食材 | 用量 |
|------|------|
| 番茄 | 2个 |
| 鸡蛋 | 3个 |
| 葱花 | 适量 |
| 盐 | 少许 |
| 糖 | 少许 |

---

**小贴士：** 番茄要选熟透的，炒出来的汤汁更浓郁哦～
"""

    # OBE 学习目标勾选状态
    if "obe_goals" not in st.session_state:
        st.session_state["obe_goals"] = {
            "goal_1": {"text": "能说出网页的三个基本组成部分", "checked": False},
            "goal_2": {"text": "会使用 Markdown 编写标题、图片和文字", "checked": False},
            "goal_3": {"text": "能提交一份完整的美食介绍网页作品", "checked": False},
            "goal_4": {"text": "知道图片版权的基本概念，会标注图片来源", "checked": False},
            "goal_5": {"text": "能对同学作品进行有礼貌的互评", "checked": False},
        }

    # 作品版本历史（演示数据）
    if "work_versions" not in st.session_state:
        st.session_state["work_versions"] = []

    # 合规自查勾选状态
    if "compliance_checks" not in st.session_state:
        st.session_state["compliance_checks"] = {
            "check_1": {"text": "我使用的图片来自免费图库（如 Unsplash、Pexels）", "checked": False},
            "check_2": {"text": "每张图片下面都标注了来源", "checked": False},
            "check_3": {"text": "我没有直接从搜索引擎随意下载别人的图片", "checked": False},
            "check_4": {"text": "我使用的文字是自己写的，没有大段抄袭", "checked": False},
            "check_5": {"text": "作品中没有出现个人隐私信息（家庭住址、电话等）", "checked": False},
        }

    # 当前选中的任务难度
    if "selected_task_level" not in st.session_state:
        st.session_state["selected_task_level"] = "基础版"


# ============================================================
# 📚 左侧：OBE 学习目标栏
# ============================================================
def render_left_obe_panel():
    """
    渲染左侧 OBE 预期成果勾选清单
    学生每完成一个目标，可以自行勾选，追踪学习进度
    """
    st.markdown("### 🎯 本单元学习目标")
    st.caption("学完本单元，你将能做到：")

    # 遍历所有目标，渲染复选框
    goal_count = len(st.session_state["obe_goals"])
    checked_count = sum(
        1 for g in st.session_state["obe_goals"].values() if g["checked"]
    )

    # 进度条（可视化进度）
    progress = checked_count / goal_count if goal_count > 0 else 0
    st.progress(progress)
    st.caption(f"已完成 {checked_count}/{goal_count} 个目标 🌟")

    st.markdown("---")

    for key, goal in st.session_state["obe_goals"].items():
        # 使用复选框让学生自主勾选
        new_val = st.checkbox(
            goal["text"],
            value=goal["checked"],
            key=f"obe_{key}",
            help="完成后就打个勾吧！"
        )
        # 同步更新状态
        if new_val != goal["checked"]:
            st.session_state["obe_goals"][key]["checked"] = new_val

    st.markdown("---")

    # 鼓励语
    if progress == 1.0:
        st.success("🎉 太棒了！你已经完成了所有学习目标！")
    elif progress >= 0.6:
        st.info("💪 加油！胜利就在眼前～")
    else:
        st.info("🌱 一步一步来，每个小目标都是成长的脚印！")


# ============================================================
# 🎨 中间：主操作区 —— 1. Markdown 实时预览沙箱
# ============================================================
def render_md_sandbox():
    """
    Markdown 简易网页实时预览沙箱
    左右分栏：左侧编辑区，右侧预览区
    支持基础 Markdown 语法：标题、粗体、图片、列表、表格等
    """
    render_section_title(
        title="✏️ Markdown 网页创作沙箱",
        subtitle="左边写代码，右边看效果，边学边练超有趣！",
        icon="🎨"
    )

    # 左右分栏布局
    left_col, right_col = st.columns(2)

    # ---------- 左侧：编辑器 ----------
    with left_col:
        st.markdown("**📝 编辑区**（写 Markdown 代码）")

        # 语法小提示（可折叠）
        with st.expander("📖 点击查看 Markdown 语法小抄", expanded=False):
            st.markdown("""
            | 语法 | 效果 |
            |------|------|
            | `# 一级标题` | 大标题 |
            | `## 二级标题` | 中标题 |
            | `**粗体文字**` | **粗体** |
            | `*斜体文字*` | *斜体* |
            | `![图片名](网址)` | 插入图片 |
            | `- 列表项` | 无序列表 |
            | `> 引用文字` | 引用块 |
            | `---` | 分隔线 |
            """)
            st.caption("💡 小提示：试着修改左边的内容，右边会实时变化哦！")

        # 文本编辑框
        new_content = st.text_area(
            "在这里输入你的 Markdown 代码：",
            value=st.session_state["md_editor_content"],
            height=450,
            key="md_textarea_main",
            help="输入 Markdown 语法，右边会实时显示预览效果"
        )
        # 实时同步到 session state
        st.session_state["md_editor_content"] = new_content

        # 快捷模板按钮
        st.caption("🎯 快捷模板：")
        tpl_col1, tpl_col2, tpl_col3 = st.columns(3)
        with tpl_col1:
            if st.button("🍜 菜品介绍", key="tpl_food", use_container_width=True):
                st.session_state["md_editor_content"] = """# 🍜 菜名

> 一句话介绍这道菜

## 📸 成品展示
![菜品图片](https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400)
*图片来源：Unsplash*

## 🥘 菜品介绍

在这里介绍这道菜的故事和特点……

### 🌟 特色
- 特色一
- 特色二

---
**小贴士：** 你的小提示～
"""
                st.rerun()
        with tpl_col2:
            if st.button("📋 菜谱做法", key="tpl_recipe", use_container_width=True):
                st.session_state["md_editor_content"] = """# 📋 菜谱名称

## 🥗 准备食材
| 食材 | 用量 |
|------|------|
| 食材1 | 适量 |
| 食材2 | 适量 |

## 👨‍🍳 制作步骤
1. 第一步：……
2. 第二步：……
3. 第三步：……

## 💡 小贴士
- 小提示一
- 小提示二
"""
                st.rerun()
        with tpl_col3:
            if st.button("🎨 空白画布", key="tpl_blank", use_container_width=True):
                st.session_state["md_editor_content"] = "# 我的美食网页\n\n在这里开始你的创作吧！\n\n"
                st.rerun()

    # ---------- 右侧：预览区 ----------
    with right_col:
        st.markdown("**👀 预览区**（实时查看网页效果）")

        # 模拟浏览器窗口效果
        preview_header = """
        <div style="border: 2px solid #e0e0e0; border-radius: 10px; overflow: hidden;
                    background: white; min-height: 450px;">
            <div style="background: #f5f5f5; padding: 8px 12px; border-bottom: 1px solid #e0e0e0;
                        display: flex; align-items: center; gap: 6px;">
                <span style="width: 12px; height: 12px; border-radius: 50%; background: #ff5f57;"></span>
                <span style="width: 12px; height: 12px; border-radius: 50%; background: #febc2e;"></span>
                <span style="width: 12px; height: 12px; border-radius: 50%; background: #28c840;"></span>
                <span style="margin-left: 10px; font-size: 0.8rem; color: #999;">🌐 我的美食网页</span>
            </div>
            <div style="padding: 15px;">
        """
        st.markdown(preview_header, unsafe_allow_html=True)

        # 真正的 Markdown 渲染
        st.markdown(st.session_state["md_editor_content"])

        st.markdown("</div></div>", unsafe_allow_html=True)

        # 字数统计
        word_count = len(st.session_state["md_editor_content"])
        st.caption(f"📊 字数统计：{word_count} 字  |  💡 建议：100-500 字最合适")


# ============================================================
# 📤 中间：主操作区 —— 2. 作品提交与版本管理
# ============================================================
def render_submit_panel():
    """
    美食作品在线提交与多版本存档
    - 提交按钮：将当前编辑内容保存为新版本
    - 版本历史列表：查看、恢复历史版本
    """
    render_section_title(
        title="📤 作品提交与版本存档",
        subtitle="每次提交都会保存一个版本，随时可以回看修改记录哦！",
        icon="📦"
    )

    # ---- 提交区域 ----
    submit_col1, submit_col2, submit_col3 = st.columns([2, 1, 1])

    with submit_col1:
        work_title = st.text_input(
            "📝 作品标题",
            value="我的美食介绍网页",
            key="work_title_input",
            help="给你的作品起个好听的名字吧！"
        )

    with submit_col2:
        work_tags_input = st.text_input(
            "🏷️ 标签（用逗号分隔）",
            value="番茄炒蛋,家常菜",
            key="work_tags_input",
            help="方便以后搜索和分类"
        )

    with submit_col3:
        # 提交按钮
        st.markdown("<br>", unsafe_allow_html=True)  # 一点垂直间距
        submit_btn = st.button(
            "🚀 提交作品",
            key="submit_work_btn",
            type="primary",
            use_container_width=True
        )

    # 处理提交逻辑
    if submit_btn:
        # 生成版本号
        version_num = len(st.session_state["work_versions"]) + 1

        # 创建版本记录
        version_record = {
            "version": f"v{version_num}.0",
            "title": work_title,
            "content": st.session_state["md_editor_content"],
            "tags": [t.strip() for t in work_tags_input.split(",") if t.strip()],
            "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "word_count": len(st.session_state["md_editor_content"]),
        }

        # 保存到本地版本历史
        st.session_state["work_versions"].insert(0, version_record)

        # 同时存入数据存储（用于成长档案）
        try:
            create_work(
                user_id=st.session_state["current_user_id"],
                unit_id="unit1",
                title=work_title,
                content=st.session_state["md_editor_content"],
                description=f"第{version_num}版作品",
                tags=[t.strip() for t in work_tags_input.split(",") if t.strip()],
            )
        except Exception as e:
            # 存储失败不影响体验，只做提示
            st.warning(f"💾 本地存档已保存（云同步提示：{e}）")

        st.success(f"""
        🎉 作品提交成功！这是你的第 **{version_num}** 版作品～

        - 版本号：v{version_num}.0
        - 字数：{version_record['word_count']} 字
        - 标签：{', '.join(version_record['tags'])}
        """)

        # 完成对应的学习目标
        if not st.session_state["obe_goals"]["goal_3"]["checked"]:
            st.session_state["obe_goals"]["goal_3"]["checked"] = True
            st.balloons()

    # ---- 版本历史列表 ----
    st.markdown("#### 📜 版本历史")

    versions = st.session_state["work_versions"]

    if not versions:
        # 没有版本时的友好提示
        st.info("""
        📭 还没有提交过作品呢～

        在上方的沙箱里编辑好内容，点击 **"🚀 提交作品"** 按钮，
        你的第一个版本就会出现在这里啦！
        """)
    else:
        # 有版本时，用可折叠面板展示每个版本
        for idx, ver in enumerate(versions):
            with st.expander(
                f"📌 {ver['version']} ｜ {ver['title']} ｜ {ver['submitted_at']}",
                expanded=(idx == 0)  # 最新版本默认展开
            ):
                col_a, col_b, col_c = st.columns([1, 1, 2])
                with col_a:
                    st.metric("字数", ver["word_count"])
                with col_b:
                    st.metric("标签数", len(ver["tags"]))
                with col_c:
                    # 标签展示
                    tags_html = " ".join(
                        [f'<span class="ms-tag" style="margin: 2px;">{t}</span>' for t in ver["tags"]]
                    )
                    st.markdown(f"**标签：** {tags_html}", unsafe_allow_html=True)

                # 操作按钮
                btn_col1, btn_col2, btn_col3 = st.columns(3)
                with btn_col1:
                    if st.button(f"📖 预览此版本", key=f"preview_ver_{idx}", use_container_width=True):
                        st.session_state["md_editor_content"] = ver["content"]
                        st.success(f"✨ 已加载 {ver['version']} 的内容到编辑器，可以继续修改～")
                        st.rerun()
                with btn_col2:
                    if st.button(f"📝 基于此版本修改", key=f"edit_ver_{idx}", use_container_width=True):
                        st.session_state["md_editor_content"] = ver["content"]
                        st.info("✏️ 已复制到编辑器，修改后提交就是新版本啦！")
                        st.rerun()
                with btn_col3:
                    st.caption("提交时间：" + ver["submitted_at"])

        # 版本统计
        st.info(f"📊 你已经提交了 **{len(versions)}** 个版本，每一次修改都是进步！ 💪")


# ============================================================
# ✅ 中间：主操作区 —— 3. 网页素材合规自查
# ============================================================
def render_compliance_check():
    """
    网页素材合规自查清单
    - 图片版权提醒
    - 来源标注检查
    - 隐私信息自查
    """
    render_section_title(
        title="✅ 网页素材合规自查清单",
        subtitle="做一个尊重版权、遵守规则的小小网页设计师！",
        icon="🛡️"
    )

    # 上方重要提醒（醒目卡片）
    warning_html = """
    <div style="background: linear-gradient(135deg, #FFF3CD, #FFEAA7);
                border-left: 5px solid #FFC107; padding: 1rem; border-radius: 8px;
                margin-bottom: 1rem;">
        <div style="font-weight: bold; color: #856404; font-size: 1.1rem; margin-bottom: 0.5rem;">
            ⚠️ 图片版权小知识
        </div>
        <div style="color: #856404; font-size: 0.9rem; line-height: 1.6;">
            <p style="margin: 0.25rem 0;">🌐 <b>可以用的图片：</b>免费图库网站（Unsplash、Pexels、Pixabay）的图片</p>
            <p style="margin: 0.25rem 0;">📷 <b>最好的图片：</b>自己拍摄的美食照片！</p>
            <p style="margin: 0.25rem 0;">🚫 <b>不能随便用的：</b>百度图片直接搜到的、别人的摄影作品、有版权标识的图片</p>
        </div>
    </div>
    """
    st.markdown(warning_html, unsafe_allow_html=True)

    # 自查清单
    st.markdown("#### 📋 自查清单（完成一项就打个勾吧！）")

    all_checked = True
    for key, check in st.session_state["compliance_checks"].items():
        col_cb, col_text = st.columns([1, 20])
        with col_cb:
            new_val = st.checkbox(
                "",
                value=check["checked"],
                key=f"compliance_{key}",
                label_visibility="collapsed"
            )
        with col_text:
            st.markdown(f"{check['text']}")

        if new_val != check["checked"]:
            st.session_state["compliance_checks"][key]["checked"] = new_val

        if not new_val:
            all_checked = False

    st.markdown("---")

    # 自查结果
    total_checks = len(st.session_state["compliance_checks"])
    passed_count = sum(
        1 for c in st.session_state["compliance_checks"].values() if c["checked"]
    )

    result_col1, result_col2 = st.columns([1, 2])
    with result_col1:
        # 进度环效果（用进度条代替）
        st.metric("合规得分", f"{passed_count}/{total_checks}")
        st.progress(passed_count / total_checks if total_checks > 0 else 0)

    with result_col2:
        if all_checked:
            st.success("""
            🎊 恭喜你！所有自查项都通过啦～

            你是一个尊重版权、遵守规则的优秀小设计师！
            现在可以放心地提交你的作品了 ✨
            """)
            # 自动勾选学习目标
            if not st.session_state["obe_goals"]["goal_4"]["checked"]:
                st.session_state["obe_goals"]["goal_4"]["checked"] = True
        elif passed_count >= total_checks * 0.6:
            st.info("""
            👍 已经完成了大部分自查项，继续加油！

            还没勾选的项目记得检查一下哦，
            确保你的作品合规又安全～
            """)
        else:
            st.warning("""
            📝 还有不少项目需要检查呢～

            慢慢来，一项一项对照着检查，
            这是成为专业设计师的必经之路！💪
            """)

    # 免费图库推荐
    with st.expander("🔗 推荐免费图片网站（点击展开）", expanded=False):
        st.markdown("""
        这些网站的图片都可以免费使用，不用担心版权问题：

        | 网站名 | 特点 | 网址 |
        |--------|------|------|
        | Unsplash | 高质量摄影图，种类丰富 | unsplash.com |
        | Pexels | 图片和视频都有，中文界面 | pexels.com |
        | Pixabay | 插画、矢量图也很多 | pixabay.com |
        | 美食天下 | 中文美食图片（注意看授权） | meishichina.com |

        💡 **小提示：** 使用时最好在图片下面标注"图片来源：XXX"，这样更规范哦！
        """)


# ============================================================
# 🎯 中间：主操作区 —— 4. 网页分层任务包
# ============================================================
def render_task_packages():
    """
    网页分层任务包
    - 基础版：美食介绍页（单页）
    - 进阶版：多页面菜谱网站
    - 挑战版：带导航美食站点
    """
    render_section_title(
        title="🎯 分层任务包",
        subtitle="选择适合你的挑战等级，一步一步成为网页小达人！",
        icon="🏆"
    )

    # 难度选择（单选按钮）
    level = st.radio(
        "选择你的挑战等级：",
        options=["🌱 基础版", "🌿 进阶版", "🌳 挑战版"],
        index=0,
        key="task_level_radio",
        horizontal=True,
        help="选择适合自己的难度，也可以从基础版开始逐步挑战！"
    )

    # 提取等级名称（去掉 emoji）
    level_name = level.split(" ")[1]
    st.session_state["selected_task_level"] = level_name

    st.markdown("---")

    # ===== 基础版任务 =====
    if level_name == "基础版":
        # 任务卡片
        task_card(
            task_title="基础任务：我的美食介绍页",
            task_description="制作一个单页面的美食介绍网页，包含标题、一张美食图片和一段介绍文字。",
            task_type="normal",
            status="pending",
            points=50,
            deadline="本周内完成",
            task_icon="🌱",
            card_key="task_basic"
        )

        st.markdown("#### 📝 任务要求")
        st.markdown("""
        - ✅ 有一个醒目的大标题（菜名）
        - ✅ 有一张清晰的美食图片（注意版权哦！）
        - ✅ 有至少 100 字的菜品介绍
        - ✅ 图片下面标注了来源
        - ✅ 排版整齐，看起来舒服

        💡 **建议时间：** 30-45 分钟
        🎁 **完成奖励：** 50 积分 + "初试锋芒" 徽章
        """)

        with st.expander("📖 任务脚手架（点击展开步骤提示）", expanded=False):
            st.markdown("""
            **第一步：确定主题**
            - 想一想你要介绍哪一道美食？
            - 给你的网页起一个好听的标题

            **第二步：准备素材**
            - 在免费图库网站找一张美食图片
            - 复制图片的网址（URL）

            **第三步：编写内容**
            - 用 `#` 写标题
            - 用 `![](图片网址)` 插入图片
            - 用普通文字写介绍

            **第四步：检查提交**
            - 对照自查清单检查一遍
            - 点击提交按钮保存作品
            """)

        if st.button("🚀 开始基础版挑战", key="start_basic", type="primary", use_container_width=True):
            # 加载基础模板
            st.session_state["md_editor_content"] = """# 🍜 我的拿手好菜

> 一句话介绍这道菜～

## 📸 美食图片

![美食图片](https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500)
*图片来源：Unsplash*

## 🥘 菜品介绍

在这里写一写这道菜的故事、味道、特点……

比如：它是哪里的菜？吃起来什么感觉？你为什么喜欢它？

---

**小贴士：** 写一写你和这道菜的小故事吧～
"""
            st.success("✨ 已加载基础版模板，快去沙箱里创作吧！")
            st.rerun()

    # ===== 进阶版任务 =====
    elif level_name == "进阶版":
        task_card(
            task_title="进阶任务：多页面菜谱网站",
            task_description="制作包含首页和菜谱详情页的多页面网站，添加食材清单和制作步骤。",
            task_type="normal",
            status="pending",
            points=100,
            deadline="两周内完成",
            task_icon="🌿",
            card_key="task_intermediate"
        )

        st.markdown("#### 📝 任务要求")
        st.markdown("""
        - ✅ 首页：展示多道菜品的缩略图和简介
        - ✅ 详情页：每道菜有详细的做法介绍
        - ✅ 包含食材清单表格
        - ✅ 包含分步骤的制作方法
        - ✅ 至少介绍 2 道菜
        - ✅ 所有图片都标注了来源

        💡 **建议时间：** 60-90 分钟
        🎁 **完成奖励：** 100 积分 + "小有所成" 徽章
        """)

        with st.expander("📖 任务脚手架（点击展开步骤提示）", expanded=False):
            st.markdown("""
            **第一步：规划内容**
            - 决定介绍哪几道菜（至少 2 道）
            - 每道菜准备一张图片

            **第二步：制作首页**
            - 网站大标题
            - 每道菜的缩略图和简短介绍
            - 用分隔线分开不同菜品

            **第三步：制作详情页**
            - 每道菜的详细介绍
            - 食材表格（用 Markdown 表格语法）
            - 制作步骤（用有序列表）

            **第四步：添加链接（可选挑战）**
            - 在首页和详情页之间添加跳转链接
            """)

        if st.button("🚀 开始进阶版挑战", key="start_intermediate", type="primary", use_container_width=True):
            st.session_state["md_editor_content"] = """# 🍳 我的私房菜谱网站

> 欢迎来到我的美食小站！这里有我最爱的几道家常菜～

---

## 📚 菜谱目录

### 🍅 番茄炒蛋
![番茄炒蛋](https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=300)
*图片来源：Unsplash*

一道简单又美味的家常菜，酸甜可口，超级下饭！

[👉 查看详细做法](#番茄炒蛋的做法)

---

### 🥒 拍黄瓜
![拍黄瓜](https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=300)
*图片来源：Unsplash*

清爽开胃的凉拌菜，夏天吃最舒服啦！

[👉 查看详细做法](#拍黄瓜的做法)

---

# 🍅 番茄炒蛋的做法

## 🥗 准备食材
| 食材 | 用量 |
|------|------|
| 番茄 | 2个 |
| 鸡蛋 | 3个 |
| 葱花 | 适量 |
| 盐 | 少许 |
| 糖 | 少许 |

## 👨‍🍳 制作步骤
1. 番茄洗净切块，鸡蛋打散备用
2. 热锅倒油，倒入蛋液炒至凝固盛出
3. 锅中再倒少许油，放入番茄翻炒出汁
4. 加入炒好的鸡蛋，加盐和糖调味
5. 撒上葱花，出锅装盘！

## 💡 小贴士
- 番茄要选熟透的，汤汁更浓郁
- 喜欢酸甜口的可以多加点糖

---

# 🥒 拍黄瓜的做法

## 🥗 准备食材
| 食材 | 用量 |
|------|------|
| 黄瓜 | 1根 |
| 大蒜 | 3瓣 |
| 生抽 | 2勺 |
| 醋 | 1勺 |
| 香油 | 几滴 |

## 👨‍🍳 制作步骤
1. 黄瓜洗净，用刀背拍碎
2. 拍好的黄瓜切段放入碗中
3. 大蒜切末撒在黄瓜上
4. 加入生抽、醋、香油拌匀
5. 放入冰箱冷藏10分钟更美味！

---

*🍴 更多菜谱持续更新中……*
"""
            st.success("✨ 已加载进阶版模板，快去沙箱里修改吧！")
            st.rerun()

    # ===== 挑战版任务 =====
    elif level_name == "挑战版":
        task_card(
            task_title="挑战任务：带导航的美食站点",
            task_description="制作一个有导航栏、多个页面和底部信息的完整美食网站，展现你的设计才华！",
            task_type="challenge",
            status="pending",
            points=200,
            deadline="本月内完成",
            task_icon="🌳",
            card_key="task_challenge"
        )

        st.markdown("#### 📝 任务要求")
        st.markdown("""
        - ✅ 顶部有导航栏（首页、菜谱列表、关于我等）
        - ✅ 至少 3 个不同的页面/板块
        - ✅ 有 footer 底部信息（版权声明、联系方式等）
        - ✅ 整体设计有统一的风格
        - ✅ 排版精美，有设计感
        - ✅ 所有素材都符合版权规范

        💡 **建议时间：** 2-3 小时
        🎁 **完成奖励：** 200 积分 + "创意之星" 徽章
        """)

        with st.expander("📖 任务脚手架（点击展开步骤提示）", expanded=False):
            st.markdown("""
            **第一步：网站规划**
            - 你的网站叫什么名字？
            - 有哪些栏目？（首页、菜谱、关于我……）
            - 整体风格是什么？（可爱风、简约风、中国风……）

            **第二步：设计导航栏**
            - 网站 Logo / 标题
            - 导航菜单链接
            - 用分隔线或特殊样式突出导航区

            **第三步：制作各个页面**
            - 首页：欢迎语 + 精选推荐
            - 菜谱页：多道菜的详细介绍
            - 关于页：介绍你自己和这个网站

            **第四步：添加页脚**
            - 版权声明
            - 感谢语
            - 联系信息（注意保护隐私！）

            **第五步：美化润色**
            - 统一的标题风格
            - 合适的表情符号点缀
            - 清晰的段落分隔
            """)

        if st.button("🚀 开始挑战版任务", key="start_challenge", type="primary", use_container_width=True):
            st.session_state["md_editor_content"] = """# 🍜 美味小厨
*—— 一个热爱美食的小学生的个人网站 ——*

> **🧭 导航：** [🏠 首页](#首页) | [📖 菜谱大全](#菜谱大全) | [👩‍🍳 关于我](#关于我)

---

# 🏠 首页

## 🌟 欢迎来到美味小厨！

嗨，我是小厨神👋 这是我的美食小站，
在这里我会分享自己喜欢的美食和做法～

## 🔥 本周推荐

### 🥇 第一名：红烧肉
![红烧肉](https://images.unsplash.com/photo-1544025162-d76694265947?w=400)
*图片来源：Unsplash*

肥而不腻，入口即化，我的最爱！

### 🥈 第二名：寿司
![寿司](https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=400)
*图片来源：Unsplash*

颜值超高的日本料理，做起来也很有趣！

### 🥉 第三名：水果沙拉
![水果沙拉](https://images.unsplash.com/photo-1490474418585-ba9bad8fd0ea?w=400)
*图片来源：Unsplash*

清爽健康，好吃不胖～

[📖 查看更多菜谱 →](#菜谱大全)

---

# 📖 菜谱大全

## 🍖 肉类菜谱

### 红烧肉
- **难度：** ⭐⭐⭐
- **时间：** 90分钟
- **评分：** ⭐⭐⭐⭐⭐

### 可乐鸡翅
- **难度：** ⭐⭐
- **时间：** 30分钟
- **评分：** ⭐⭐⭐⭐

## 🥬 素菜菜谱

### 地三鲜
- **难度：** ⭐⭐
- **时间：** 20分钟
- **评分：** ⭐⭐⭐⭐

### 蒜蓉西兰花
- **难度：** ⭐
- **时间：** 10分钟
- **评分：** ⭐⭐⭐

## 🍰 甜点饮品

### 草莓奶昔
- **难度：** ⭐
- **时间：** 5分钟
- **评分：** ⭐⭐⭐⭐⭐

### 芒果布丁
- **难度：** ⭐⭐
- **时间：** 30分钟+冷藏
- **评分：** ⭐⭐⭐⭐

---

# 👩‍🍳 关于我

## 👋 你好呀！

我是一个热爱美食的小学生，
特别喜欢看妈妈做饭，也喜欢自己动手做美食～

## 🎯 我的梦想

成为一名美食设计师，
把好吃的东西做得又好看又美味！

## 📫 联系我

- 🏫 XX学校 七年级
- 📧 我的邮箱：example@email.com
- 💬 欢迎和我交流美食心得！

---

---

## 📮 页脚

© 2024 美味小厨 ｜ 用 ❤️ 制作
*本站图片均来自 Unsplash，遵循 CC0 协议*

[🔝 回到顶部](#美味小厨)
"""
            st.success("✨ 已加载挑战版模板，展现你的创意吧！")
            st.rerun()


# ============================================================
# 📊 中间：主操作区 —— 5. 作品互评量规卡
# ============================================================
def render_peer_rubric():
    """
    作品互评量规卡
    三个维度：排版、信息完整性、分享规范
    每个维度有评分标准和分数滑块
    """
    render_section_title(
        title="📊 作品互评量规卡",
        subtitle="用专业的眼光欣赏同学的作品，给出真诚的评价和建议！",
        icon="🎖️"
    )

    # 选择要评价的作品（演示用，实际项目中从作品列表选择）
    st.markdown("#### 🎯 选择评价作品")
    work_options = [
        "小明的《番茄炒蛋》作品",
        "小红的《北京烤鸭》作品",
        "小刚的《川菜美食之旅》作品",
    ]
    selected_work = st.selectbox(
        "选择你要评价的作品：",
        options=work_options,
        key="peer_selected_work",
        help="从同学的作品中选一个来评价吧"
    )

    # 预览作品（可折叠）
    with st.expander("👀 点击预览该作品", expanded=True):
        st.info("📝 这里会显示同学的作品内容，方便你对照评价～")
        # 演示用预览
        st.markdown(f"""
        # 🍜 {selected_work}

        > 这是一道美味的家常菜～

        ## 📸 美食图片
        ![美食图片](https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400)
        *图片来源：Unsplash*

        ## 🥘 菜品介绍
        这道菜很好吃，我很喜欢。它的做法很简单，大家都可以试试。

        ### 食材
        - 食材1
        - 食材2
        """)

    st.markdown("---")

    # ===== 评分区域 =====
    st.markdown("#### ⭐ 评分（拖动滑块给分）")

    # 维度1：排版
    st.markdown("##### 🎨 维度一：排版美观度（20分）")
    layout_score = st.slider(
        "排版得分",
        min_value=0,
        max_value=20,
        value=15,
        step=1,
        key="rubric_layout",
        help="页面看起来舒服吗？层次分明吗？"
    )

    # 评分标准提示
    layout_standards = {
        (0, 5): "🔴 待改进 - 排版混乱，找不到重点",
        (6, 10): "🟡 一般 - 有基本结构，但不够美观",
        (11, 15): "🟢 良好 - 排版整齐，层次清晰",
        (16, 20): "🌟 优秀 - 设计精美，赏心悦目",
    }
    for (low, high), desc in layout_standards.items():
        if low <= layout_score <= high:
            st.caption(f"评分标准参考：{desc}")
            break

    st.markdown("---")

    # 维度2：信息完整性
    st.markdown("##### 📚 维度二：信息完整性（40分）")
    info_score = st.slider(
        "信息完整度得分",
        min_value=0,
        max_value=40,
        value=30,
        step=1,
        key="rubric_info",
        help="信息够不够丰富？介绍清楚了吗？"
    )

    info_standards = {
        (0, 10): "🔴 待改进 - 内容太少，信息不完整",
        (11, 20): "🟡 一般 - 有基本信息，但不够详细",
        (21, 30): "🟢 良好 - 内容丰富，介绍清楚",
        (31, 40): "🌟 优秀 - 信息详尽，引人入胜",
    }
    for (low, high), desc in info_standards.items():
        if low <= info_score <= high:
            st.caption(f"评分标准参考：{desc}")
            break

    st.markdown("---")

    # 维度3：分享规范
    st.markdown("##### 📜 维度三：分享规范性（40分）")
    norm_score = st.slider(
        "分享规范得分",
        min_value=0,
        max_value=40,
        value=35,
        step=1,
        key="rubric_norm",
        help="图片有版权吗？来源标注了吗？有没有隐私问题？"
    )

    norm_standards = {
        (0, 10): "🔴 待改进 - 版权问题严重，来源未标注",
        (11, 20): "🟡 一般 - 部分图片未标注来源",
        (21, 30): "🟢 良好 - 基本合规，大部分有标注",
        (31, 40): "🌟 优秀 - 完全合规，所有来源清晰标注",
    }
    for (low, high), desc in norm_standards.items():
        if low <= norm_score <= high:
            st.caption(f"评分标准参考：{desc}")
            break

    st.markdown("---")

    # ===== 总分计算 =====
    total_score = layout_score + info_score + norm_score

    score_col1, score_col2, score_col3, score_col4 = st.columns(4)
    with score_col1:
        st.metric("排版得分", f"{layout_score}/20")
    with score_col2:
        st.metric("信息完整", f"{info_score}/40")
    with score_col3:
        st.metric("分享规范", f"{norm_score}/40")
    with score_col4:
        st.metric("🎉 总分", f"{total_score}/100")

    # 等级评定
    if total_score >= 90:
        grade = "🌟 S级 - 完美作品"
        grade_color = "#f39c12"
    elif total_score >= 80:
        grade = "🥇 A级 - 优秀作品"
        grade_color = "#27ae60"
    elif total_score >= 60:
        grade = "🥈 B级 - 良好作品"
        grade_color = "#3498db"
    elif total_score >= 40:
        grade = "🥉 C级 - 继续加油"
        grade_color = "#9b59b6"
    else:
        grade = "💪 D级 - 需要努力"
        grade_color = "#e74c3c"

    st.markdown(f"""
    <div style="text-align: center; padding: 1rem; background: {grade_color}15;
                border-radius: 10px; border: 2px solid {grade_color}30;">
        <div style="font-size: 1.5rem; font-weight: bold; color: {grade_color};">
            {grade}
        </div>
        <div style="font-size: 0.9rem; opacity: 0.7; margin-top: 0.25rem;">
            总分 {total_score} / 100
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ===== 评语与建议 =====
    st.markdown("#### 💬 评语和建议")

    # 鼓励语单选
    encouragement = st.radio(
        "选一句鼓励的话送给同学吧：",
        [
            "👏 太棒了！我要向你学习！",
            "👍 做得很好，继续加油！",
            "😊 很不错，有进步空间哦～",
            "💪 继续努力，你会更棒的！",
        ],
        key="rubric_encouragement",
        help="互评要先肯定优点，再提建议哦～"
    )

    # 优点
    st.markdown("**🌟 作品的优点：**")
    good_points = st.text_area(
        "说说你最喜欢这个作品的哪些地方？",
        value="排版很整齐，图片选得很好看！",
        height=80,
        key="rubric_good",
        help="先夸一夸，真诚地说出优点"
    )

    # 建议
    st.markdown("**💡 改进建议：**")
    suggestions = st.text_area(
        "你觉得哪些地方可以做得更好？",
        value="如果介绍文字再多一点就更完美了～",
        height=80,
        key="rubric_suggestions",
        help="提出友好的建议，帮助同学进步"
    )

    # 提交评价按钮
    submit_rating = st.button(
        "📮 提交评价",
        key="submit_peer_rating",
        type="primary",
        use_container_width=True
    )

    if submit_rating:
        st.success(f"""
        🎉 评价提交成功！谢谢你的真诚反馈～

        **评价概览：**
        - 评价作品：{selected_work}
        - 总分：{total_score}/100（{grade}）
        - 鼓励语：{encouragement}

        💡 小提示：给同学评价也是在学习哦，
        看看别人的优点，想想自己的作品可以怎么改进～
        """)

        # 完成学习目标
        if not st.session_state["obe_goals"]["goal_5"]["checked"]:
            st.session_state["obe_goals"]["goal_5"]["checked"] = True


# ============================================================
# 📎 右侧：辅助侧边栏
# ============================================================
def render_right_sidebar():
    """
    右侧辅助侧边栏
    包含：微课视频链接、脚手架提示、自查清单、参考样例
    """
    # 1. 微课视频
    st.markdown("### 🎬 微课视频")
    video_items = [
        {"icon": "📺", "title": "什么是网页？", "duration": "3分钟", "key": "v1"},
        {"icon": "✏️", "title": "Markdown 入门", "duration": "5分钟", "key": "v2"},
        {"icon": "🖼️", "title": "图片版权小知识", "duration": "4分钟", "key": "v3"},
    ]
    for v in video_items:
        with st.expander(f"{v['icon']} {v['title']}（{v['duration']}）", expanded=False):
            st.info(f"🎥 播放视频：{v['title']}")
            st.caption("（演示占位，实际项目会嵌入视频播放器）")

    st.markdown("---")

    # 2. 脚手架提示
    st.markdown("### 💡 学习脚手架")
    with st.expander("📝 写作思路提示", expanded=False):
        st.markdown("""
        介绍一道美食可以从这些方面写：

        1. **外观** - 看起来怎么样？颜色？形状？
        2. **味道** - 吃起来什么感觉？酸？甜？辣？
        3. **故事** - 这道菜有什么故事吗？
        4. **做法** - 怎么做？难不难？
        5. **感受** - 你为什么喜欢它？

        💡 选 2-3 个方面来写就很好啦！
        """)

    with st.expander("🎨 排版小技巧", expanded=False):
        st.markdown("""
        让你的网页更好看的小技巧：

        1. **多用小标题** - 大段文字没人爱看哦
        2. **适当空行** - 段落之间空一行更清爽
        3. **表情符号** - 适当加 emoji 更生动
        4. **列表表格** - 信息用列表更清晰
        5. **分隔线** - 用 --- 分隔不同部分

        ✨ 试试看，你的网页会大变样！
        """)

    with st.expander("❓ 遇到问题怎么办", expanded=False):
        st.markdown("""
        遇到问题别着急，试试这些方法：

        1. 📖 再看一遍微课视频
        2. 👥 问问同桌或小组同学
        3. 💬 在疑问广场提问题
        4. 👋 举手请老师帮忙

        💪 每个问题都是成长的机会！
        """)

    st.markdown("---")

    # 3. 快速自查清单（简化版）
    st.markdown("### ✅ 快速自查")
    quick_checks = [
        "标题醒目吗？",
        "图片清晰吗？",
        "标注来源了吗？",
        "文字通顺吗？",
        "排版整齐吗？",
    ]
    for i, check in enumerate(quick_checks):
        st.checkbox(check, key=f"quick_check_{i}")

    st.markdown("---")

    # 4. 参考样例
    st.markdown("### 🌟 参考样例")
    sample_items = [
        {"name": "优秀作品示例一", "emoji": "🥟", "author": "六年级 小红"},
        {"name": "优秀作品示例二", "emoji": "🍣", "author": "七年级 小明"},
        {"name": "优秀作品示例三", "emoji": "🍰", "author": "八年级 小华"},
    ]
    for i, sample in enumerate(sample_items):
        sample_html = f"""
        <div style="padding: 0.5rem; background: #f8f9fa; border-radius: 8px;
                    margin-bottom: 0.5rem; cursor: pointer;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.5rem;">{sample['emoji']}</span>
                <div>
                    <div style="font-size: 0.85rem; font-weight: 500;">{sample['name']}</div>
                    <div style="font-size: 0.75rem; opacity: 0.6;">{sample['author']}</div>
                </div>
            </div>
        </div>
        """
        st.markdown(sample_html, unsafe_allow_html=True)
        if st.button(f"查看样例{i+1}", key=f"view_sample_{i}", use_container_width=True):
            st.info(f"📖 正在打开「{sample['name']}」参考样例……")

    # 底部鼓励
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem; 
                background: linear-gradient(135deg, #E8F4FD, #FFF0E6);
                border-radius: 10px;">
        <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🌟</div>
        <div style="font-weight: 600; color: #2C3E50;">相信自己，你可以的！</div>
        <div style="font-size: 0.8rem; opacity: 0.7; margin-top: 0.25rem;">
            每一次尝试都是进步 💪
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 🎯 主函数：页面入口
# ============================================================
def main():
    """
    第一单元「用网页展示美食」主页面入口
    三栏布局：左(学习目标) - 中(主操作区) - 右(辅助栏)
    """
    # 初始化会话状态
    _init_session_state()

    # 页面标题
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem;
                background: linear-gradient(135deg, #E8F4FD, #FFF0E6);
                border-radius: 15px; margin-bottom: 1.5rem;">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🌐</div>
        <h2 style="margin: 0; color: #2C3E50;">第一单元：用网页展示美食</h2>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.7;">
            学习用 Markdown 制作美食网页，做一个小小的网页设计师！
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ===== 三栏布局 =====
    left_col, mid_col, right_col = st.columns([1, 2.5, 1])

    # ----- 左侧栏：OBE 学习目标 -----
    with left_col:
        render_left_obe_panel()

    # ----- 中间栏：主操作区（用 Tab 组织五大功能） -----
    with mid_col:
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "✏️ Markdown沙箱",
            "📤 提交作品",
            "✅ 合规自查",
            "🎯 任务包",
            "📊 互评量规"
        ])

        with tab1:
            render_md_sandbox()

        with tab2:
            render_submit_panel()

        with tab3:
            render_compliance_check()

        with tab4:
            render_task_packages()

        with tab5:
            render_peer_rubric()

    # ----- 右侧栏：辅助侧边栏 -----
    with right_col:
        render_right_sidebar()


# ============================================================
# 🚀 页面运行入口
# ============================================================
if __name__ == "__main__":
    # 设置页面配置（实际项目中通常在主入口文件设置）
    st.set_page_config(
        page_title="第一单元：用网页展示美食",
        page_icon="🌐",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # 注入全局样式（实际项目中从 components.style 导入）
    try:
        from components.style import inject_global_style
        inject_global_style()
    except Exception:
        pass  # 样式加载失败不影响功能

    # 运行主页面
    main()
