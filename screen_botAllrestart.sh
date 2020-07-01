 #!/bin/bash
 # entry_exit
 screen -S enter_exit -X quit
 screen -dmS enter_exit
 sleep 3s
 screen -S enter_exit -X stuff 'cd ~/discord/entry_exit/;source .env;python3 enter_exit_bot.py'`echo -ne '\015'`
 
 # musicbot2
 screen -S musicbot -X quit
 screen -dmS musicbot
 sleep 3s
 screen -S musicbot -X stuff 'cd ~/MusicBot; python3 run.py'`echo -ne '\015'`
 
 # musicbot2
 screen -S musicbot2 -X quit
 screen -dmS musicbot2
 sleep 3s
 screen -S musicbot2 -X stuff 'cd ~/repos/musicbot2/MusicBot/;python3 run.py'`echo -ne '\015'`
 
 # auto_reaction2
 screen -S auto_reaction2 -X quit
 screen -dmS auto_reaction2
 sleep 3s
 screen -S auto_reaction2 -X stuff 'cd ~/discord/entry_exit/;source .env;python3 auto_reaction2.py'`echo -ne '\015'`
 
 # rolesmaneger
 screen -S rolesmaneger -X quit
 screen -dmS rolesmaneger
 sleep 3s
 screen -S rolesmaneger -X stuff 'cd ~/discord/management;node rolesmaneger.js'`echo -ne '\015'`
 
 # post_week_result
 screen -S post_week_result -X quit
 screen -dmS post_week_result
 sleep 3s
 screen -S post_week_result -X stuff 'cd ~/discord/entry_exit/;python3 post_week_result.py'`echo -ne '\015'`
 
 # post_month_result
 screen -S post_month_result -X quit
 screen -dmS post_month_result
 sleep 3s
 screen -S post_month_result -X stuff 'cd ~/discord/entry_exit/;python3 post_month_result.py'`echo -ne '\015'`

 # activetimes_move
 screen -S activetimes_move -X quit
 screen -dmS activetimes_move
 sleep 3s
 screen -S activetimes_move -X stuff 'cd ~/discord/management;python3 activetimes_move.js'`echo -ne '\015'`

 # autoCreateTimes
 screen -S autoCreateTimes -X quit
 screen -dmS autoCreateTimes
 sleep 3s
 screen -S autoCreateTimes -X stuff 'cd ~/discord/management;python3 autoCreateTimes.js'`echo -ne '\015'`
 
 # sqlite_mem_time
 screen -S sqlite_mem_time -X quit
 screen -dmS sqlite_mem_time
 sleep 3s
 screen -S sqlite_mem_time -X stuff 'cd ~/discord/management;python3 sqlite_mem_time.js'`echo -ne '\015'`
