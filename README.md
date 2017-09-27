# syrup-sopel-modules
Modules for syrup.  Mostly updates of the ones in the phenny repo  
Used to be called syrup-willie-modules  
Python 3.3

### Modules descriptions:  
##### anime.py
Checks releases of animes on specified day. Based off https://github.com/infinitylabs/uguubot/blob/master/plugins/anime.py
##### animerss.py
Outputs RSS news from animenewsnetwork, I think the latest commit broke it, so use the one before it.
##### bday.py
Notifies channel when a user has their birthday (every 6 hours on the day of the birthday), or how many days away the next birthday is. refer to data.txt to see how the user's birthdays are suppose to be set up.
##### bitcoin.py
Bitcoin/ETH/XRP module. You can add more memecoins in too. Based off of https://github.com/sc0tt/boredbot-modules/blob/master/bitcoin.py
##### dubtrack.py
Dubtrack (and plugdj) module.  Dubtrack has a really nice API.  plugdj does not, but whatever.
##### edict.py
Translate japanese terms using wwwjdic|edict api, accepts both kanji and romaji inputs.  
##### fact.py
Fact Seagull gives a 100% true fact.  Based off a flash.
##### gdq.py
Module for GamesDoneQuick.  Counts down to next GDQ when none are happening.  When there is a GDQ, gives some information about current game, runner, etc.
##### gelbooru.py
Gelbooru module.  search for lewd or safe images of 'You're Waifu'.  also gives some image info if a gelbooru link shows up.
##### heh.py
Not sure what I even use from here, maybe the reddit shit.  Taken from sc0tt.
##### hltb.py
'How long to beat' module.  Outputs how long it would take to beat a video game.  
##### hots.py
Guest module by afengg, some heroes of the storm module that does...something... give best skills by popularity? IDK, I only play good games.
##### mal.py
Anime module to check myanimelist for show info, can also check for manga, VAs, characters, etc.  gives stats on animu if a mal url is posted.  Requires whitelisted MAL api user-agent key, and base 64 encoded username:password 
##### mtg.py
Magic the Gathering module.  Get info on a specific card.
##### nicovideourl.py
Outputs information on nicovideo urls when they're posted to the channel.
##### pb.py
Pushbullet module.  At work and someone posted a link to something interesting, but can't/shouldn't view it?  Push it to your phone instead to safely view it.  Requires pushbullet API key.
##### pixiv.py
Pixiv module to search pixiv (jp and en) images.  Warning, this has a higher memory/cpu usage compared to other modules.
##### ratewaifu.py
A waifu rating module that provides absolutely no value. Don't forget, you're waifu a shit tho.
##### remind.py
A modified remind.py (from sopel's own plugins).  defaults to minutes when entering a number, does not require a message.  Adds a 'LP' unit of time, which is 6 minutes, for love live school idol festival players. 
##### search2.py
A modified search.py (from sopel's own plugins). Mostly changed the UK->US and removed ads from showing up in results.
##### shadowverse.py
Get info about cards from some random waifu card fighting game. created by @agricola 
##### smug.py
Outputs a random smug anime image out of 71 choices.
##### sotd.py
Song of the Day module.  Allows users to submit a song of the day to be recorded on a database.  Supports youtube, soundcloud, bandcamp songs.  Requires lots of setup and different api keys.
##### soundcloudurl.py
Outputs information on soundcloud urls when they're posted to the channel.  Requires a soundcloud clientID
##### stocks.py
Outputs the dow jones index average, or search your own favourite stocks!  Info comes from finance.google.com, and has a 15 minute stocks delay.
##### sync.py
Sync module to start a countdown to sync chinese cartoons with your irc friends.  Written by https://github.com/agricola
##### traffic.py
Traffic/duration to location module that works off the .setlocation set for user.  it's not really well done.  requires google api (distance matrix) 
##### trivia.py
Trivia module, by @sc0tt 
##### twitch.py
Module for getting info on a twitch/smashcast/mixer channel assuming they are currently streaming, as well as setting up a notification announcement for set twitch/smashcast users when they start streaming. Gives info on twitch users when a twitch url is posted.  Requires hitbox, twitch, youtube API keys.  By default it checks every ten seconds for streaming status of specified users, this adds up!  25920 url calls or more a day.  Twitch API is slow, don't expect instant announcements (sometimes 1m lag time on api), hitbox is p. good and quick.  There are slight issues with it, may randomly not work, and it requires probably a complete rewrite (now in progress). :|  Now requires Client-ID from twitch: https://www.twitch.tv/settings/connections
##### urbandict.py
Outputs urban dictionary definitions for input words.  I'm not 100% sure where this came from, probably a modified version of this: https://github.com/mutantmonkey/phenny/blob/master/modules/urbandict.py
##### url2.py
A modified url.py (from sopel's own plugins).  Add BeautifulSoup support, which should give improved results for url titles, fallsback to regex (old way) if any issues. Requires bs4 module. 
##### vndb.py
Gets information about a visual novel.  Requires tags.json to be downloaded from vndb.  You should probably rename the client name/version as well.  Based on https://github.com/theappleman/pyvndb 
##### wait.py
What anime is this module.  input takes a direct image link and checks whatanime.ga to find out ...what anime it is.  Requires Pillow python image library
##### wafflebot.py
Markov chain bot created by sc0tt, additional functionality added by me.  Keeps track of all lines said in a channel (greater than 5 words).  You can make it output a line based on all lines side, or output a line based on content that a specific user has said.  After 1000 lines are said in a channel the bot will automatically say a line.  Will try and avoid highlighting users if they are currently in the channel.  Requires redis.  Redis setup process is completely unknown...ask sc0tt?!
##### weather2.py
Modified version of weather.py from sopel's modules.  uses forcast.io to get weather.  Adds weather alerts and a 7 day weather forecast.  Requires forecast.io and google url shortner API keys.
##### youtoob.py
Modified youtube.py from https://gist.github.com/calzoneman/b5ee12cf69863bd3fcc3.  Requires youtube API Key. 
