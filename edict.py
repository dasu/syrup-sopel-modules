from urllib.request import urlopen, quote
from bs4 import BeautifulSoup
import sopel
@sopel.module.commands('edict')
@sopel.module.example('.edict word/character')
def edict(bot, trigger):
    if not trigger.group(2):
        return bot.say("Please enter a word.")
    i = trigger.group(2)
    try:
        i.encode('ascii')
        print(i)
        x = urlopen("http://nihongo.monash.edu/cgi-bin/wwwjdic?1ZDJ{0}".format(i))
        c = x.read()
        bs = BeautifulSoup(c)
        #print(bs)
        if bs.pre:
            res = bs.pre.contents[0].splitlines()[1]
            #print(res)
        else:
            res = "No matches found."
        bot.say(res)
    except:
        print(i)
        x = urlopen("http://nihongo.monash.edu/cgi-bin/wwwjdic?1ZIK{0}".format(quote(i)))
        c = x.read()
        bs = BeautifulSoup(c)
        if bs.li:
            res = bs.li.contents[0]
        else:
            res = "No matches found."
        bot.say(res)
