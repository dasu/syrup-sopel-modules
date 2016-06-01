import requests
import sopel
import json

@sopel.module.commands('partypoi','djpoi','dubpoi')
def djpoi(bot,trigger):
    #bot.say("")
    x = requests.get("http://api.dubtrack.fm/room/563eabe1d4c45a1e00caa25a").json()
    if not x['data']['currentSong']:
        bot.say("さあ、素敵なパーティーしましょう https://www.dubtrack.fm/join/pancakes")
    else:
        bot.say("Current song: {0} Listeners: {1} | https://www.dubtrack.fm/join/pancakes".format(x['data']['currentSong']['name'],x['data']['activeUsers']))

@sopel.module.commands('party','dj', 'dub','dubtrack')
def dj(bot,trigger):
    #bot.say("The party is dead.")
    x = requests.get("http://api.dubtrack.fm/room/563eabe1d4c45a1e00caa25a").json()
    if not x['data']['currentSong']:
        bot.say("It's a party! https://www.dubtrack.fm/join/pancakes")
    else:
        bot.say("Current song: {0} Listeners: {1} | https://www.dubtrack.fm/join/pancakes".format(x['data']['currentSong']['name'],x['data']['activeUsers']))

@sopel.module.commands('plug','plugdj')
def plugdj(bot,trigger):
        bot.say("It's a party! https://plug.dj/4045415754446389448")
