import requests
import sopel

# TODO: Make these config options c:
announce_chan = "#pancakes"
streamers = [
"coalll",
"chouxe",
"kwlpp",
"dasusp",
"lurkk",
"agriks",
"repppie",
"squidgay",
"supersocks",
"sc00ty",
"kaask",
"mole_star",
"twoiis"
]

hstreamers = [
'kwlpp',
'agriks',
'coal',
'chouxe',
'socks',
'dasusp',
'agriks'
]

currently_streaming = {}
currently_hstreaming = {}
currently_ystreaming = {}

@sopel.module.interval(10)
def monitor_streamers(bot):
  streaming_names = []
  streaming = requests.get('https://api.twitch.tv/kraken/streams', params={"channel": ",".join(streamers)}).json()
  results = []
  for streamer in streaming["streams"]:
    streamer_name = streamer["channel"]["name"]
    streamer_game = streamer["channel"]["game"]
    streamer_url = streamer["channel"]["url"]
    streamer_viewers = streamer["viewers"]

    if streamer_name not in currently_streaming:
      currently_streaming[streamer_name] = streamer_game, {'cooldown': 0}
      results.append("%s just went live playing %s! (%s - %s viewer%s)" % (streamer_name,
                                                                          streamer_game,
                                                                          streamer_url,
                                                                          streamer_viewers,
                                                                          "s" if streamer_viewers != 1 else ""))
    elif streamer_game != currently_streaming[streamer_name][0]:
      currently_streaming[streamer_name] = streamer_game, {'cooldown': 0}
      results.append("%s just started playing %s! (%s - %s viewer%s)" % (streamer_name,
                                                                        streamer_game,
                                                                        streamer_url,
                                                                        streamer_viewers,
                                                                        "s" if streamer_viewers != 1 else ""))

    streaming_names.append(streamer_name)

  if results:
    bot.msg(announce_chan, ", ".join(results))

  # Remove people who stopped streaming
  for streamer in currently_streaming.keys():
    if streamer not in streaming_names:
      currently_streaming[streamer][1]['cooldown'] += 10
    if currently_streaming[streamer][1]['cooldown'] > 130:
      del currently_streaming[streamer]

  hstreaming_names = []
  hs = ",".join(hstreamers)
  hstreaming = requests.get('http://api.hitbox.tv/media/live/{0}'.format(hs)).json()
  hresults = []
  for hstreamer in hstreaming["livestream"]:
    if hstreamer["media_is_live"] is "1":
      hstreamer_name = hstreamer["media_user_name"]
      hstreamer_game = hstreamer["category_name"]
      hstreamer_url = hstreamer["channel"]["channel_link"]
      hstreamer_viewers = hstreamer["media_views"]

      if hstreamer_name not in currently_hstreaming:
        currently_hstreaming[hstreamer_name] = hstreamer_game, {'cooldown': 0}
        hresults.append("%s just went live playing %s! (%s - %s viewer%s)" % (hstreamer_name,hstreamer_game,hstreamer_url,hstreamer_viewers,"s" if hstreamer_viewers != 1 else ""))

      elif hstreamer_game != currently_hstreaming[hstreamer_name][0]:
        currently_hstreaming[hstreamer_name] = hstreamer_game, {'cooldown': 0}
        hresults.append("%s just started playing %s! (%s - %s viewer%s)" % (hstreamer_name,hstreamer_game,hstreamer_url,hstreamer_viewers,"s" if hstreamer_viewers != 1 else ""))

      hstreaming_names.append(hstreamer_name)

  if hresults:
    bot.msg(announce_chan, ", ".join(hresults))

  for hstreamer in currently_hstreaming.keys():
    if hstreamer not in hstreaming_names:
      currently_hstreaming[hstreamer][1]['cooldown'] += 10
    if currently_hstreaming[hstreamer][1]['cooldown'] > 130:
      del currently_hstreaming[hstreamer]

  ystreaming_names = []
  yresults = []
  ystreaming = requests.get('https://www.googleapis.com/youtube/v3/search?part=id,snippet&channelId=UCKJTvpLA4kcahLhl5ka-iIw&eventType=live&type=video&key=enteryourkeyhere').json()

  if ystreaming["items"]:
    ystreamer_name = "repppie"
    ystreamer_url = "http://youtube.com/user/repppie/live"
    ystreamer_title = ystreaming["items"][0]["snippet"]["title"]

    if ystreamer_name not in currently_ystreaming:
      currently_ystreaming[ystreamer_name] = ystreamer_title, {'cooldown': 0}
      yresults.append("%s just went live playing %s! ( %s )" % (ystreamer_name, ystreamer_title, ystreamer_url))

    elif ystreamer_title != currently_ystreaming[ystreamer_name][0]:
      currently_ystreaming[ystreamer_name] = ystreamer_title, {'cooldown': 0 }
      yresults.append("%s just started playing %s! ( %s )" % (ystreamer_name, ystreamer_title, ystreamer_url))



    ystreaming_names.append(ystreamer_name)

  if yresults:
    bot.msg(announce_chan, ", ".join(yresults))

  for ystreamer in currently_ystreaming.keys():
    if ystreamer not in ystreaming_names:
      currently_ystreaming[ystreamer][1]['cooldown'] += 10
    if currently_ystreaming[ystreamer][1]['cooldown'] > 130:
      del currently_ystreaming[ystreamer]


