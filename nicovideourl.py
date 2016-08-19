import random
import sopel
from sopel.tools import SopelMemory
from nicovideo import Nicovideo
import re

nvregex = re.compile('.*(https?:\/\/(?:www\.)?nicovideo\.jp\/watch\/(.*?)((?=[\s])|$))')

def setup(bot):
    if not bot.memory.contains('url_callbacks'):
        bot.memory['url_callbacks'] = SopelMemory()
    bot.memory['url_callbacks'][nvregex] = nicovideoirc

def shutdown(bot):
    del bot.memory['url_callbacks'][nvregex]

@sopel.module.rule('.*(https?:\/\/(?:www\.)?nicovideo\.jp\/watch\/(.*?)((?=[\s])|$))')
def nicovideoirc(bot, trigger, match=None):
    match = match or trigger
    id = match.group(2)
    nico = Nicovideo()
    nico.append(id)
    title = nico._video[id].title
    seconds = nico._video[id].length
    duration = '%d:%02d' % (seconds / 60, seconds % 60)
    views = nico._video[id].view_counter
    tags = ", ".join(random.sample(nico._video[id].tags,3)) if len(nico._video[id].tags) > 3 else ", ".join(nico._video[id].tags)
    bot.say(u"{} [{}]| ►:{} | Tags: {}".format(title,duration,views,tags))
