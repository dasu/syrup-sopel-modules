import sopel
from sopel.tools import SopelMemory
import soundcloud
import re

scregex = re.compile('.*(https?:\/\/soundcloud.com\/.*?\/.*?((?=[\s])|$))')

def setup(bot):
    if not bot.memory.contains('url_callbacks'):
        bot.memory['url_callbacks'] = SopelMemory()
    bot.memory['url_callbacks'][scregex] = soundcloudirc

def shutdown(bot):
    del bot.memory['url_callbacks'][scregex]

client = soundcloud.Client(
    client_id='id',
    client_secret='secret',
    username='email',
    password='password')
    
@sopel.module.rule('.*(https?:\/\/soundcloud.com\/.*?\/.*?((?=[\s])|$))')
def soundcloudirc(bot, trigger, match=None):
    match = match or trigger
    track = client.get('/resolve', url=match.group(1))
    title = track.title
    artist = track.user['username']
    plays = track.playback_count
    favorites = track.favoritings_count
    hours, ms = divmod(track.duration, 3600000)
    minutes, ms = divmod(ms, 60000)
    seconds = float(ms)/1000
    time = "%02i:%i" % ( minutes, seconds) if hours is 0 else "%i:%02i:%i" % (hours, minutes, seconds)
    genre = track.genre


    bot.say("{0} - {1} [{2}] ►:{3} ❤:{4} Genre: {5}".format(artist,title,time,plays,favorites,genre))
