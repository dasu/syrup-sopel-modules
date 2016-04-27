#MAL anime module v0.80
#thanks agri for index error shit fix

import requests
from bs4 import BeautifulSoup
import sopel
import re
from sopel.tools import SopelMemory

malregex = re.compile('.*(https?:\/\/myanimelist.net\/anime\/(\d+)((?=[\s])|$))')

def setup(bot):
    if not bot.memory.contains('url_callbacks'):
        bot.memory['url_callbacks'] = SopelMemory()
    bot.memory['url_callbacks'][malregex] = malirc

def shutdown(bot):
    del bot.memory['url_callbacks'][malregex]

@sopel.module.rule('.*(https?:\/\/myanimelist.net\/anime\/(\d+)((?=[\s])|$))')
def malirc(bot, trigger, match=None):
    match = match or trigger
    id = match.group(2)
    url = 'http://myanimelist.net/includes/ajax.inc.php?t=64&id={}-id'.format(id)
    bs, x = connect(url)
    if bs.text == 'No such series found.':
        return
    if "... (" in (bs.find_all('a', {'class':'hovertitle'})[0].text):
        name =  bs.find_all('a', {'class':'hovertitle'})[0].text.split("...")[0].strip()
        year =  bs.find_all('a', {'class':'hovertitle'})[0].text.split("...")[1].strip()[1:-1]
    else:
        split = bs.find_all('a', {'class':'hovertitle'})[0].text.split(' (')
        name = split[0]
        year = split[1][0:-1]
    status = bs.findAll('span',text='Status:')[0].nextSibling.strip()
    episodes = bs.findAll('span',text='Episodes:')[0].nextSibling.strip()
    type = bs.findAll('span',text='Type:')[0].nextSibling.strip()
    genres = bs.findAll('span',text='Genres:')[0].nextSibling.strip()
    bot.say("{0} [{1}] - Type: {2} Eps: {3} Genres: {4} Status: {5}".format(name,year,type,episodes,genres,status))
    
def connect(url):
    headers = {'User-Agent':'API_KEY_GOES_HERE','Authorization':'AUTH_KEY_GOES_HERE'}
    x = requests.get(url,headers=headers).content
    bs = BeautifulSoup(x)
    return (bs, x)

@sopel.module.commands('mal')
def mal(bot,trigger):
    if not trigger.group(2):
        return bot.say("Enter an anime name you weeaboo.")
    i = trigger.group(2)
    if len(i)>1 and len(trigger.group())>5:
        d = 'http://myanimelist.net/api/anime/search.xml?q={0}'.format(i)
        bs, x = connect(d)
        if len(x) > 14:
            if bs.find('type').string == 'Movie':
                bot.reply('{0} ({2}): http://myanimelist.net/anime/{1}'.format(bs.find('title').string, bs.find('id').string, bs.find('type').string))
            else:
                bot.reply('{0} (eps:{2}) http://myanimelist.net/anime/{1}'.format(bs.find('title').string, bs.find('id').string, bs.find('episodes').string))
        else:
            bot.say("No results.")
    else:
        bot.say("No results.")

@sopel.module.commands('manga')
def manga(bot,trigger):
    if not trigger.group(2):
        return bot.say("Enter a mango name you weeaboo.")
    i = trigger.group(2)
    if len(i)>1 and len(trigger.group())>7:
        uri = 'http://myanimelist.net/api/manga/search.xml?q={0}'.format(i)
        bs, x = connect(uri)
        if len(x) > 14:
            bot.reply('{0} ({2}): http://myanimelist.net/manga/{1}'.format(bs.find('title').string, bs.find('id').string, bs.find('chapters').string))
        else:
            bot.say("No results.")
    else:
        bot.say("No results.")
        
@sopel.module.commands('people','va','seiyuu','malva')
def people(bot,trigger):
    if not trigger.group(2):
        return bot.say("Enter a name, retard")
    i = trigger.group(2)
    if len(i)>1 and len(trigger.group())>7:
        uri = 'http://myanimelist.net/people.php?q={0}'.format(i)
        bs, x = connect(uri)
        if len(x) > 14 and bs.body.findAll("table")[0].findAll("tr")[1].td.string != 'No results returned':
            if not bs.body.findAll(text='Search Results'):
                bot.say(bs.h1.string + ": http://myanimelist.net" + bs.findAll(id="horiznav_nav")[0].a['href'])
            else:
                bot.say(bs.body.findAll("table")[0].findAll("tr")[1].findAll("td")[1].a.string + ": http://myanimelist.net" + bs.body.findAll("table")[0].findAll("tr")[1].a['href'])
        else:
            bot.say("No results found.")
    else:
        bot.say("Please enter a proper term.")

@sopel.module.commands('character','malc')
def character(bot,trigger):
    if not trigger.group(2):
        return bot.say("Enter a name, retard")
    i = trigger.group(2)
    if len(i)>1 and len(trigger.group())>8:
        uri = 'http://myanimelist.net/character.php?q={0}'.format(i)
        bs, x = connect(uri)
        if len(x) > 14 and bs.body.findAll("table")[0].findAll("tr")[1].td.string != 'No results returned': #or 'No results found'
            if not bs.body.findAll(text='Search Results'):
                bot.say(bs.h1 + ": http://myanimelist.net" + bs.findAll(id="horiznav_nav")[0].a['href'])
            else:
                bot.say(bs.body.findAll("table")[0].findAll("tr")[1].findAll("td")[1].a.string + " from: " + bs.body.findAll("table")[0].findAll("tr")[1].findAll('td')[2].a.string)
        else:
            bot.say("No results found.")
    else:
        bot.say("Please enter a proper term.")
