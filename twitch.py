#As of 09-14-2016, twitch API now requires Client-ID with all requests.  You will need to create one from here: 
# https://www.twitch.tv/settings/connections
# complete twitch.py rewrite coming soon™
import requests
import sopel
import re
from sopel.tools import SopelMemory
import datetime

# TODO: Make these config options c:
twitchclientid = "clientIDgoeshere" 
announce_chan = "#pancakes"
logchannel = "#whateverchannelyouwant" #used for live logging certain issues that plague this module
streamers = [
"coalll",
"chouxe",
"kwlpp",
"dasu_",
"esicra",
"agriks",
"repppie",
"squidgay",
"supersocks",
"sc00ty",
"kaask",
"mole_star",
"twoiis",
"sasserr",
"mogra" #untz untz
]
#end config

twitchregex = re.compile('(?!.*\/v\/).*https?:\/\/(?:(?:www\.)|(?:go\.))?twitch.tv\/(.*?)\/?(?:(?=[\s])|$)')
mixerregex = re.compile('(?!.*\/v\/).*https?:\/\/(?:www\.)?mixer.com\/(.*?)\/?(?:(?=[\s])|$)')
twitchclipsregex = re.compile('(?!.*\/v\/).*https?:\/\/clips\.twitch.tv\/(.*?)\/?(?:(?=[\s])|$)')

def setup(bot):
    if not bot.memory.contains('url_callbacks'):
        bot.memory['url_callbacks'] = SopelMemory()
    bot.memory['url_callbacks'][twitchregex] = twitchirc
    bot.memory['url_callbacks'][mixerregex] = mixerirc
    bot.memory['url_callbacks'][twitchclipsregex] = twitchclipsirc

def shutdown(bot):
    del bot.memory['url_callbacks'][twitchregex]
    del bot.memory['url_callbacks'][mixerregex]
    del bot.memory['url_callbacks'][twitchclipsregex]

currently_streaming = {}
currently_ystreaming = {}
tsep = lambda a : "{:,}".format(int(a))

@sopel.module.interval(20)
def monitor_streamers(bot):
  streaming_names = []
  try:
    streaming = requests.get('https://api.twitch.tv/kraken/streams', params={"channel": ",".join(streamers)}, headers={"Client-ID":twitchclientid}).json()
  except Exception as  e:
    return print("There was an error reading twitch API  {0}".format(e))
  results = []
  if streaming.get("streams"):
    for streamer in streaming["streams"]:
      streamer_name = streamer["channel"]["name"]
      streamer_game = streamer["channel"]["game"]
      streamer_status = streamer["channel"]["status"]
      streamer_url = streamer["channel"]["url"]
      streamer_starttime = datetime.datetime.strptime(streamer['created_at'], '%Y-%m-%dT%H:%M:%SZ')
      streamer_viewers = streamer["viewers"]
    
      if streamer_name not in currently_streaming:
        currently_streaming[streamer_name] = streamer_game, {'cooldown': 0, 'starttime': streamer_starttime}
        results.append("%s just went live playing %s! [%s] (%s - %s viewer%s)" % (streamer_name, 
                                                                          streamer_game, 
                                                                          streamer_status,
                                                                          streamer_url, 
                                                                          tsep(streamer_viewers), 
                                                                          "s" if streamer_viewers != 1 else ""))
      streaming_names.append(streamer_name)

  if results:
    bot.msg(announce_chan, ", ".join(results))  

  # Remove people who stopped streaming
  for streamer in list(currently_streaming):
    if streamer not in streaming_names:
      currently_streaming[streamer][1]['cooldown'] += 10
    if currently_streaming[streamer][1]['cooldown'] > 130:
      #bot.msg(logchannel,'{0} was removed from currently_streaming for reaching a cooldown of {1}'.format(streamer,currently_streaming[streamer][1]['cooldown']))
      del currently_streaming[streamer]

