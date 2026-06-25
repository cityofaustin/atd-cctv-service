FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY cctv-fetcher.py .

RUN useradd --create-home appuser \
    && mkdir -p /data \
    && chown appuser:appuser /data

    USER appuser

CMD ["python", "cctv-fetcher.py"]
