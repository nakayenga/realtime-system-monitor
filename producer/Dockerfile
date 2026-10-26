FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY producer/requirements.txt .

RUN pip install \
    --no-cache-dir \
    -r requirements.txt

COPY producer/ ./producer/

RUN useradd \
    --create-home \
    appuser

USER appuser

CMD ["python", "-m", "producer.app"]