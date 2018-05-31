import sopel
import requests

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
