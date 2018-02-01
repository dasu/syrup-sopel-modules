import requests
from bs4 import BeautifulSoup
import sopel

def get_defintion(word,search_method):
    result = requests.get("http://nihongo.monash.edu/cgi-bin/wwwjdic?{0}{1}".format(search_method,word))
    return BeautifulSoup(result.content, "html.parser")

@sopel.module.commands('edict')
@sopel.module.example('.edict word/character')
def edict(bot, trigger):
    if not trigger.group(2):
        return bot.say("Please enter a word.")
    word = trigger.group(2)
    try:
        word.encode('ascii')
        edict_return = get_defintion(word,'1ZDJ')
        if edict_return.pre:
            return bot.say(edict_return.pre.contents[0].splitlines()[1])
        else:
            return bot.say("No matches found.")
    except:
        edict_return = get_defintion(word,'1ZIK')
        if edict_return.li:
            return bot.say(edict_return.li.contents[0])
        else:
            return bot.say("No matches found.")
