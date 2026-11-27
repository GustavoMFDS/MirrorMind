FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN python -m pip install --no-cache-dir . && \
    groupadd --gid 10001 mirrormind && \
    useradd --uid 10001 --gid 10001 --no-create-home mirrormind
USER 10001:10001
EXPOSE 8000
CMD ["uvicorn", "mirrormind.api:app", "--host", "0.0.0.0", "--port", "8000"]
