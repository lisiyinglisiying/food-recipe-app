# 美食数字菜谱 · 信息科技智能助教
# Streamlit 应用容器镜像
FROM python:3.11-slim

# 时区设为东八区，保证 datetime.now() 与国内时间一致
ENV TZ=Asia/Shanghai \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app

# 先用国内镜像源装依赖，构建更快
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    -i https://mirrors.cloud.tencent.com/pypi/simple \
    --trusted-host mirrors.cloud.tencent.com

COPY . .

# 数据目录（容器内临时可写；如需持久化请挂载 CFS 或改用云数据库）
RUN mkdir -p /app/data

EXPOSE 8501

# 云托管会注入 PORT 环境变量，未注入时回退到 8501
CMD ["sh", "-c", "streamlit run ai_assistant.py --server.port=${PORT:-8501} --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false --server.enableXsrfProtection=true --browser.gatherUsageStats=false"]
