#!/bin/sh
bash $(pwd)/entry_exit/enter_exit_bot.sh &
bash $(pwd)/entry_exit/post_week_result.sh &
while :; do
    sleep 1
done
