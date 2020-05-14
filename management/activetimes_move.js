require('dotenv').config()

const Discord = require('discord.js');
const env = process.env;
const TOKEN = env.CRON_BOT_TOKEN
const client = new Discord.Client()


client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
});


// チャットがあったtimes_をACTIVE_TIMESに移動する
categoryMove = (channels, channelid) => {
    console.log('-----categoryMove-----');
    const categoryid = '709805664163332147'; // ACTIVE_TIMES
    console.log('editchanne_info: ', channels.cache.get(channelid).name ,' / ',channels.cache.get(channelid).rawPosition);
    channels.cache.get(channelid).setParent(categoryid)
    //.then(console.log)
    .catch(console.error);
}

// 
setPositionOnly = (channels, channelid , position) => {
    channels.cache.get(channelid).setPosition(position,true)
        .then(newChannel => console.log(`Channel's new position is ${newChannel.position}`))
        .catch(console.error);
};

// 全てのtimes_を[分報チャンネル]カテゴリーに移動する
// 戻す際にチャンネル名でソートした順番を引数に入れて、setPositionで変更する
categoryAllMove = (channels, channelid, position) => {
    console.log('-----categorlMove-----');
    const beforePosition = channels.cache.get(channelid).rawPosition
    const categoryid = '673004651871993866'; // 分報チャンネル
    // 現在のカテゴリーとの比較文必要か検討
    if(!channels.cache.get(channelid).parentID.includes(categoryid)) {
        channels.cache.get(channelid).edit({parentID: categoryid})
    }
    //positionの仕組みが謎なので一旦御形封印
    ////channels.cache.get(channelid).setPosition(position)
    //setPositionOnly(channels, channelid, position);

    console.log('reset前');
    console.log('editchanne_info: ', channels.cache.get(channelid).name ,' / ',beforePosition, ' --> ', channels.cache.get(channelid).rawPosition,' (設定値)',position,typeof(position));
}
getTimesChannelsid = (message) => {
    const ownerChannelid = '673006702924136448';
    const channelsid = message.guild.channels.cache.keyArray();
    const objChannelname_id = {};
    const listChannelname = [];
    const listChannelid = [];
    // timesのチャンネルをオブジェクトに入れる
    channelsid.map( id => {
        const channel = message.guild.channels.cache.get(id);
        if(channel.name.includes('times_')) {
            objChannelname_id[channel.name] = channel.id;
        }
    });
    // オブジェクトから名前だけの配列を作成
    for(name in objChannelname_id) {
        if(objChannelname_id.hasOwnProperty(name)) {
          listChannelname.push(name);
        }
    }
    // 名前をソートする
    listChannelname.sort()
    // ソートした順で、名前と紐づくIDを配列に入れる
    listChannelname.map( name => {
        listChannelid.push(objChannelname_id[name]);
    });
    // suのIDだけ先頭に移動
    let index = listChannelid.indexOf(ownerChannelid);
    if (index > -1) { // [times_supleiades]を配列の先頭移動する
        listChannelid.splice(index, 1);
        listChannelid.unshift(ownerChannelid)
    }
    //現在の順番を確認
    listChannelid.map(id => {
        console.log(message.guild.channels.cache.get(id).name,' : ', message.guild.channels.cache.get(id).rawPosition);
    });
    return listChannelid
}

client.on('message', message => {
    console.log(`${message.author.username}が${message.channel.name}でメッセージを送信しました。`);
    if(message.author.bot) return 
    const channels = message.guild.channels;
    if(message.channel.name.includes('times_')) {
        console.log('true!!!');
        categoryMove(channels, message.channel.id)
    }
    if(message.author.id != '603567991132782592') return
    if(message.content === '¥reset') {
        if(message.author.id != '603567991132782592') return
        const allTimesId = getTimesChannelsid(message);
        allTimesId.map(channelid => {
            let index = allTimesId.indexOf(channelid)
            categoryAllMove(channels, channelid, index);
        });
        console.log('===reset_end===')
    }
});
client.login(TOKEN);
