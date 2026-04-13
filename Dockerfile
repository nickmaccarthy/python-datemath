FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY pyproject.toml uv.lock README.md LICENSE ./
COPY datemath ./datemath
COPY tests ./tests
COPY verify.py ./

RUN pip install --upgrade pip \
    && pip install uv \
    && uv sync --group dev --frozen

RUN uv run pytest

CMD ["uv", "run", "python", "verify.py"]
