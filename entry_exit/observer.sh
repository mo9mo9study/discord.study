#!/bin/sh
<<<<<<< HEAD
bash $(pwd)/entry_exit/enter_exit_bot.sh
#bash post_week_result.sh
=======
bash $(pwd)/entry_exit/enter_exit_bot.sh &
bash $(pwd)/entry_exit/post_week_result.sh &
>>>>>>> update observe.sh
while :; do
    sleep 1
done
