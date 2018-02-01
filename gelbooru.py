import requests
from bs4 import BeautifulSoup
import random
import re
import sopel
from sopel.tools import SopelMemory

gelregex = re.compile('.*(https?:\/\/gelbooru.com\/.*?id=(\d+).*?((?=[\s])|$))')

def setup(bot):
    if not bot.memory.contains('url_callbacks'):
        bot.memory['url_callbacks'] = SopelMemory()
    bot.memory['url_callbacks'][gelregex] = gelbooruirc

def shutdown(bot):
    del bot.memory['url_callbacks'][gelregex]

@sopel.module.rule('.*(https?:\/\/gelbooru.com\/.*?id=(\d+).*?((?=[\s])|$))')
def gelbooruirc(bot, trigger, match=None):
    match = match or trigger
    id = match.group(2)
    url = "http://gelbooru.com/index.php?page=dapi&s=post&q=index&id={0}".format(id)
    try:
        bs = BeautifulSoup(requests.get(url).content, "html.parser")
    except:
        return
    image = bs.findAll('post')[0]
    rating = image.get('rating')
    if rating == 's':
        lewdness = 'Safe'
    elif rating == 'q':
        lewdness = 'Semi-NSFW'
    elif rating == 'e':
        lewdness = 'NSFW'
    resolution = "{0}x{1}".format(image.get('height'),image.get('width'))
    score = image.get('score')
    tags = image.get('tags').split()
    bot.say('[{0}] Resolution: {1}|Score: {2}|Tags: {3}'.format(lewdness,resolution,score,", ".join(random.sample(tags,6)) if len(tags) > 6 else ", ".join(tags)))

def get_gel_data(terms,pid=None):
    if terms[0].lower() in ['safe','questionable','nsfw']:
        if terms[0].lower() == 'nsfw':
            rating = 'explicit'
        else:
            rating = terms[0].lower()
    else:
        rating = None
    if rating:
        #terms.pop(0)
        tags = 'rating:{0}+{1}'.format(rating, '+'.join(terms[1:]))
    else:
        tags = '+'.join(terms)
    if pid:
        url = 'http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags={0}&pid={1}'.format(tags,pid)
    else:
        url = 'http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags={0}'.format(tags)
    try:
        return BeautifulSoup(requests.get(url).content, "html.parser"), tags
    except:
        return

@sopel.module.commands('gel', 'gelbooru')
@sopel.module.example('.gelbooru search_term or .gelbooru safe search_term')
def gel(bot, trigger):
    if not trigger.group(2):
        return bot.say("Enter a search term.")
    search_term = trigger.split(' ')
    search_term.pop(0)
    bs, tags = get_gel_data(search_term)
    if not bs:
        return
    if bs.find_all('posts')[0].get('count') == '0':
        return bot.say('Nothing but us chickens!')
    else:
        total = bs.findAll('posts')[0].get('count')
        bot.say('[{0} found] http://gelbooru.com/index.php?page=post&s=list&tags={1}'.format(total, tags))

@sopel.module.commands('gbr', 'gelboorurandom')
@sopel.module.example('.gbr search_term or .gbr safe search_term')
def gbr(bot, trigger):
    if not trigger.group(2):
        #return bot.say("Enter a search term.")
        trigger = 'lol  '
    search_term = trigger.split(' ')
    search_term.pop(0)
    i = 10
    bs = None
    while not bs:
        try:
            pid = random.choice(range(i))
        except:
            pid = 0
        bs,tags2 = get_gel_data(search_term,pid)
        if not bs.find_all('post'):
            if i <= 0:
                return bot.say("Nothing but us chickens!")
            bs = None
            i = i-5
    if not bs:
        return
    choosen = random.choice(bs.find_all('post'))
    rating = choosen.get('rating')
    if rating == 's':
        lewdness = 'Safe'
    elif rating == 'q':
        lewdness = 'Semi-NSFW'
    elif rating == 'e':
        lewdness = 'NSFW'
    resolution = "{0}x{1}".format(choosen.get('height'),choosen.get('width'))
    score = choosen.get('score')
    tags = choosen.get('tags').split()
    url = 'http://gelbooru.com/index.php?page=post&s=view&id={0}'.format(choosen.get('id'))
    bot.say('[{0}] {1} Resolution: {2}|Score: {3}|Tags: {4}'.format(lewdness,url,resolution,score,", ".join(random.sample(tags,6)) if len(tags) > 6 else ", ".join(tags)))
