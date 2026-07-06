#!/bin/sh
# dump env for cron
printenv | grep -v "^_" > /etc/environment

# run once immediately on startup
/usr/local/bin/python /app/cctv-fetcher.py

# hand off to cron
cron -f