@sopel.module.commands('twitchtv','twitch','tv')
@sopel.module.example('.twitch  or .twitch twitchusername')
def streamer_status(bot, trigger):
  streamer_name = trigger.group(2)
  query = streamers if streamer_name is None else streamer_name.split(" ")

  streaming = requests.get('https://api.twitch.tv/kraken/streams', params={"channel": ",".join(query)}, headers={"Client-ID":twitchclientid}).json()
  results = []
  if streaming.get("streams"):
    for streamer in streaming["streams"]:
      streamer_name = streamer["channel"]["name"]
      streamer_game = streamer["channel"]["game"]
      streamer_status = streamer["channel"]["status"]
      streamer_url = streamer["channel"]["url"]
      streamer_viewers = streamer["viewers"]
    
      results.append("%s is playing %s [%s] (%s - %s viewer%s)" % (streamer_name, 
                                                           streamer_game, 
                                                           streamer_status,
                                                           streamer_url, 
                                                           tsep(streamer_viewers), 
                                                           "s" if streamer_viewers != 1 else "" ))
  if results:
    bot.say(", ".join(results))
  else:
    bot.say("Nobody is currently streaming.")

@sopel.module.rule('(?!.*\/v\/).*https?:\/\/(?:(?:www\.)|(?:go\.))?twitch.tv\/(.*?)\/?(?:(?=[\s])|$)')
def twitchirc(bot, trigger, match = None):
  match = match or trigger
  streamer_name = match.group(1)
  query = streamers if streamer_name is None else streamer_name.split(" ")
  streaming = requests.get('https://api.twitch.tv/kraken/streams', params={"channel": ",".join(query)}, headers={"Client-ID":twitchclientid}).json()
  results = []
  if streaming.get("streams"):
    for streamer in streaming["streams"]:
      streamer_name = streamer["channel"]["name"]
      streamer_game = streamer["channel"]["game"]
      streamer_status = streamer["channel"]["status"]
      streamer_viewers = streamer["viewers"]

      results.append("%s is playing %s [%s] - %s viewer%s" % (streamer_name,
                                                           streamer_game,
                                                           streamer_status,
                                                           tsep(streamer_viewers),
                                                           "s" if streamer_viewers != 1 else "" ))
  if results:
    bot.say(", ".join(results))
  else:
    pass

@sopel.module.rule('(?!.*\/v\/).*https?:\/\/(?:www\.)?mixer.com\/(.*?)\/?(?:(?=[\s])|$)')
def mixerirc(bot, trigger, match = None):
  match = match or trigger
  streamer_name = match.group(1)
  streaming = requests.get('https://mixer.com/api/v1/channels/{}'.format(streamer_name)).json()
  results = []
  if streaming:
    streamer_name = streaming["token"]
    if streaming.get("type"):
      streamer_game = streaming["type"]["name"]
    else:
      streamer_game = "a game"
    streamer_status = streaming["name"]
    streamer_viewers = streaming["viewersCurrent"]

  results.append("%s is playing %s [%s] - %s viewer%s" % (streamer_name,
                                                         streamer_game,
                                                         streamer_status,
                                                         tsep(streamer_viewers),
                                                         "s" if streamer_viewers != 1 else "" ))
  if results:
    bot.say(", ".join(results))
  else:
    pass

@sopel.module.rule('.*(?:https?:\/\/clips\.twitch.tv\/(.*?)\/?(?:(?=[\s])|$))|(?:https?:\/\/(?:www)?\.twitch\.tv\/.*?\/clip\/(.*?)\/?(?:(?=[\s])|$))')
def twitchclipsirc(bot,trigger, match = None):
  match = match or trigger
  slug = match.group(1) or match.group(2)
  clips = requests.get("https://api.twitch.tv/kraken/clips/{}".format(slug), headers={"Client-ID":twitchclientid,"Accept":"application/vnd.twitchtv.v5+json"}).json()
  name = clips['broadcaster']['display_name']
  title = clips['title']
  game = clips['game']
  views = clips['views']
  bot.say("{} [{}] | {} | {} views".format(title, game, name, tsep(views)))

@sopel.module.commands('debugtv')
def debug(bot, trigger):
    bot.msg(logchannel,"currently_streaming: {}".format(", ".join(currently_streaming)))
