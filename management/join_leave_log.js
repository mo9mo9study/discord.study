require("dotenv").config();
const Discord = require("discord.js");

const env = process.env;
const TOKEN = env.MANAGER_BOT_TOKEN;
const client = new Discord.Client();
const CHANNEL = env.JOIN_LEAVE_CHANNEL_ID;

const allInvites = {}

client.on("ready", async () => {
  console.log(`Logged in as ${client.user.tag}!`);
  client.guilds.cache.forEach(guild => {
    guild.fetchInvites().then(invites => {
      allInvites[guild.id] = invites
    })
  })
});

const sendMessage = (member, text) => {
  member.guild.channels.cache.get(CHANNEL).send(text);
};

client.on('inviteCreate', (invite) => {
  client.guilds.cache.forEach(guild => {
    guild.fetchInvites().then(invites => {
      allInvites[guild.id] = invites
    })
  })
});

client.on("guildMemberAdd", (member) => {
  console.log("参加時");
  member.guild.fetchInvites().then(invites => {
    const oldInvites = allInvites[member.guild.id]
    allInvites[member.guild.id] = invites
    // 以前に取得した招待コードと新たに取得したので、使用回数が増えたものを探す
    const invite = invites.find(i => oldInvites.get(i.code).uses < i.uses)
    console.log(`${member.user.tag} は ${invite.code} を使ってサーバーに参加しました`)
    console.log(invite)
    let text = `${member.user.username} (__id:${member.user.id}__) が参加しました。【 招待者：<@${invite.inviter.id}> 】`;
    sendMessage(member, text);
  });
});

client.on("guildMemberRemove", (member) => {
  console.log("退室時");
  let text = `${member.user.username} (__id:${member.user.id}__) が離脱しました。`;
  sendMessage(member, text);
});

client.login(TOKEN);
