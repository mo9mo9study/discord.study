#!/bin/sh
ps -ef |grep -v grep | grep -v 'vi ' |grep study_target.py
strStatus=$(echo $?)
today=$(date "+%Y/%m/%d/%H:%M:%S")

# initialize
BOT_BASE_DIR=$(pwd) # /home/ec2-user/discord
BOT_LOG_DIR=$(pwd)/logs/study_target # /var/log/discord/enterBot
if [ ! -e ${BOT_LOG_DIR} ]; then
    mkdir -p ${BOT_LOG_DIR}
fi
TIME_LOG_DIR=$(pwd)/entry_exit/timelog
if [ ! -e ${TIME_LOG_DIR} ]; then
    mkdir -p ${TIME_LOG_DIR}
fi
USER_SETTINGS_DIR=$(pwd)/entry_exit/userSettings
if [ ! -e ${USER_SETTINGS_DIR} ]; then
    mkdir -p ${USER_SETTINGS_DIR}
fi

# validation
# if [ ! -f /dotfiles/.env ] then
#     echo "${BOT_BASE_DIR}/entry_exit/env_vars/.env is not found."
#     echo "Could you create ./entry_exit/env_vars/.env?  You can see sample via ./entry_exit/env_vars/.env.default"
# fi

if [ ${strStatus} -eq 1 ]; then
    python3 ${BOT_BASE_DIR}/entry_exit/study_target.py & 1>> ${BOT_LOG_DIR}/success.log 2>> ${BOT_LOG_DIR}/error.log
    echo "${today} - bot process is not found. start or restart." >> ${BOT_LOG_DIR}/observer.log
elif [ ${strStatus} -ne 0 -o ${strStatus} -ne 1 ]; then
    echo "${today} - OK!" >> ${BOT_LOG_DIR}/observer.log
fi
while :; do
    sleep 1
done