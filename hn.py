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
        return bot.say("Enter a URL to see if there is a HN discussion")
    x = requests.get("https://hn.algolia.com/api/v1/search?query={}".format(trigger.group(2))).json()
    try:
        return bot.say("https://news.ycombinator.com/item?id={}".format(x['hits'][0]['objectID']))
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
