require("dotenv").config();
const Discord = require("discord.js");

const env = process.env;
const TOKEN = env.MANAGER_BOT_TOKEN;
const client = new Discord.Client();

const deleteTimeout = 2000;
const CHANNEL = env.AUTO_ROLE_CHANNEL_ID;

const emojiRoleMap = {
  "🇦": "JOIN_gym",
  "🇧": "RSS_AWS技術ブログ",
  "🇨": "RSS_AWS公式",
  "🇩": "RSS_GCP公式",
  "🇪": "RSS_etc",
  "🇫": "RSS_itnews",
};
//  "🇬": ""

const rolesmanagement_text = () => {
  //let strText = '\n対応した役職を付与します\n';
  let strText = "";
  const tmp = Object.entries(emojiRoleMap);
  for (const [key, value] of tmp) {
    strText += `${key} : #${value}\n`;
  }
  strText += `(※ 🗑️ : 自動で付与/剥奪できる役職全てを剥奪します )\n`;
  return strText;
};

const embedManegeMessage = {
  embed: {
    color: 16757683,
    title: "対応した役職を付与します",
    description: rolesmanagement_text(),
    fields: [
      {
        name: "[:regional_indicator_a: : JOIN_gym ]",
        value: "- #gym",
        inline: true,
      },
      {
        name: "[:regional_indicator_b: : RSS_AWS技術ブログ]",
        value: "- #rss-aws-classmethod \n - #rss-aws-serverworks \n - #rss-aws-iret",
        inline: true,
      },
      {
        name: "[:regional_indicator_c: :RSS_AWS公式]",
        value: "- #rss-aws-公式ブログ \n - #rss-aws-公式最新情報",
        inline: true,
      },
      {
        name: "[:regional_indicator_d: :RSS_GCP公式]",
        value: "- #rss-gcp-公式ブログ",
        inline: true,
      },
      {
        name: "[:regional_indicator_e: :RSS_etc]",
        value: "- #rss-最新文房具",
        inline: true,
      },
      {
        name: "[:regional_indicator_f: :RSS_itnews]",
        value: "- #rss-it-zdnet",
        inline: true,
      },
    ],
  },
};

const channelMessageAllDelete = async (channel) => {
  // 直近100件のbotメッセージ一括削除
  const messages = await channel.messages.fetch({ limit: 100 });
  //const filtered = messages.filter(message => message.author.bot);
  //message.channel.bulkDelete(filtered);
  messages.map((m) => {
    try {
      m.delete().then(console.log(m.content, ": メッセージを削除"));
    } catch (err) {
      console.error(err);
    }
  });
}

client.on("ready", () => {
  const channel = client.channels.cache.get(CHANNEL);
  console.log(`Logged in as ${client.user.tag}!`);
  channelMessageAllDelete(channel);
  channel.send(embedManegeMessage);
});

// リアクション起動コード
client.on("messageReactionRemove", async (reaction, user) => {
  const messageAuthorChannelId = reaction.message.channel.id;
  const channel = await user.client.channels.fetch(messageAuthorChannelId);
  if (channel != CHANNEL) return; // 「役職自動付与」チャンネル以外で実行不可
  if (!channel) return console.log("channel が取得できません！");
  const member = await channel.guild.members.fetch(user);
  if (!member) return console.log("member が取得できません！");

  // リアクションしたuserがBOTなら処理を終える
  if (user.bot) return;
  // 対応する役職がリアクションしたメンバーに付与されていなければ処理を終える
  // {未実装}
  if (reaction.emoji.name in emojiRoleMap) {
    const role = reaction.message.guild.roles.cache.find(
      (role) => role.name === emojiRoleMap[reaction.emoji.name]
    );
    const reply = await reaction.message.channel.send(
      `${user.username}から役職[ ${role.name} ]を剥奪しました`
    );
    member.roles.remove(role).then(reply.delete({ timeout: deleteTimeout }));
  }
});

client.on("messageReactionAdd", async (reaction, user) => {
  if (user.bot) return;
  const messageAuthorChannelId = reaction.message.channel.id;
  const channel = await user.client.channels.fetch(messageAuthorChannelId);
  if (channel != CHANNEL) return; // 「役職自動付与」チャンネル以外で実行不可
  if (!channel) return console.log("channel が取得できません！");
  const member = await channel.guild.members.fetch(user);
  if (!member) return console.log("member が取得できません！");
  console.log(
    ` ${user.tag} が${reaction.message.channel.name}の(${reaction.message})に ${reaction.emoji.name} をリアクションしました`
  );
  console.log("リアクション", reaction.emoji);
  // リアクション'🗑️'を行うことで[emojiRoleMap].valueの役職を全て剥奪
  if (reaction.emoji.name === "🗑️") {
    const reply = await reaction.message.channel.send(
      `${user.username}から役職を全て剥奪しました`
    );
    Object.values(emojiRoleMap).map((value) => {
      const role = reaction.message.guild.roles.cache.find(
        (role) => role.name === value
      );
      member.roles.remove(role);
    });
    reply.delete({ timeout: deleteTimeout });
    return;
  }
  // ボットのメッセージに絵文字リアクションしたかどうか判定
  // ->  してない場合 -> 処理を終える
  // ->  した場合は -> 本文に「対応した役職を付与します」があれば -> 役職を付与する処理を行う
  // const bot = await channel.guild.members.fetch(reacton.message.author.id);
  // if (!bot) return 'bot の絵文字にリアクションしていません！'
  if (reaction.emoji.name in emojiRoleMap) {
    const role = reaction.message.guild.roles.cache.find(
      (role) => role.name === emojiRoleMap[reaction.emoji.name]
    );
    const reply = await reaction.message.channel.send(
      `${user.username}に役職[ ${role.name} ]を付与しました`
    );
    member.roles.add(role).then(reply.delete({ timeout: deleteTimeout }));
  }
});

client.on("message", async (message) => {
  if (message.channel.id != CHANNEL) return; // 「役職自動付与」チャンネル以外で実行不可
  // ボットの場合は処理をしない
  console.log("---start---");
  if (message.author.bot) {
    if (message.embeds.length != 1) return;
    if (!message.embeds[0].title.includes("対応した役職を付与します")) return;
    console.log("---bot---");
    let tmp = Object.entries(emojiRoleMap);
    for (let [key, value] of tmp) {
      message.react(key);
    }
    return;
  }
  // 人のメッセージの中に特定の文字列(今回なら¥rolesmanagement)なら処理をする
  if (message.content === "¥rolesmanagement") {
    let channel = message.channel;
    let author = message.author.username;
    channelMessageAllDelete(channel);
    console.log("---command---");
    // メッセージへリアクション
    message.channel
      .send(embedManegeMessage)
      .then((message) => console.log(`Sent message: ${message}`))
      .catch(console.error);
    message.delete({ timeout: deleteTimeout });
    return;
  }
});

client.login(TOKEN);