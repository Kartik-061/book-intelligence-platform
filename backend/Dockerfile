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
RUN python manage.py migrate --noinput || true
RUN python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='bookiqadmin').exists() or User.objects.create_superuser('bookiqadmin', 'krishkarthikyamotwani@gmail.com', 'BookIQ@2026')" || true
EXPOSE 8080
CMD python manage.py migrate --noinput && gunicorn backend.wsgi --bind 0.0.0.0:$PORT --log-file -
