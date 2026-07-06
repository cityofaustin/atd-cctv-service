FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY cctv-fetcher.py .

# install cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# add crontab - run every 12 hours
RUN echo "0 */12 * * * /usr/local/bin/python /app/cctv-fetcher.py >> /proc/1/fd/1 2>&1" | crontab -

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
CMD ["sh", "./entrypoint.sh"]

