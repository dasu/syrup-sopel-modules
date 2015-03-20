import urllib
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
import willie

@willie.module.commands('gdq','sgdq','agdq')
def gdq(bot, trigger):
    url = 'https://gamesdonequick.com/schedule'
    req = urllib.request.Request(url,data=None,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
    try:
        x = urllib.request.urlopen(req)
    except:
        now = datetime.now()
        delta = datetime(2015,7,26,12,00) - now
        return bot.say("SGDQ is {0} days away (July 26)".format(delta.days))
    c = (x.read().decode('utf-8'))
    bs = BeautifulSoup(c)
    run = bs.find("tbody",{"id":"runTable"})
    schedule = run.find_all('tr')
    now = datetime.now()
    game = ''
    for item in schedule:
        group = item.find_all('td')
        st = group[0].getText()
        starttime = datetime.strptime(st, '%m/%d/%Y %H:%M:%S' )
        offset = datetime.strptime(group[4].getText(), "%H:%M:%S")
        endtime = starttime + timedelta(hours = offset.hour, minutes = offset.minute, seconds=offset.second)
        if starttime < now and endtime > now:
            game = group[1].getText()
            runner = group[2].getText()
            console = group[3].getText()
            comment = group[6].getText()
            eta = group[4].getText()
        if starttime > now:
            nextgame = group[1].getText()
            nextrunner = group[2].getText()
            break
        else:
            nextgame = 'done'
            game = ''
    if nextgame == 'done':
        delta = datetime(2015,7,26,12,00) - now
        return bot.say("SGDQ is {0} days away (July 26)".format(delta.days))
    if game:
        if comment:
            bot.say("Current Game: {0} [{1}] by {2} ETA: {3} Comment: {4} | Next Game: {5} by {6}".format(game, console, runner, eta, comment, nextgame, nextrunner))
        else:
            bot.say("Current Game: {0} [{1}] by {2} ETA: {3} | Next Game: {4} by {5}" % (game, console, runner, eta, nextgame, nextrunner))
    else:
        bot.say("Current Game: setup?? | Next Game {0} by {1}" % (nextgame, nextrunner))
