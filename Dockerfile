# 使用官方 Python 轻量级镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8 \
    PIP_NO_CACHE_DIR=1 \
    CHROME_DRIVER_PATH=/usr/bin/chromedriver \
    CHROME_BINARY=/usr/bin/chromium

# ==========================================
# 安装系统依赖
# ==========================================
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    build-essential \
    gcc \
    g++ \
    wget \
    curl \
    fonts-dejavu \
    libglib2.0-0 \
    libnss3 \
    libfontconfig1 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgbm1 \
    libxshmfence1 \
    libfreetype6-dev \
    libjpeg-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# 先复制依赖文件
COPY requirements-base.txt .
COPY requirements-ml.txt .

# 升级基础构建工具
RUN pip install --upgrade pip setuptools wheel

# 先安装基础依赖
RUN pip install -r requirements-base.txt

# 先安装 hdbscan 需要的底层依赖
RUN pip install "Cython<3" "numpy==1.26.4"

# 单独安装高风险依赖 hdbscan
RUN pip install "hdbscan==0.8.33"

# 再安装其余 ML 依赖（不重复安装 hdbscan）
RUN grep -v '^hdbscan==' requirements-ml.txt > requirements_ml_no_hdbscan.txt && \
    pip install -r requirements_ml_no_hdbscan.txt

# 复制项目代码
COPY . .

# 创建运行目录
RUN mkdir -p /app/data/exports

# 暴露 Streamlit 默认端口
EXPOSE 8501

# 启动 Streamlit 应用
CMD ["streamlit", "run", "app17.py", "--server.address=0.0.0.0", "--server.port=8501"]
