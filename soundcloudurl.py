import sopel
from sopel.tools import SopelMemory
import soundcloud
import re

scregex = re.compile('.*(https?:\/\/soundcloud.com\/.*?\/.*?((?=[\s])|$))')
client_id = '' #soundcloud client ID
def setup(bot):
    if not bot.memory.contains('url_callbacks'):
        bot.memory['url_callbacks'] = SopelMemory()
    bot.memory['url_callbacks'][scregex] = soundcloudirc

def shutdown(bot):
    del bot.memory['url_callbacks'][scregex]

@sopel.module.rule('.*(https?:\/\/soundcloud.com\/.*?\/.*?((?=[\s])|$))')
def soundcloudirc(bot, trigger, match=None):
    client = soundcloud.Client(client_id=client_id)
    match = match or trigger
    try:
        track = client.get('/resolve', url=match.group(1), client_id=client_id)
    except:
        return
    title = track.title
    artist = track.user['username']
    hours, ms = divmod(track.duration, 3600000)
    minutes, ms = divmod(ms, 60000)
    seconds = float(ms)/1000
    time = "%02i:%02i" % ( minutes, seconds) if hours is 0 else "%02i:%02i:%02i" % (hours, minutes, seconds)
    genre = track.genre
    if track.kind == 'track':
        plays = track.playback_count
        favorites = track.favoritings_count
        bot.say(u"{0} - {1} [{2}] ►:{3} ❤:{4} Genre: {5}".format(artist,title,time,plays,favorites,genre))
    if track.kind == 'playlist':
        track_count = track.track_count
        bot.say(u"{0} - {1} [{2}] Tracks: {3} Genre: {4}".format(artist,title,time,track_count,genre))
