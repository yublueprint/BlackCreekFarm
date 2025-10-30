FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV DJANGO_SETTINGS_MODULE=config.settings
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]