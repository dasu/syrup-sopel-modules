#from feety

import sopel
from random import choice
import datetime
import requests

alotImages = ["http://i.imgur.com/7GJ5XoB.png",
              "http://i.imgur.com/xncEQ8B.png",
              "http://i.imgur.com/3t5QHBu.png",
              "http://i.imgur.com/Bz2ei9E.png",
              "http://i.imgur.com/lqBkdnP.png",
              "http://i.imgur.com/7gdB5fU.png",
              "http://i.imgur.com/B0jd549.png",
              "http://i.imgur.com/4Jpt8k6.png",
              "http://i.imgur.com/BlEay4o.png",
              "http://i.imgur.com/5X5a4ZQ.png",
              "http://i.imgur.com/iLLLhnP.png",
              "http://i.imgur.com/nMgttwX.png"]

@sopel.module.commands('pax')
def pax(bot, trigger):
   now = datetime.datetime.now()     
   pax = datetime.datetime(2015, 3, 6, 10)
   delta = pax - now
   if delta.days < 6:
      hours, remainder = divmod(delta.seconds, 3600)
      minutes, seconds = divmod(remainder, 60) 
      output = "{days} days, {hours} hours, {minutes} minutes, and {seconds} seconds until PAX!".format(days=delta.days, hours=hours, minutes=minutes, seconds=seconds)
   else:
      output = "%s days until PAX!" % delta.days
   bot.say(output)

@sopel.module.rule(r'(^|.+ )alot( .+|$)')
def alot(bot, trigger):
   bot.say("%s LEARN TO SPELL: %s" % (trigger.nick, choice(alotImages)))

@sopel.module.commands('zen')
def zen(bot, trigger):
   bot.say(requests.get("https://api.github.com/zen").text)

@sopel.module.commands('nfact')
def nfact(bot, trigger):
   bot.say(requests.get("http://numbersapi.com/random").text)

@sopel.module.commands('42')
def fourtytwo(bot, trigger):
   bot.say(requests.get("http://numbersapi.com/42").text)

@sopel.module.commands('tfact')
def today(bot, trigger):
   month = datetime.datetime.now().month
   day = datetime.datetime.now().day
   bot.say(requests.get("http://numbersapi.com/%s/%s/date" % (month, day)).text)

@sopel.module.commands('askreddit', 'asscredit')
def ask(bot, trigger):
  header =  {"User-Agent": "Boredbot/1.0 by sc00ty"}
  bot.say(choice(requests.get("http://www.reddit.com/r/askreddit.json?limit=100", headers=header).json()["data"]["children"])["data"]["title"])

@sopel.module.commands('shower')
def shower(bot, trigger):
  header =  {"User-Agent": "Boredbot/1.0 by sc00ty"}
  bot.say(choice(requests.get("http://www.reddit.com/r/showerthoughts.json?limit=100", headers=header).json()["data"]["children"])["data"]["title"])

@sopel.module.commands('5050')
def fifty(bot, trigger):
  header =  {"User-Agent": "Boredbot/1.0 by sc00ty"}
  pick = choice(requests.get("http://www.reddit.com/r/fiftyfifty.json?limit=100", headers=header).json()["data"]["children"])["data"]
  bot.say("%s - %s" % (pick["title"], pick["url"]))

@sopel.module.commands('rather')
def rather(bot, trigger):
  header =  {"User-Agent": "Boredbot/1.0 by sc00ty"}
  bot.say(choice(requests.get("http://www.reddit.com/r/wouldyourather.json?limit=100", headers=header).json()["data"]["children"])["data"]["title"])


@sopel.module.commands('mirror', 'h', 'h1x0')
def mirror(bot, trigger):
  if trigger.group(2):
    bot.say("http://m.h1x0.net/%s" % trigger.group(2))
