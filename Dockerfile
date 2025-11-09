FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.5.20 /uv /uvx /bin/

COPY pyproject.toml pyproject.toml

RUN uv pip install --system --no-cache-dir -r pyproject.toml

COPY ./src /app/src

WORKDIR /app

ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]