require("dotenv").config();

const Discord = require("discord.js");
const env = process.env;
const TOKEN = env.MANAGER_BOT_TOKEN;
const client = new Discord.Client();
const SERVER = env.DISCORD_SEVER_ID;

client.on("ready", () => {
  console.log(`Logged in as ${client.user.tag}!`);
});

client.on("voiceStateUpdate", (before, after) => {
  const userid = after.id;
  const member = after.guild.members.cache.get(userid);
  const roleid = "710333297598922752";
  console.log("before: ", before.channelID, "(after) ", after.channelID);
  if (after.guild.id === SERVER && before.channelID != after.channelID) {
    console.log("viceStateUpdate");
    if (before.channelID == null) {
      console.log(
        `${member.user.username}(${userid})がボイスチャンネルに参加しました`
      );
      member.roles.add(roleid);
    }
    if (after.channelID == null) {
      console.log(
        `${member.user.username}(${userid})がボイスチャンネル から退室しました`
      );
      // ロール付与されているかの確認をいれてエラーをなくす
      member.roles.remove(roleid);
    }
  }
});

client.login(TOKEN);
