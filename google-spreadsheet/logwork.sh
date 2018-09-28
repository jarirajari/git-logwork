#!/usr/bin/env bash
if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then
  echo "Please check usage."
  exit 0
fi
if [ -z "$GIT_LW_KEYFILE" ]; then
  echo "Google Spreadsheet key file (absolute path) is not set! export GIT_LW_KEYFILE"
  exit 0
fi
if [ -z "$GIT_LW_SSID" ]; then
  echo "Google Spreadsheet sheet ID is not set! export GIT_LW_SSID"
  exit 0
fi
if [ -z "$GIT_LW_SHEETNAME" ]; then
  echo "Google Spreadsheet sheet name is not set! export GIT_LW_SHEETNAME"
  exit 0
fi
if [ -z "$GIT_LW_A1RANGE" ]; then
  echo "Google Spreadsheet sheet range is not set! export GIT_LW_A1RANGE"
  exit 0
fi
LOGWORK=$0
WORK=$1
PROJECT=$2
if [ "$#" -eq 3 ] && [ -n "$3" ]; then
  DATE=$3
else
  DATE=`date +%Y-%m-%d`
fi
RESULT=$(python ./logwork.py $WORK $PROJECT $DATE $GIT_LW_KEYFILE $GIT_LW_SSID $GIT_LW_SHEETNAME $GIT_LW_A1RANGE  2>&1>/dev/null)
if [ "$RESULT" = "+" ]; then
  export GIT_LW_LAST="$WORK $PROJECT $DATE"
  echo "Logged work '$GIT_LW_LAST'"
else
  echo "Failed to log work: $RESULT"
fi

