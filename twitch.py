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
"dasusp",
"lurkk",
"agriks",
"repppie",
"squidgay",
"supersocks",
"sc00ty",
"kaask",
"mole_star",
"twoiis",
"sasserr"
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
#end config

twitchregex = re.compile('(?!.*\/v\/).*https?:\/\/(?:www\.)?twitch.tv\/(.*?)\/?(?:(?=[\s])|$)')

def setup(bot):
    if not bot.memory.contains('url_callbacks'):
        bot.memory['url_callbacks'] = SopelMemory()
    bot.memory['url_callbacks'][twitchregex] = twitchirc

def shutdown(bot):
    del bot.memory['url_callbacks'][twitchregex]

currently_streaming = {}
currently_hstreaming = {}
currently_ystreaming = {}

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
      streamer_url = streamer["channel"]["url"]
      streamer_starttime = datetime.datetime.strptime(streamer['created_at'], '%Y-%m-%dT%H:%M:%SZ')
      streamer_viewers = streamer["viewers"]
    
      if streamer_name not in currently_streaming:
        currently_streaming[streamer_name] = streamer_game, {'cooldown': 0, 'starttime': streamer_starttime}
        results.append("%s just went live playing %s! (%s - %s viewer%s)" % (streamer_name, 
                                                                          streamer_game, 
                                                                          streamer_url, 
                                                                          streamer_viewers, 
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

  hstreaming_names = []
  hs = ",".join(hstreamers)
  try:
    testingtimeout = datetime.datetime.now()
    hstreaming = requests.get('http://api.hitbox.tv/media/live/{0}'.format(hs),timeout=(1.5,1.5)).json()
  except requests.exceptions.ConnectionError:
    #return bot.msg(logchannel,"timeout time: {}".format((datetime.datetime.now() - testingtimeout).total_seconds()))
  except:
    #return bot.msg(logchannel,"error with hitbox api")
  hresults = []
  if hstreaming.get("livestream"):
    for hstreamer in hstreaming["livestream"]:
      if hstreamer["media_is_live"] is "1":
        hstreamer_name = hstreamer["media_user_name"]
        hstreamer_game = hstreamer["category_name"]
        hstreamer_url = hstreamer["channel"]["channel_link"]
        hstreamer_viewers = hstreamer["media_views"]
      
        if hstreamer_name not in currently_hstreaming:
          currently_hstreaming[hstreamer_name] = hstreamer_game, {'cooldown': 0}
          hresults.append("%s just went live playing %s! (%s - %s viewer%s)" % (hstreamer_name,hstreamer_game,hstreamer_url,hstreamer_viewers,"s" if hstreamer_viewers != 1 else ""))

        hstreaming_names.append(hstreamer_name)

  if hresults:
    bot.msg(announce_chan, ", ".join(hresults))
  
  for hstreamer in list(currently_hstreaming):
    if hstreamer not in hstreaming_names:
      currently_hstreaming[hstreamer][1]['cooldown'] += 10
    if currently_hstreaming[hstreamer][1]['cooldown'] > 130:
      del currently_hstreaming[hstreamer]

@sopel.module.commands('twitchtv','twitch')
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

@sopel.module.commands('tv')
@sopel.module.example('.tv')
def allstreamer_status(bot, trigger):
  streamer_name = trigger.group(2)
  query = streamers if streamer_name is None else streamer_name.split(" ")

  streaming = requests.get('https://api.twitch.tv/kraken/streams', params={"channel": ",".join(query)}, headers={"Client-ID":twitchclientid}).json()
  results = []
  if streaming.get("streams"):
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
  if hstreaming.get("livestream"):
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

  if results:
    bot.say(", ".join(results))
  else:
    bot.say("Nobody is currently streaming.")

@sopel.module.rule('(?!.*\/v\/).*https?:\/\/(?:www\.)?twitch.tv\/(.*?)\/?(?:(?=[\s])|$)')
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
                                                           streamer_viewers,
                                                           "s" if streamer_viewers != 1 else "" ))
  if results:
    bot.say(", ".join(results))
  else:
    pass
    #bot.say("Nobody is currently streaming.")

@sopel.module.commands('debugtv')
def debug(bot, trigger):
    bot.msg(logchannel,"currently_streaming: {}".format(", ".join(currently_streaming)))
    bot.msg(logchannel,"currently_hstreaming: {}".format(", ".join(currently_hstreaming)))