@sopel.module.commands('twitchtv','twitch')
@sopel.module.example('.twitch  or .twitch twitchusername')
def streamer_status(bot, trigger):
  streamer_name = trigger.group(2)
  query = streamers if streamer_name is None else streamer_name.split(" ")

  streaming = requests.get('https://api.twitch.tv/kraken/streams', params={"channel": ",".join(query)}).json()
  results = []
  for streamer in streaming["streams"]:
    streamer_name = streamer["channel"]["name"]
    streamer_game = streamer["channel"]["game"]
    streamer_url = streamer["channel"]["url"]
    streamer_viewers = streamer["viewers"]

    results.append("%s is playing %s (%s - %s viewer%s)" % (streamer_name,
                                                           streamer_game,
                                                           streamer_url,
                                                           streamer_viewers,
                                                           "s" if streamer_viewers != 1 else "" ))
  if results:
    bot.say(", ".join(results))
  else:
    bot.say("Nobody is currently streaming.")

@sopel.module.commands('hb','hitbox')
@sopel.module.example('.hb  or .hb twitchusername')
def hstreamer_status(bot, trigger):
  hstreamer_name = trigger.group(2)
  query = ",".join(hstreamers) if hstreamer_name is None else hstreamer_name
  hstreaming = requests.get('http://api.hitbox.tv/media/live/{0}'.format(query)).json()
  hresults = []
  for hstreamer in hstreaming["livestream"]:
    if hstreamer["media_is_live"] is "1":
        hstreamer_name = hstreamer["media_user_name"]
        hstreamer_game = hstreamer["category_name"]
        hstreamer_url = hstreamer["channel"]["channel_link"]
        hstreamer_viewers = hstreamer["media_views"]

        hresults.append("%s is playing %s (%s - %s viewer%s)" % (hstreamer_name,
                                                           hstreamer_game,
                                                           hstreamer_url,
                                                           hstreamer_viewers,
                                                           "s" if hstreamer_viewers != 1 else "" ))
  if hresults:
    bot.say(", ".join(hresults))
  else:
    bot.say("Nobody is currently streaming.")

@sopel.module.commands('yg')
@sopel.module.example('.yg')
def ystreamer_status(bot, trigger):

  ystreaming = requests.get('https://www.googleapis.com/youtube/v3/search?part=id,snippet&channelId=UCKJTvpLA4kcahLhl5ka-iIw&eventType=live&type=video&key=enteryourkeyhere').json()
  yresults = []
  if ystreaming["items"]:
    ystreamer_name = "repppie"
    ystreamer_url = "http://youtube.com/user/repppie/live"
    ystreamer_title = ystreaming["items"][0]["snippet"]["title"]

    yresults.append("%s is playing %s ( %s )" % (ystreamer_name,
                                                 ystreamer_title,
                                                 ystreamer_url))
  if yresults:
    bot.say(", ".join(yresults))
  else:
    bot.say("Nobody is currently streaming.")

@sopel.module.commands('tv')
@sopel.module.example('.tv')
def allstreamer_status(bot, trigger):
  streamer_name = trigger.group(2)
  query = streamers if streamer_name is None else streamer_name.split(" ")

  streaming = requests.get('https://api.twitch.tv/kraken/streams', params={"channel": ",".join(query)}).json()
  results = []
  for streamer in streaming["streams"]:
    streamer_name = streamer["channel"]["name"]
    streamer_game = streamer["channel"]["game"]
    streamer_url = streamer["channel"]["url"]
    streamer_viewers = streamer["viewers"]

    results.append("%s is playing %s (%s - %s viewer%s)" % (streamer_name,
                                                           streamer_game,
                                                           streamer_url,
                                                           streamer_viewers,
                                                           "s" if streamer_viewers != 1 else "" ))
  query = ",".join(hstreamers)
  hstreaming = requests.get('http://api.hitbox.tv/media/live/{0}'.format(query)).json()
  hresults = []
  for hstreamer in hstreaming["livestream"]:
    if hstreamer["media_is_live"] is "1":
        hstreamer_name = hstreamer["media_user_name"]
        hstreamer_game = hstreamer["category_name"]
        hstreamer_url = hstreamer["channel"]["channel_link"]
        hstreamer_viewers = hstreamer["media_views"]

        results.append("%s is playing %s (%s - %s viewer%s)" % (hstreamer_name,
                                                           hstreamer_game,
                                                           hstreamer_url,
                                                           hstreamer_viewers,
                                                           "s" if hstreamer_viewers != 1 else "" ))

  ystreaming = requests.get('https://www.googleapis.com/youtube/v3/search?part=id,snippet&channelId=UCKJTvpLA4kcahLhl5ka-iIw&eventType=live&type=video&key=enteryourkeyhere').json()
  yresults = []

  if ystreaming["items"]:
    ystreamer_name = "repppie"
    ystreamer_url = "http://youtube.com/user/repppie/live"
    ystreamer_title = ystreaming["items"][0]["snippet"]["title"]

    results.append("%s is playing %s ( %s )" % (ystreamer_name,
                                                 ystreamer_title,
                                                 ystreamer_url))

  if results:
    bot.say(", ".join(results))
  else:
    bot.say("Nobody is currently streaming.")
