import sopel
import json
import requests
from datetime import datetime, date

def symbol_lookup(symb):
    s = requests.get("http://d.yimg.com/aq/autoc?query={}&region=US&lang=en-US".format(symb)).json()
    return s['ResultSet']['Result'][0]['name']

@sopel.module.commands('dji','stocks')
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
            x = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=^DJI&interval=1min&apikey=APIKEYGOESHERELOL")
    else:
        x = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&interval=1min&apikey=APIKEYGOESHERELOL".format(trigger.group(2)))
    if trigger.group(2):
        name = symbol_lookup(trigger.group(2))
    else:
        name = "Dow Jones Index"
    today = date.today()
    start = '{0:.2f}'.format(float(x.json()['Time Series (Daily)'][(today.strftime("%Y-%m-%d"))]['1. open']))
    current = '{0:.2f}'.format(float(x.json()['Time Series (Daily)'][(today.strftime("%Y-%m-%d"))]['4. close']))
    change = '{0:.2f}'.format(float(current) - float(start))
    percent = '{0:.2f}'.format((float(change) / float(start))*100)
    return bot.say("{0}: {1} ({2}/{3}) from {4}".format(name,current,"\x0304"+change+"\x0F" if float(change) < 0 else "\x0303"+change+"\x0F","\x0304"+percent+"%\x0F" if float(percent) < 0 else "\x0303+"+percent+"%\x0F",start))

@sopel.module.commands('futures')
def futures(bot,trigger):
    futures = requests.get("http://www.bloomberg.com/markets/api/quote-page/DM1:IND?local=en").json()
    futurespoints = str(futures['basicQuote']['priceChange1Day'])
    futurespercent = str(float("{0:.2f}".format(futures['basicQuote']['percentChange1Day'])))
    return bot.say("Dow Jones Index futures: {} ({}/{}) from {}".format(futures['basicQuote']['price'], "\x0304"+futurespoints+"\x0F" if float(futurespoints) < 0 else "\x0303+"+futurespoints+"\x0F", "\x0304"+futurespercent+"%\x0F" if float(futurespercent) < 0 else "\x0303+"+futurespercent+"%\x0F", futures['basicQuote']['previousClosingPriceOneTradingDayAgo']))
