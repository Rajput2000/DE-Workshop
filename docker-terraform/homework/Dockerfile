FROM python:3.9-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /code
ENV PATH="/code/.venv/bin:$PATH"

COPY pyproject.toml .python-version uv.lock ./
ENV UV_HTTP_TIMEOUT=300
RUN uv sync --locked

COPY homework_ingestion.py .

ENTRYPOINT ["python", "homework_ingestion.py"]