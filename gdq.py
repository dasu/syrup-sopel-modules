#I have no clue if this will work come JAN 1st...
import sopel
import requests
import json
from datetime import datetime, timedelta, date

def getinfo(gdqlist,now):
    game,runner,category,comment,eta,nextgame,nextrunner,nextcategory,nexteta,nextcomment = '','','','','','','','','',''
    for item in gdqlist:
        starttime = item[1]
        offset = datetime.strptime(item[4], "%H:%M:%S")
        endtime = starttime + timedelta(hours = offset.hour, minutes = offset.minute, seconds=offset.second)
        if starttime < now and endtime > now:
            game = item[0]
            category = item[2]
            runner = item[3]
            eta = item[4]
            comment = item[6]
        if starttime > now:
            nextgame = item[0]
            nextrunner = item[3]
            nextcategory = item[2]
            nexteta = item[4]
            nextcomment = item[6]
            break
        else:
            nextgame = 'done'
            nextrunner = 'done'
    return(game, runner, category, comment, eta, nextgame, nextrunner, nexteta, nextcategory, nextcomment)

@sopel.module.commands('gdq','sgdq','agdq')
def gdq(bot,trigger):
    gdqlist = []
    row = ""
    dati, game, runners, time, category, estimate, setup, comment = '','','','','','','',''
    url ='https://spreadsheets.google.com/feeds/cells/1_gibuPSqCLOY8HruYJ15OYGGkFfth0IevIi7fE9Xp2E/1/public/values?prettyprint=true&alt=json'
    r = requests.get(url).json()

    year = datetime.today().year+1 if datetime.today().month is 12 else datetime.today().year
    now = datetime.now()
    for cell in r['feed']['entry']:
        if cell['gs$cell']['col'] == '1':
            if cell['gs$cell']['$t']:
                try:
                    datetime.strptime(cell['gs$cell']['$t'], '%A %m/%d')
                    date = cell['gs$cell']['$t']
                except:
                    pass
        if cell['gs$cell']['col'] == '2':
            if row<cell['gs$cell']['row']:
                row
                if (game != 'Game') and (game != ''):
                    gdqlist+=[[game, dati, category, runners, estimate, setup, comment]]
            row = cell['gs$cell']['row']
            game, runners, time, category, estimate, setup, comment = '','','','','','',''
            try:
                time = cell['gs$cell']['$t']
                dati = datetime.strptime("{} {}, {}".format(date, year, time), "%A %m/%d %Y, %I:%M %p" )
            except:
                pass
        if cell['gs$cell']['col'] == '3':
            game = cell['gs$cell']['$t']
        if cell['gs$cell']['col'] == '4':
            runners = cell['gs$cell']['$t']
        if cell['gs$cell']['col'] == '5':
            category = cell['gs$cell']['$t']
        if cell['gs$cell']['col'] == '6':
            estimate = cell['gs$cell']['$t']
        if cell['gs$cell']['col'] == '7':
            setup = cell['gs$cell']['$t']
        if cell['gs$cell']['col'] == '8':
            if cell['gs$cell']['$t']:
                comment = cell['gs$cell']['$t']
    (game, runner, category, comment, eta, nextgame, nextrunner, nexteta, nextcategory, nextcomment) = getinfo(gdqlist, now)
    if now < gdqlist[0][1]:
        tts = gdqlist[0][1] - now
        if tts.days <= 3:
            return bot.say("GDQ is {0} hours away. First game: {1} [{2}] by {3} ETA: {4} ".format(int(tts.total_seconds() // 3600),nextgame, nextcategory, nextrunner, nexteta))
        else:
            return bot.say("GDQ is {0} days away ({1})".format(tts.days, gdqlist[0][1].strftime('%m/%d/%Y')))


    if nextgame == 'done':
        delta = datetime(2016,6,15,12,00) - now
        return bot.say("GDQ is {0} days away (June 15)".format(delta.days))
    if game:
        if comment:
            bot.say("Current Game: {0} [{1}] by {2} ETA: {3} Comment: {4} | Next Game: {5} by {6}".format(game, category, runner, eta, comment, nextgame, nextrunner))
        else:
            bot.say("Current Game: {0} [{1}] by {2} ETA: {3} | Next Game: {4} by {5}".format(game, category, runner, eta, nextgame, nextrunner))
    else:
        bot.say("Current Game: setup?? | Next Game {0} by {1}".format(nextgame, nextrunner))
