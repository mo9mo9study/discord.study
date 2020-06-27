require("dotenv").config();

const Discord = require("discord.js");
const env = process.env;
const TOKEN = env.MANAGER_BOT_TOKEN;
const client = new Discord.Client();
const CHANNELID = env.SELF_INTRODUCTION_CHANEL_ID;
const categoryid = env.ACTIVE_TIMES_CATEGORY_ID;

const sendMessage =
  "このチャンネルはあなたの分報(個人)チャンネルです。\n使い方は「参考資料」又は「他メンバーの分報チャンネル」をご覧ください。\n上手に活用してみてくださいね\n 　参考資料：http://c16e.com/1511101558/";

const allChannelNameList = (values) => {
  const list = [];
  values.map((value) => {
    if (!value.type.includes("text")) return;
    if (value.name.includes("times_")) {
      list.push(value.name);
    }
  });
  return list;
};

client.on("ready", () => {
  console.log(`Logged in as ${client.user.tag}!`);
});

client.on("message", (message) => {
  if (message.channel.id != CHANNELID) return;
  const channels = allChannelNameList(message.channel.guild.channels.cache);
  const channelName = ("times_" + message.author.username).toLowerCase();
  console.log(`timesチャンネルは${channels.length}個存在します`);
  if (message.content.includes("呼び名")) {
    if (channels.includes(channelName)) {
      console.log("既にチャンネル名が存在します");
    } else {
      if (channels.length > 50) {
        let alertMessage = `timesチャンネルが50個(現在：${channels.length}個)を超えました`;
        // 管理者の文法チャンネルにメンション付きで連絡する機能
        const member = message.channel.guild.members.cache.get(
          message.channel.guild.ownerID
        );
        // おいおいは、チャンネルのトピックにownerIDが含まれているチャンネルを選択するやり方にする
        const channel = message.channel.guild.channels.cache.get(
          "673006702924136448"
        );
        channel
          .send(alertMessage, { reply: member })
          .then(
            console.log(
              `${channel.name}に「分報チャンネル」の総数が50個を超えた旨を連絡しました`
            )
          )
          .catch(console.error);
      }
      message.channel.guild.channels.create(channelName, {
        type: "text",
        parent: categoryid,
        topic: message.author.id,
      });
      console.log(`${channelName}を作成しました`);
    }
  }
});

client.on("channelCreate", (channel) => {
  console.log(`---> 新しく[ ${channel.name} ]チャンネルが作成されました`);
  const channelUserid = channel.topic;
  const member = channel.guild.members.cache.get(channelUserid);
  console.log(member);
  if (member == undefined) return;
  if (channel.name.includes("times_")) {
    channel
      .send(sendMessage, { reply: member })
      .then(
        console.log(
          `${channel.name}で${member.user.username}に「分報チャンネル」案内のメッセージを送りました`
        )
      )
      .catch(console.error);
  }
});

client.login(TOKEN);
