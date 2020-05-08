require('dotenv').config()
const Discord = require('discord.js');

const env = process.env;
const TOKEN = env.MANAGER_BOT_TOKEN;
const client = new Discord.Client();
const CHANNEL = env.JOIN_LEAVE_CHANNEL_ID;

client.on('ready', () => {
    console.log(`Logged in as ${client.user.tag}!`);
});

const sendMessage = (member, text) => {
    member.guild.channels.cache.get(CHANNEL).send(text)
}

client.on('guildMemberAdd', member => {
    console.log('参加時');
    let text = `${member.user.username} (id:${member.user.id}) が参加しました。`
    sendMessage(member, text);
});

client.on('guildMemberRemove', member => {
    console.log('退室時');
    let text = `${member.user.username} (id:${member.user.id}) が離脱しました。`
    sendMessage(member, text);
});

client.login(TOKEN);
