# 美食数字菜谱 · 信息科技智能助教

面向初中信息科技课程的 Streamlit 教学平台，覆盖「用网页展示美食」单元的项目式学习全流程：学习目标自查、Markdown 网页沙箱、作品提交与版本管理、智能助教问答、任务中心、疑问广场与成长档案。

## 功能模块

| 页面 | 说明 |
|---|---|
| 第一单元 | 三栏布局：OBE 学习目标清单 / Markdown 沙箱与作品提交 / 微课与合规自查 |
| 智能助教 | 学生端与教师端双知识库，关键词 + 模糊匹配问答 |
| 成长档案 | 学习数据卡片、四维素养雷达图、作品时间线、成就徽章 |
| 任务中心 | 学生端任务进度与教师端任务管理（提醒、完成率统计） |
| 疑问广场 | 学生提问与教师答疑管理 |
| 帮助说明 | 使用指南、常见问题、联系老师 |

支持学生 / 教师身份切换，以及深色模式、字体缩放、护眼模式三项显示设置。

## 本地运行

```bash
pip install -r requirements.txt
streamlit run ai_assistant.py
```

默认访问 http://localhost:8501

## 项目结构

```
ai_assistant.py         应用主入口（原版），内置登录页、侧边导航与页面分发
—                       （ai_assistant.py 内含：智能助教知识库 + 匹配引擎）
growth.py              成长档案与素养雷达图
tasks.py               任务中心
questions.py           疑问广场
help.py                帮助说明
unit1_webpage.py       第一单元页面
components/            UI 组件（样式注入、侧边栏、页头、卡片）
utils/storage.py       轻量 JSON 持久化层（作品、任务、疑问）
utils/obe_tracker.py   OBE 素养评分与学习档案汇总
data/db.json           运行时数据文件（首次写入自动生成）
```

## 数据存储说明

当前采用 `utils/storage.py` 的 JSON 文件存储，零外部依赖，适合演示与单机部署。

> **注意**：托管平台（如 Streamlit Community Cloud）的容器文件系统是临时的，应用重启后写入的数据会重置。若需长期保存学生作品，建议后续接入外部数据库（如 Supabase / PostgreSQL / 飞书多维表格），只需替换 `utils/storage.py` 中的读写实现，上层页面无需改动。

## 环境变量

| 变量 | 作用 | 默认值 |
|---|---|---|
| `APP_DATA_DIR` | 数据文件存放目录 | 项目根目录下的 `data/` |

## 部署

本项目为纯 Python 应用，可直接部署到 Streamlit Community Cloud、Hugging Face Spaces 或任意支持 Python 的容器平台。
