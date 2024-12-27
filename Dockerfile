FROM python:3.13-slim

# 更新包管理器并安装 default-mysql-client
RUN apt-get update && apt-get install -y --no-install-recommends default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 安装poetry
RUN pip install poetry

# 复制项目依赖文件
COPY app pyproject.toml poetry.lock* ./

RUN sh

# 配置poetry不创建虚拟环境（在容器中没有必要）
RUN poetry config virtualenvs.create false

# 安装项目依赖
RUN poetry install

# 暴露端口
EXPOSE 8080

# 使用uvicorn启动应用
CMD ["sh", "-c", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]