#!/bin/sh
ps -ef |grep -v grep |grep enter_exit_bot.py
strStatus=$(echo $?)
today=$(date "+%Y/%m/%d/%H:%M:%S")

# initialize
ENTER_BOT_BASE_DIR=$(pwd) # /home/ec2-user/discord
ENTER_BOT_LOG_DIR=$(pwd)/logs/enterBot # /var/log/discord/enterBot
if [ ! -e ${ENTER_BOT_LOG_DIR} ]; then
    mkdir -p ${ENTER_BOT_LOG_DIR}
fi
TIME_LOG_DIR=$(pwd)/timelog
if [ ! -e ${TIME_LOG_DIR} ]; then
    mkdir -p ${TIME_LOG_DIR}
fi

# validation
# if [ ! -f /dotfiles/.env ] then
#     echo "${ENTER_BOT_BASE_DIR}/entry_exit/env_vars/.env is not found."
#     echo "Could you create ./entry_exit/env_vars/.env?  You can see sample via ./entry_exit/env_vars/.env.default"
# fi

if [ ${strStatus} -eq 1 ]; then
    # source ${ENTER_BOT_BASE_DIR}/entry_exit/.env
    source /dotfiles/.env
    python3 ${ENTER_BOT_BASE_DIR}/entry_exit/enter_exit_bot.py & 1>> ${ENTER_BOT_LOG_DIR}/success.log 2>> ${ENTER_BOT_LOG_DIR}/error.log
    echo "${today} - bot not found. start or restart." >> ${ENTER_BOT_LOG_DIR}/observer.log
elif [ ${strStatus} -ne 0 -o ${strStatus} -ne 1 ]; then
    echo "${today} - OK!" >> ${ENTER_BOT_LOG_DIR}/observer.log
fi
