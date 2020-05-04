require('dotenv').config()
const Discord = require('discord.js');
const sqlite = require('sqlite3').verbose();

const env = process.env;
const TOKEN = env.CRON_BOT_TOKEN;
const client = new Discord.Client();
const db = new sqlite.Database('/home/ec2-user/sqlite3/mokumoku_online_studyroom.sqlite3');

// ログイン
client.on('ready', () => {
    console.log(`Logged in as ${client.user.tag}!`);
});

// 全て取得
const select_all = () => {
    db.each('SELECT * FROM mem_time;', (error, row) => {
        if(error) {
            console.error('Error!', error);
            return;
        }
        console.log('row',row);
    });
}
// データゼロ想定の書き込み
const insert_member = (userid, username, guild_join_datetime) => {
    db.each("SELECT * FROM mem_time WHERE userid = ? and username = ?",[userid,username],(error, row) => {
        if(error){
            console.log('Error!:', error);
            return;
        }
    }, (error, count) => {  //←complete処理追加
        //SQL実行直後に上のコールバック処理が走る前にここが処理されるで。
        if (error){
            //エラー処理
            console.log('Error!:', error);
        }else{
            if (count == 0){
                //ここでSQLの実行結果が0件の処理や
                db.run("INSERT INTO mem_time(userid, username, guild_join_datetime) VALUES(?,?,?);",[userid, username, guild_join_datetime])
                console.log(`${userid}(${username})を新規追加(INSERT)しました`);
            }else{
                console.log(`既にDBに${userid}(${username})が存在します`);
            }
        }
    });
} 

//insert_member(603567991132782600,'SuPleiades');

// 送信されたメッセージをトリガーに処理開始
client.on('message', message => {
    let channel = message.channel;
    let author = message.author.username;
//    if(message.content === '!all_insert_jointime') {
    console.log('---command---');
    const members = message.guild.members.cache.keyArray();
    members.forEach(function(value) {
        const name = message.guild.members.cache.get(value);
        console.log('------------------------')
        console.log('name.user.id: ',name.id);
        console.log('name.user.username: ',name.user.username);
        console.log('name.joinedTimestamp: ',name.joinedTimestamp);

//        db.serialize(() => {
//            insert_member(name.id, name.user.username, name.joinedTimestamp);
//            db.finalize();
//        });
    db.close();
//    var date = new Date(name.joinedTimestamp)
//    // メッセージへリアクション
//    message.reply(reply_text)
//        .then(message => console.log(`Sent message: ${reply_text}`))
//        .catch(console.error);
//    message.delete({ timeout: 1000 })
//    return;
    });
});

client.login(TOKEN);
