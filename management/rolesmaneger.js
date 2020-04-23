require('dotenv').config()

const Discord = require('discord.js');
const env = process.env;
const client = new Discord.Client();


const TOKEN = env.TEST_BOT_TOKEN;

client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
});

const rolesmanagement_text = () => {
    var strText = '対応した役職を付与します\n';
    strText += ':zero: AWSの役職\n';
    strText += ':one: ジム\n';
    strText += ':two:\n';
    return strText
}
//Bot自身の発言を無視する呪い
client.on('message', message =>{
    console.log('---start---');
    if(message.author.bot){
	console.log('---bot---');
    	message.react('0⃣');
    	message.react('1⃣');
    	message.react('2⃣');
        return;
    }
    message.react('💩');
	
    if(message.content === '!rolesmanagement'){
	console.log('---command---');
        let channel = message.channel;
	let author = message.author.username;
	let reply_text = rolesmanagement_text();
        // メッセージへリアクション
        message.reply(reply_text)
            .then(message => console.log(`Sent message: ${reply_text}`))
            .catch(console.error);
        return;
    }
});



client.login(TOKEN);
