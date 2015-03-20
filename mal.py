#MAL anime module v0.60
#thanks agri for index error shit fix

import urllib.request
from bs4 import BeautifulSoup
import willie

def connect(url):
        opener = urllib.request.build_opener()
        auth_string = ''
        opener.addheaders = [('User-Agent', ''),('Authorization', auth_string),]
        x = opener.open(url).read()
        bs = BeautifulSoup(x)
        return (bs, x)

@willie.module.commands('mal')
def mal(bot,trigger):
        if not trigger.group(2):
            return bot.say("Enter an anime name you weeaboo.")
        i = trigger.group(2)
        if len(i)>1 and len(trigger.group())>5:
            i = urllib.request.quote(i)
            d = 'http://myanimelist.net/api/anime/search.xml?q={0}'.format(i)
            bs, x = connect(d)
            if len(x) > 14:
                if bs.find('type').string == 'Movie':
                    bot.reply('{0} ({2}): http://myanimelist.net/anime/{1}'.format(bs.find('title').string, bs.find('id').string, bs.find('type').string))
                else:
                    bot.reply('{0} (eps:{2}) http://myanimelist.net/anime/{1}'.format(bs.find('title').string, bs.find('id').string, bs.find('episodes').string))
            else:
                bot.say("Wakaranai ┐(-｡ｰ;)┌")
        else:
            bot.say("Wakaranai ┐(-｡ｰ;)┌")

@willie.module.commands('manga')
def manga(bot,trigger):
        if not trigger.group(2):
                return bot.say("Enter a mango name you weeaboo.")
        i = trigger.group(2)
        if len(i)>1 and len(trigger.group())>7:
                i = urllib.request.quote(i)
                uri = 'http://myanimelist.net/api/manga/search.xml?q={0}'.format(i)
                bs, x = connect(uri)
                if len(x) > 14:
                        bot.reply('{0} ({2}): http://myanimelist.net/manga/{1}'.format(bs.find('title').string, bs.find('id').string, bs.find('chapters').string))
                else:
                        bot.say("Wakaranai ┐(-｡ｰ;)┌")
        else:
                bot.say("Wakaranai ┐(-｡ｰ;)┌")

@willie.module.commands('people','va','seiyuu','malva')
def people(bot,trigger):
        if not trigger.group(2):
                return bot.say("Enter a name, retard")
        i = trigger.group(2)
        if len(i)>1 and len(trigger.group())>8:
                i = urllib.request.quote(i)
                uri = 'http://myanimelist.net/people.php?q={0}'.format(i)
                bs, x = connect(uri)
                if len(x) > 14 and bs.body.findAll("table")[1].findAll("tr")[1].td.string != 'No results returned':
                       if not bs.body.findAll(text='Search Results'):
                                bot.say(bs.h1.string + ": http://myanimelist.net" + bs.findAll(id="horiznav_nav")[0].a['href'])
                       else:
                                bot.say(bs.body.findAll("table")[1].findAll("tr")[1].findAll("td")[1].a.string + ": http://myanimelist.net" + bs.body.findAll("table")[1].findAll("tr")[1].a['href'])
                else:
                        bot.say("No results found. ┐(-｡ｰ;)┌")
        else:
                bot.say("Please enter a proper term. ┐(-｡ｰ;)┌")

@willie.module.commands('character','malc')
def character(bot,trigger):
        if not trigger.group(2):
                return bot.say("Enter a name, retard")
        i = trigger.group(2)
        if len(i)>1 and len(trigger.group())>11:
                i = urllib.request.quote(i)
                uri = 'http://myanimelist.net/character.php?q={0}'.format(i)
                bs, x = connect(uri)
                if len(x) > 14 and bs.body.findAll("table")[1].findAll("tr")[1].td.string != 'No results returned': #or 'No results found'
                       if not bs.body.findAll(text='Search Results'):
                                bot.say(bs.h1 + ": http://myanimelist.net" + bs.findAll(id="horiznav_nav")[0].a['href'])
                       else:
                                bot.say(bs.body.findAll("table")[1].findAll("tr")[1].findAll("td")[1].a.string + " from: " + bs.body.findAll("table")[1].findAll("tr")[1].findAll('td')[2].a.string + " http://myanimelist.net" + bs.body.findAll("table")[1].findAll("tr")[1].a['href'])
                else:
                        bot.say("No results found. ┐(-｡ｰ;)┌")
        else:
                bot.say("Please enter a proper term. ┐(-｡ｰ;)┌")
