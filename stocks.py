import sopel
import json
import requests
from datetime import datetime, date

@sopel.module.commands('dji','stocks','stock')
def stocks(bot,trigger):
    now = datetime.now()
    nysestart = datetime.time(datetime(1904,1,1,9,45))
    nyseclose = datetime.time(datetime(1904,1,1,16,00))
    if not trigger.group(2):
        if (now.weekday() > 4) or now.time() <= nysestart or now.time() >= nyseclose:
            futures = requests.get("http://www.bloomberg.com/markets/api/quote-page/DM1:IND?local=en").json()
            futurespoints = str(futures['basicQuote']['priceChange1Day'])
            futurespercent = str(float("{0:.2f}".format(futures['basicQuote']['percentChange1Day'])))
            return bot.say("Dow Jones Index futures: {} ({}/{}) from {}".format(futures['basicQuote']['price'], "\x0304"+futurespoints+"\x0F" if float(futurespoints) < 0 else "\x0303+"+futurespoints+"\x0F", "\x0304"+futurespercent+"%\x0F" if float(futurespercent) < 0 else "\x0303+"+futurespercent+"%\x0F", futures['basicQuote']['previousClosingPriceOneTradingDayAgo']))
        else:
            x = requests.get("https://www.bloomberg.com/markets/api/quote-page/INDU:IND")
    else:
        x = requests.get("https://www.bloomberg.com/markets/api/quote-page/{}:US".format(trigger.group(2)))
    if x.json()['securityType'] == 'UNKNOWN':
        return bot.say("Please enter a valid stock symbol.")
    if trigger.group(2):
        name = x.json()['basicQuote']['name']
    else:
        name = "Dow Jones Index"
    start = x.json()['basicQuote']['openPrice']
    current = x.json()['basicQuote']['price']
    change = x.json()['basicQuote']['priceChange1Day']
    percent = "{0:.2f}".format(x.json()['basicQuote']['percentChange1Day'])
    return bot.say("{0}: {1} ({2}/{3}) from {4}".format(name,current,"\x0304"+str(change)+"\x0F" if change < 0 else "\x0303"+str(change)+"\x0F","\x0304"+percent+"%\x0F" if change < 0 else "\x0303+"+percent+"%\x0F",start))

@sopel.module.commands('futures')
def futures(bot,trigger):
    futures = requests.get("http://www.bloomberg.com/markets/api/quote-page/DM1:IND?local=en").json()
    futurespoints = str(futures['basicQuote']['priceChange1Day'])
    futurespercent = str(float("{0:.2f}".format(futures['basicQuote']['percentChange1Day'])))
    return bot.say("Dow Jones Index futures: {} ({}/{}) from {}".format(futures['basicQuote']['price'], "\x0304"+futurespoints+"\x0F" if float(futurespoints) < 0 else "\x0303+"+futurespoints+"\x0F", "\x0304"+futurespercent+"%\x0F" if float(futurespercent) < 0 else "\x0303+"+futurespercent+"%\x0F", futures['basicQuote']['previousClosingPriceOneTradingDayAgo']))
