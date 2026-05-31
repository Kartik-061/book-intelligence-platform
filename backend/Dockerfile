# Stage 1: Builder
FROM python:3.13-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.13-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

RUN python manage.py collectstatic --noinput || true

EXPOSE 8080

CMD ["gunicorn", "backend.wsgi", "--bind", "0.0.0.0:8080", "--log-file", "-"]