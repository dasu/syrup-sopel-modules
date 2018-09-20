import sopel
import requests

def symbol_lookup(symb):
    s = requests.get("http://d.yimg.com/aq/autoc?query={}&region=US&lang=en-US".format(symb)).json()
    return s['ResultSet']['Result'][0]['name']

@sopel.module.commands('dji','stocks','stock')
def stocks(bot,trigger):
    if not trigger.group(2):
        x = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=^DJI&interval=1min&apikey=APIKEYGOESHERELOL")
    else:
        x = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&interval=1min&apikey=APIKEYGOESHERELOL".format(trigger.group(2)))
    if x.json().get('Information'):
        return bot.say('Rate limit reached (5/min), try again in one minute')
    if x.json().get('Error Message'):
        return bot.say('Please enter a valid stock symbol')
    if trigger.group(2):
        name = symbol_lookup(trigger.group(2))
    else:
        name = "Dow Jones Index"
    dates = sorted(x.json()['Time Series (Daily)'].keys(), reverse=True)
    start = '{0:.2f}'.format(float(x.json()['Time Series (Daily)'][dates[1]]['4. close']))
    current = '{0:.2f}'.format(float(x.json()['Time Series (Daily)'][dates[0]]['4. close']))
    change = '{0:.2f}'.format(float(current) - float(start))
    percent = '{0:.2f}'.format((float(change) / float(start))*100)
    return bot.say("{0}: {1} ({2}/{3}) from {4}".format(name,current,"\x0304"+change+"\x0F" if float(change) < 0 else "\x0303"+change+"\x0F","\x0304"+percent+"%\x0F" if float(percent) < 0 else "\x0303+"+percent+"%\x0F",start))
