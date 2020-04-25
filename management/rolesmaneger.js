require('dotenv').config()
const Discord = require('discord.js');

const env = process.env;
const TOKEN = env.TEST_BOT_TOKEN;
const client = new Discord.Client();

client.on('ready', () => {
    console.log(`Logged in as ${client.user.tag}!`);
});

const roleNames = {
    '🇦': 'AWS_RSS',
    '🇧': 'UR',
    '🇨': 'SR',
    '🇩': 'R',
    '🇫': 'UC',
    '🇬': 'C'
}

const rolesmanagement_text = () => {
    const strText = '\n対応した役職を付与します\n';
    const tmp = Object.entries(roleNames)
    for (const [ key, value ] of tmp) {
        //strText += `${key} : ${value}\n`
    }
    return strText
}

// リアクション起動コード
client.on('messageReactionAdd', async (reaction, user) => {
    if(user.bot) return console.log('bot だよ')
    console.log(`${reaction.message.guild} で ${user.tag} が ${reaction.emoji.name} をリアクションしました`)

    const channel = await user.client.channels.fetch('696268022930866180');
    const member = await channel.guild.members.fetch(user);

    try{
        if (reaction.emoji.name in roleNames) {
          const role = reaction.message.guild.roles.cache.find(role => role.name === roleNames[reaction.emoji.name]);
          member.roles.add(role)
        }
    } catch (e) {
        console.log(e)
    }
})

client.on('message', message => {
    // ボットの場合は処理をしない
    console.log('---start---');
    if(message.author.bot) {
        console.log('---bot---');
        //message.react('0️⃣');
        let tmp = Object.entries(roleNames)
        for (let [ key, value ] of tmp) {
            message.react(key);
        }
        return;
    }
    message.react('💩');

    // 人のメッセージの中に特定の文字列(今回なら!rolesmanagement)なら処理をする
    if(message.content === '!rolesmanagement') {
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
