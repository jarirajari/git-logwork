#!/usr/bin/env bash
if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then
  echo "Please check usage."
  exit 0
fi
if [ -z "$GIT_LW_SERVER_URL" ]; then
  echo "No JIRA server URL! export GIT_LW_SERVER_URL with trailing slash"
  exit 0
fi
GIT_LW_USER_CREDS=$(cat ~/gitlw/.secret)
if [ -z "$GIT_LW_USER_CREDS" ]; then
  echo "Creating and securing secret directory and file..."
  rm -rf ~/gitlw/
  mkdir -p ~/gitlw/
  touch ~/gitlw/.secret
  read -p    "Enter JIRA username: "  username
  read -s -p "Enter JIRA password: "  password
  GIT_LW_USER_CREDS="$username:$password"
  echo $GIT_LW_USER_CREDS > ~/gitlw/.secret
  chmod 500 ~/gitlw/.secret
  chmod 500 ~/gitlw/
fi
JIRA_REST_API="/jira/rest/api/2/"
LOGWORK=$0
WORK=$1
PROJECT=$2
if [ "$#" -eq 3 ] && [ -n "$3" ]; then
  DATE=$3
else
  DATE=`date +%Y-%m-%d`
fi
RESULT=$(python ./logwork.py $WORK $PROJECT $DATE $GIT_LW_SERVER_URL$JIRA_REST_API $GIT_LW_USER_CREDS 2>&1>/dev/null)
if [ "$RESULT" = "+" ]; then
  export GIT_LW_LAST="$WORK $PROJECT $DATE"
  echo "Logged work '$GIT_LW_LAST'"
else
  echo "Failed to log work: $RESULT"
fi
