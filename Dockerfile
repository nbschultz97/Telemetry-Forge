FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE /app/
COPY src /app/src

RUN pip install --no-cache-dir .

ENV BOT_DATA_DIR=/var/lib/ceradon-sam-bot

CMD ["ceradon-sam-bot", "run", "--config", "config/config.yaml", "--once"]
