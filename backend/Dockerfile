# Build Stage
FROM python:3.12-slim as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN pip install uv

WORKDIR /app
COPY pyproject.toml ./

RUN uv venv && uv pip install -r pyproject.toml

# Production Stage
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN groupadd -r eaios && useradd -r -g eaios eaios

COPY --from=builder /app/.venv /app/.venv
COPY . /app/

RUN chown -R eaios:eaios /app
USER eaios

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/api/v1/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
