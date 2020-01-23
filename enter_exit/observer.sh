#!/bin/sh
ps -ef |grep -v grep |grep enter_exit_bot.py >> /var/log/discord/enterBot/observer.log

strStatus=$(echo $?)
today=$(date "+%Y/%m/%d/%H:%M:%S")
if [ ${strStatus} -eq 1 ]; then
    source /home/ec2-user/discords/enter_exit/.env
    /usr/bin/python3 /home/ec2-user/discords/enter_exit/enter_exit_bot.py & >> /var/log/discord/enterBot/success.log 2>> /var/log/discord/enterBot/error.log
    echo "${today} - bot not found. restart." >> /var/log/discord/enterBot/observer.log
elif [ ${strStatus} -ne 0 -o ${strStatus} -ne 1 ]; then
    echo "${today} - OK!" >> /var/log/discord/enterBot/observer.log
fi
