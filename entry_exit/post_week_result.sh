#!/bin/sh
ps -ef |grep -v grep | grep -v 'vi ' |grep post_week_result.py
strStatus=$(echo $?)
today=$(date "+%Y/%m/%d/%H:%M:%S")

# initialize
BOT_BASE_DIR=$(pwd) # /home/ec2-user/discord
BOT_LOG_DIR=$(pwd)/logs/post_week_result # /var/log/discord/enterBot
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
    # source ${BOT_BASE_DIR}/entry_exit/.env
    source ${BOT_BASE_DIR}/entry_exit/env_vars/.env
    python3 ${BOT_BASE_DIR}/entry_exit/post_week_result.py & 1>> ${BOT_LOG_DIR}/success.log 2>> ${BOT_LOG_DIR}/error.log
    echo "${today} - bot not found. start or restart." >> ${BOT_LOG_DIR}/observer.log
elif [ ${strStatus} -ne 0 -o ${strStatus} -ne 1 ]; then
    echo "${today} - OK!" >> ${BOT_LOG_DIR}/observer.log
fi
while :; do
    sleep 1
done