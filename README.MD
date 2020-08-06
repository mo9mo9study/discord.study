## first step
```
pip install -r requirements.txt
```


## sqlite3 databaseschema
```
CREATE TABLE mem_time(
    userid INT NOT NULL PRIMARY KEY,
    username TEXT NOT NULL,
    modifeid_datetime TEXT NOT NULL DEFAULT (DATETIME('now','localtime')),
    guild_join_datetime TEXT,
    voicechannel_lastjoin_datetime TEXT,
    voicechannel_lastleave_datetime TEXT,
    message_lastsent_datetime TEXT
);
```
### trriger
```
CREATE TRIGGER mem_time_trigger AFTER UPDATE ON mem_time
BEGIN
    UPDATE mem_time SET modifeid_datetime = datetime('now', 'localtime') WHERE userid = OLD.userid ;
END;
```


## Docker上でenterBotを動かす

- 試した環境
```
macOS 10.15.x
docker 2.3.0.3
```

- 現状対応しているのは
enterBot(enter_exit)のみ
botの起動


- Clone
```
git clone git@github.com:mo9mo9study/discord.study.git
cd discord.study
```

- .envにDiscordへの接続情報を書き込む

```
cp -i $(pwd)/entry_exit/env_vars/{.env.default,.env}
```
$(pwd)/entry_exit/env_vars/.env にテスト用DiscordサーバのTokenなどを記入する。
DiscordサーバやTokenの用意方法などはいつかまとめるかもしれないし、まとめないかもしれない。わからなければもくもくOnline勉強会で聞いてください。


- Docker imageをbuildしてenterBotを起動
```
docker build . -t discord.study
docker run -v $(pwd)/entry_exit/env_vars:/dotfiles -itd discord.study
docker ps # discord.studyが上がっていればok
```

- 起動したDocker imageのbashでログインしてbotのログを見る
```
docker exec -it $(docker ps -lq) bash  
or
docker exec -it $(docker ps|grep discord.study|awk -F' ' '{print $1}') bash  
```
この状態でDiscordサーバの音声チャネルに入退室すると、それを検知したenterBotがログを標準出力に出力します。

