require("dotenv").config();

const Discord = require("discord.js");
const env = process.env;
const TOKEN = env.CRON_BOT_TOKEN;
const client = new Discord.Client();
const cron = require("node-cron");

client.on("ready", () => {
  console.log(`Logged in as ${client.user.tag}!`);
});

// チャットがあったtimes_をACTIVE_TIMESに移動する
categoryMove = (channels, channelid) => {
  const categoryid = "709805664163332147"; // ACTIVE_TIMES
  console.log(
    "editchanne_info: ",
    channels.cache.get(channelid).name,
    " / ",
    channels.cache.get(channelid).rawPosition
  );
  channels.cache
    .get(channelid)
    .setParent(categoryid)
    //.then(console.log)
    .catch(console.error);
};

//// TODO:全てのtimes_を[分報チャンネル]カテゴリーに移動する
//// 戻す際にチャンネル名でソートした順番を引数に入れて、setPositionで変更する
//categoryAllMove = (channels, channelid, position) => {
//    const channel = channels.cache.get(channelid);
//    const beforePosition = channel.rawPosition
//    const categoryid = '673004651871993866'; // 分報チャンネル
//    // 現在のカテゴリーとの比較文必要か検討
//    if(!channel.parentID.includes(categoryid)) channel.edit({parentID: categoryid});
//    console.log('editchanne_info: ', channel.name ,' / ',beforePosition, ' --> ', channel.rawPosition,' (設定値)',position,typeof(position));
//}

categorySelectMove = (channels, channelid, categoryid) => {
  const channel = channels.cache.get(channelid);
  if (!channel.parentID.includes(categoryid))
    channel.edit({ parentID: categoryid });
  console.log("editchanne_info: ", channel.name, " --> ", channel.parentID);
};

getTimesChannelsid = (guild) => {
  const ownerChannelid = "673006702924136448";
  const channelsid = guild.channels.cache.keyArray();
  const objChannelid = { AlphaNum: [], Etc: [] };
  //const listChannelname = [];
  //const listChannelid = [];
  // timesのチャンネルをオブジェクトに入れる
  channelsid.map((id) => {
    const channel = guild.channels.cache.get(id);
    if (channel.name.includes("times_")) {
      if (channel.name.match(/^times_[a-zA-Z0-9].*$/)) {
        // 英数字のカテゴリー用配列
        //console.log(`${channel.name}は[英数字]のカテゴリーに追加されました`);
        objChannelid.AlphaNum.push(channel.id);
      } else {
        // その他カテゴリー用配列
        //console.log(`${channel.name}は[その他]のカテゴリーに追加されました`);
        objChannelid.Etc.push(channel.id);
      }
      //objChannelname_id[channel.name] = channel.id;
    }
  });
  //// TODO:sortしようしうとした時の軌跡（オブジェクトから名前だけの配列を作成）
  //for(name in objChannelname_id) {
  //    if(objChannelname_id.hasOwnProperty(name)) {
  //      listChannelname.push(name);
  //    }
  //}
  //listChannelname.sort()
  //// ソートした順で、名前と紐づくIDを配列に入れる
  //listChannelname.map( name => {
  //    listChannelid.push(objChannelname_id[name]);
  //});
  //let index = listChannelid.indexOf(ownerChannelid);
  //if (index > -1) { // [times_supleiades]を配列の先頭移動する
  //    listChannelid.splice(index, 1);
  //    listChannelid.unshift(ownerChannelid)
  //}
  //return listChannelid
  return objChannelid; // obj = {"AlphaNum":[ ], "Etc": [ ]}
};

client.on("message", (message) => {
  console.log(
    `${message.author.username}が${message.channel.name}でメッセージを送信しました。`
  );
  if (message.author.bot) return;
  const channels = message.guild.channels;
  if (message.channel.name.includes("times_")) {
    categoryMove(channels, message.channel.id);
  }
  if (message.author.id != message.channel.guild.ownerID) return;
  if (message.content === "¥reset") {
    const allTimesId = getTimesChannelsid(message.guild);
    console.log(allTimesId);
    // カテゴリー「分報チャンネル（英数字）」に移動
    allTimesId.AlphaNum.map((channelid) => {
      const channelname = channels.cache.get(channelid);
      console.log(`${channelid} : ${channelname}`);
      categorySelectMove(channels, channelid, "673004651871993866");
    });
    // カテゴリー「分報チャンネル（その他）」に移動
    allTimesId.Etc.map((channelid) => {
      const channelname = channels.cache.get(channelid);
      console.log(`${channelid} : ${channelname}`);
      categorySelectMove(channels, channelid, "719095356218146879");
    });
    //TODO: allTimesId.map(channelid => {
    //    let index = allTimesId.indexOf(channelid)
    //    console.log('channelid : ', channelid)
    //    //categoryAllMove(channels, channelid, index);
    //});
  }
});

cron.schedule("0 0 2 * * *", () => {
  const date = new Date();
  console.log(
    `${date.toLocaleString("ja")}にreset処理の定期実行を開始しました`
  );
  const guild = client.guilds.cache.get("603582455756095488");
  guild.channels.cache
    .get("673006702924136448")
    .send(`${date.toLocaleString("ja")}に定期実行を行いました`, {
      reply: guild.ownerID,
    });
  const allTimesId = getTimesChannelsid(guild);
  console.log(allTimesId);
  // カテゴリー「分報チャンネル（英数字）」に移動
  allTimesId.AlphaNum.map((channelid) => {
    categorySelectMove(guild.channels, channelid, "673004651871993866");
  });
  // カテゴリー「分報チャンネル（その他）」に移動
  allTimesId.Etc.map((channelid) => {
    categorySelectMove(guild.channels, channelid, "719095356218146879");
  });
});

client.login(TOKEN);
