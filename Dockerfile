FROM todify-base:0.1

WORKDIR /app

COPY app /app/app

# 使用uvicorn启动应用
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8080"]