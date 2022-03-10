# As of 02-28-2022, twitch api moved over to new api, and requires a client ID and client secret key which can be generated from here:
# https://dev.twitch.tv/
# more info on new api here: https://dev.twitch.tv/docs/api/migration
# complete twitch.py rewrite coming soon™
import requests
import sopel
import re
from sopel.tools import SopelMemory
import datetime

# TODO: Make these config options c:
twitchclientid = "twitchclientidgoeshere"
twitchclientsecret = "twitchclientsecretgoeshere"
token = "" #gets populated on startup, and refreshed occasionally
announce_chan = "#pancakes"
logchannel = "#dasu" #used for live logging certain issues that plague this module
streamers = [
"31847612", #coalll
"22725500", #kwlpp
"27513704", #dasu_
"30346664", #agriks
"44191385", #repppie
"24683935", #supersocks
"26979782", #sc00ty
"37155900"  #kaask
]
#end config

twitchregex = re.compile('.*https?:\/\/(?:(?:www\.)|(?:go\.))?twitch.tv\/(.*?)\/?(?:(?=[\s|\/])|$)')
twitchclipsregex = re.compile('.*https?:\/\/clips\.twitch.tv\/(.*?)\/?(?:(?=[\s])|$)')

def tokensetup(bot, twitchclientid, twitchclientsecret):
    x = requests.post('https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type=client_credentials'.format(twitchclientid,twitchclientsecret))
    global token
    token = x.json()['access_token']

def setup(bot):
    if not bot.memory.contains('url_callbacks'):
        bot.memory['url_callbacks'] = SopelMemory()
    bot.memory['url_callbacks'][twitchregex] = twitchirc
    bot.memory['url_callbacks'][twitchclipsregex] = twitchclipsirc
    tokensetup(bot,twitchclientid,twitchclientsecret)

def shutdown(bot):
    del bot.memory['url_callbacks'][twitchregex]
    del bot.memory['url_callbacks'][twitchclipsregex]

currently_streaming = {}
currently_ystreaming = {}
tsep = lambda a : "{:,}".format(int(a))

def twitch_api(stream_list):
  """ Returns the result of the http request from Twitch's api """
  return requests.get('https://api.twitch.tv/helix/streams?{}'.format('&'.join(map('user_id={}'.format,stream_list))), headers={"Client-ID": twitchclientid, "Authorization":"Bearer {}".format(token)}).json()

def gettwitchuserid(tuser):
    tuid = requests.get("https://api.twitch.tv/helix/users?login={}".format(tuser),headers={"Client-ID":twitchclientid,"Authorization":"Bearer {}".format(token)}).json()
    if not tuid['data']:
      return None
    else:
      return [tuid['data'][0]['id']]

def twitch_generator(streaming):
  for streamer in streaming["data"]:
    streamer_dict = {}
    streamer_dict["name"] = streamer["user_name"]
    streamer_dict["game"] = streamer["game_name"]
    streamer_dict["status"] = streamer["title"]
    streamer_dict["url"] = "https://twitch.tv/{}".format(streamer["user_login"])
    streamer_dict["starttime"] = datetime.datetime.strptime(streamer['started_at'], '%Y-%m-%dT%H:%M:%SZ')
    streamer_dict["viewers"] = streamer["viewer_count"]
    yield streamer_dict

@sopel.module.interval(20)
def monitor_streamers(bot):
  streaming_names = []
  try:
    streaming = twitch_api(streamers)
  except Exception as  e:
    return print("There was an error reading twitch API  {0}".format(e))
  results = []
  if streaming.get("data"):
    twitch_gen = twitch_generator(streaming)
    for streamer in twitch_gen:
      if streamer["name"] not in currently_streaming:
        currently_streaming[streamer["name"]] = streamer["game"], {'cooldown': 0, 'starttime': streamer["starttime"]}
        results.append("%s just went live playing %s! [%s] (%s - %s viewer%s)" % (streamer["name"],
                                                                                  streamer["game"],
                                                                                  streamer["status"],
                                                                                  streamer["url"],
                                                                                  tsep(streamer["viewers"]),
                                                                                  "s" if streamer["viewers"] != 1 else ""))
      streaming_names.append(streamer["name"])

  if results:
    bot.msg(announce_chan, ", ".join(results))
    #bot.msg(logchannel,"announced {}".format(streamer["name"]))
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
  query = streamers if streamer_name is None else gettwitchuserid(streamer_name)
  if query is None:
    return bot.say("Nobody is currently streaming")
  try:
    streaming = twitch_api(query)
  except Exception as  e:
    return print("There was an error reading twitch API  {0}".format(e))
  results = []
  if streaming.get("data"):
    twitch_gen = twitch_generator(streaming)
    for streamer in twitch_gen:
      results.append("%s is playing %s [%s] (%s - %s viewer%s)" % (streamer["name"],
                                                                   streamer["game"],
                                                                   streamer["status"],
                                                                   streamer["url"],
                                                                   tsep(streamer["viewers"]),
                                                                   "s" if streamer["viewers"] != 1 else ""))
  if results:
    bot.say(", ".join(results))
  else:
    bot.say("Nobody is currently streaming.")

@sopel.module.rule('.*https?:\/\/(?:(?:www\.)|(?:go\.))?twitch.tv\/(.*?)\/?(?:(?=[\s|\/])|$)')
def twitchirc(bot, trigger, match = None):
  match = match or trigger
  streamer_name = match.group(1)
  query = streamers if streamer_name is None else gettwitchuserid(streamer_name)
  try:
    streaming = twitch_api(query)
  except Exception as  e:
    return print("There was an error reading twitch API  {0}".format(e))
  results = []
  if streaming.get("data"):
    twitch_gen = twitch_generator(streaming)
    for streamer in twitch_gen:
      results.append("%s is playing %s [%s] (%s - %s viewer%s)" % (streamer["name"],
                                                                   streamer["game"],
                                                                   streamer["status"],
                                                                   streamer["url"],
                                                                   tsep(streamer["viewers"]),
                                                                   "s" if streamer["viewers"] != 1 else ""))
  if results:
    bot.say(", ".join(results))
  else:
    pass

@sopel.module.rule('.*(?:https?:\/\/clips\.twitch.tv\/(.*?)\/?(?:(?=[\s])|$))|.*(?:https?:\/\/(?:www)?\.twitch\.tv\/.*?\/clip\/(.*?)\/?(?:(?=[\s])|$))')
def twitchclipsirc(bot,trigger, match = None):
  match = match or trigger
  slug = match.group(1) or match.group(2)
  clips = requests.get("https://api.twitch.tv/helix/clips?id={}".format(slug), headers={"Client-ID": twitchclientid, "Authorization":"Bearer {}".format(token)}).json()
  name = clips['data'][0]['broadcaster_name']
  title = clips['data'][0]['title']
  game = clips['data'][0]['game_id'] #need to add gameid->game name function
  views = clips['data'][0]['view_count']
  bot.say("{} [{}] | {} | {} views".format(title, game, name, tsep(views)))

@sopel.module.commands('debugtv')
def debug(bot, trigger):
    bot.msg(logchannel,"currently_streaming: {}".format(", ".join(currently_streaming)))
