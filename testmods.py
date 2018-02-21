import sopel
import requests
from sopel.tools import Identifier
from sopel.tools import SopelMemory
import re

ssthisregex = re.compile('.*\W(?:ss|screenshot) this.*')
def setup(bot):
    if not bot.memory.contains('url_callbacks'):
        bot.memory['url_callbacks'] = SopelMemory()
    bot.memory['url_callbacks'][ssthisregex] = ssthisirc

#@sopel.module.commands('testusers')
def testusers(bot, trigger):
        line = trigger.group(2)
        nicklist = []
        nicks = bot.channels[trigger.sender.lower()].users
        for nick in nicks:
                nicklist.append(nick)
        if any(word in line.split() for word in nicklist):
                bot.say("it matched :(")
        else:
                bot.say(line)

@sopel.module.commands('wittest')
def wittest(bot,trigger):
    line = trigger.group(2)
    res = requests.get("https://api.wit.ai/message?v=20171003&q={}".format(requests.utils.quote(line)), headers = {'Authorization':''}).json() #requires wit.ai api key, and some training.
    try:
        x = res['entities']['datetime'][0]['value']
    except:
        x = res['entities']['datetime'][0]['to']['value']
    bot.say(x)

@sopel.module.rule('.*\W(?:ss|screenshot) this.*')
def ssthisirc(bot,trigger,match=None):
    match = match or trigger
    bot.say('you said ss this!!  content: {}'.format(trigger.group(0)))

@sopel.module.commands('lewd')
def lewd(bot,trigger):
    url = 'https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/analyze'
    headers = {'Ocp-Apim-Subscription-Key': ''} #requires microsoft computer vision api key
    params = {'visualFeatures':'Adult'}
    if trigger.group(2):
        data = {'url': trigger.group(2)}
        req = requests.post(url, headers=headers, params=params, json=data)
        js = req.json()
        if js['adult']['isAdultContent']:
            bot.say("[NSFW] wow lewd... lewd score: %.3f/1.00"%js['adult']['adultScore'])
        else:
            bot.say("phew safe... lewd score: %.3f/1.00"%js['adult']['adultScore'])
