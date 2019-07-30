import sopel
import requests
from sopel.tools import SopelMemory
import re
import html #python3.5+

hnregex = re.compile('.*https?:\/\/news\.ycombinator.com\/item\?id=(\d{1,15}).*?((?=[\s])|$)')

def setup(bot):
    if not bot.memory.contains('url_callbacks'):
        bot.memory['url_callbacks'] = SopelMemory()
    bot.memory['url_callbacks'][hnregex] = hnirc

def shutdown(bot):
    del bot.memory['url_callbacks'][hnregex]

@sopel.module.commands('reversehn','rhn')
@sopel.module.example('.rhn url')
def rhn(bot, trigger):
    if not trigger.group(2):
        if trigger.sender not in bot.memory['last_seen_url']:
            return
        rhnurl = bot.memory['last_seen_url'][trigger.sender]
    else:
        rhnurl = trigger.group(2)
    x = requests.get("https://hn.algolia.com/api/v1/search?query={}".format(rhnurl)).json()
    try:
        return bot.say("https://news.ycombinator.com/item?id={} | {} | \U0001F4AC:{}".format(x['hits'][0]['objectID'],x['hits'][0]['title'],x['hits'][0]['num_comments']))
    except:
        return bot.say("No HN discussion found")

@sopel.module.rule('.*https?:\/\/news\.ycombinator.com\/item\?id=(\d{1,15}).*?((?=[\s])|$)')
def hnirc(bot, trigger, match=None):
    match = match or trigger
    x = requests.get('https://hacker-news.firebaseio.com/v0/item/{}.json'.format(match.group(1))).json()
    if x['type'] == 'comment':
        bot.say('[HN Comment] {}'.format(html.unescape(x['text'])))
    else:
        bot.say('{}{} | Score: {} | Comments: {}'.format("[DEAD] "if x.get('dead') else '', x['title'], x['score'], x.get('descendants') or '0'))
