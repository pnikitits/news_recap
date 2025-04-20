#!/bin/bash

LOG="/tmp/cronlog.txt"
SCRIPT="/Users/pierrenikitits/Code/news_recap/run_main_script.sh"

crontab -l | grep -v news_recap > temp_cron || true


{
  echo "# news_recap jobs"
  echo "0 * * * * $SCRIPT >> $LOG 2>&1"
} >> temp_cron

crontab temp_cron
rm temp_cron

echo "✅ Cron jobs installed. Check with: crontab -l"