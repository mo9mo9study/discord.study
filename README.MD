## quickstart
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
