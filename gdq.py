import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date, timezone
import sopel

def getinfo(run,now):
    schedule = run.find_all('tr',attrs={'class':None})
    game,runner,console,comment,eta,nextgame,nextrunner,nextconsole,nexteta,nextcomment = '','','','','','','','','',''
    for item in schedule:
        group = item.find_all('td')
        group2 = item.find_next_sibling().find_all('td')
        st = group[0].getText()
        #estfix = timedelta(hours=-5)
        starttime = datetime.strptime(st, '%Y-%m-%dT%H:%M:%SZ' )
        starttime = starttime.replace(tzinfo=timezone.utc)
        #starttime = starttime + estfix
        try:
            offset = datetime.strptime(group2[0].getText().strip(), "%H:%M:%S")
            endtime = starttime + timedelta(hours = offset.hour, minutes = offset.minute, seconds=offset.second)
        except:
            endtime = datetime(2011,1,1,12,00)
        if starttime < now and endtime > now:
            game = group[1].getText()
            runner = group[2].getText()
            #console = group[3].getText()
            comment = group2[1].getText()
            eta = group2[0].getText().strip()
        if starttime > now:
            nextgame = group[1].getText()
            nextrunner = group[2].getText()
            #nextconsole = group[3].getText()
            nexteta = group2[0].getText().strip()
            nextcomment = group2[1].getText()
            break
        else:
            nextgame = 'done'
            nextrunner = 'done'
    return (game, runner, console, comment, eta, nextgame, nextrunner, nexteta, nextconsole, nextcomment)
            

@sopel.module.commands('gdq','sgdq','agdq')
def gdq(bot, trigger):
    now = datetime.utcnow()
    now = now.replace(tzinfo=timezone.utc)
    delta = datetime(2016,7,3,16,30,tzinfo=timezone.utc) - now
    textdate = "July 3"
    url = 'https://gamesdonequick.com/schedule'
    try:
        x = requests.get(url).content
    except:
        return bot.say("GDQ is {0} days away ({1})".format(delta.days+round((delta.seconds/86400),2),textdate))
    bs = BeautifulSoup(x)
    run = bs.find("table",{"id":"runTable"}).tbody
    try:
        gdqstart = datetime.strptime(run.td.getText(), '%Y-%m-%dT%H:%M:%SZ')
        gdqstart = gdqstart.replace(tzinfo=timezone.utc)
    except:
        return bot.say("GDQ is {0} days away ({1})".format(delta.days+round((delta.seconds/86400),2), textdate))
    (game, runner, console, comment, eta, nextgame, nextrunner, nexteta, nextconsole, nextcomment) = getinfo(run,now)
    if now < gdqstart:
        tts = gdqstart - now
        if tts.days <= 3:
            return bot.say("GDQ is {0}H{1}M away.  First game: {2} by {3} ETA: {4} Comment: {5} | https://gamesdonequick.com/schedule".format(int(tts.total_seconds() // 3600),int((tts.total_seconds() % 3600) // 60), nextgame, nextrunner, nexteta, nextcomment))
        else:
            return bot.say("GDQ is {0} days away ({1}) | https://gamesdonequick.com/schedule".format(tts.days+round((tts.seconds/86400),2),gdqstart.strftime('%m/%d/%Y')))

    if nextgame == 'done':
        return bot.say("GDQ is {0} days away ({1} [estimated])".format(delta.days+round((delta.seconds/86400),2),textdate))
    if game:
        if comment:
            bot.say("Current Game: {0} by {1} ETA: {2} Comment: {3} | Next Game: {4} by {5} | http://www.twitch.tv/gamesdonequick | https://gamesdonequick.com/schedule".format(game, runner, eta, comment, nextgame, nextrunner))
        else:
            bot.say("Current Game: {0} by {1} ETA: {2} | Next Game: {3} by {4} | http://www.twitch.tv/gamesdonequick | https://gamesdonequick.com/schedule".format(game, runner, eta, nextgame, nextrunner))
    else:
        bot.say("Current Game: setup?? | Next Game {0} by {1} | http://www.twitch.tv/gamesdonequick | https://gamesdonequick.com/schedule".format(nextgame, nextrunner))
