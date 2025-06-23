FROM python:3.13-slim

COPY requirements.txt .

RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    uv pip install --system -r requirements.txt

COPY ./app /app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]
