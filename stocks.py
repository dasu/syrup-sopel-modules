import sopel
import json
import requests
from datetime import datetime

@sopel.module.commands('dji','stocks')
def stocks(bot,trigger):
    now = datetime.utcnow()
    nysestart = datetime.time(datetime(1904,1,1,13,30))
    nyseclose = datetime.time(datetime(1904,1,1,21,00))
    if not trigger.group(2):
        if (now.weekday() > 4) or now.time() <= nysestart or now.time() >= nyseclose:
            futures = requests.get("http://www.bloomberg.com/markets/api/quote-page/DM1:IND?local=en").json()
            futurespoints = str(futures['basicQuote']['priceChange1Day'])
            futurespercent = str(float("{0:.2f}".format(futures['basicQuote']['percentChange1Day'])))
            return bot.say("Dow Jones Index futures: {} ({}/{}) from {}".format(futures['basicQuote']['price'], "\x0304"+futurespoints+"\x0F" if float(futurespoints) < 0 else "\x0303+"+futurespoints+"\x0F", "\x0304"+futurespercent+"%\x0F" if float(futurespercent) < 0 else "\x0303+"+futurespercent+"%\x0F", futures['basicQuote']['previousClosingPriceOneTradingDayAgo']))
        else:
            x = requests.get("http://finance.google.com/finance/info?client=ig&q=.DJI")
    else:
        x = requests.get("http://finance.google.com/finance/info?client=ig&q={0}".format(trigger.group(2)))
    try:
        data = json.loads(x.text[6:-3])
    except:
        return bot.say("Doesn't exist.")
    if trigger.group(2):
        name = data['t']
    else:
        name = "Dow Jones Index"
    if not data['lt']:
        return bot.say("Doesn't exist.")
    start = data['pcls_fix']
    current = data['l_fix']
    change = data['c_fix']
    percent = data['cp_fix']
    if not data.get('ec_fix'):
        return bot.say("{0}: {1} ({2}/{3}) from {4}".format(name,current,"\x0304"+change+"\x0F" if float(change) < 0 else "\x0303+"+change+"\x0F","\x0304"+percent+"%\x0F" if float(percent) < 0 else "\x0303+"+percent+"%\x0F",start))
    afterhourschange = data['ec_fix']
    afterhourspercent = data['ecp_fix']
    afterhourscurrent = data['el_fix']
    bot.say("{0} after hours: {1} ({2}/{3}) from {4} ".format(name, afterhourscurrent, "\x0304"+afterhourschange+"\x0F" if float(afterhourschange) < 0 else "\x0303+"+afterhourschange+"\x0F","\x0304"+afterhourspercent+"%\x0F" if float(afterhourspercent) < 0 else "\x0303+"+afterhourspercent+"%\x0F",current))
    
