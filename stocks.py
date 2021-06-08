import sopel
import requests

def symbol_lookup(symb):
    s = requests.get("http://d.yimg.com/aq/autoc?query={}&region=US&lang=en-US".format(symb)).json()
    if not s['ResultSet']['Result']:
        return None, None
    return s['ResultSet']['Result'][0]['name'], s['ResultSet']['Result'][0]['symbol']

@sopel.module.commands('stocks', 'stock')
def stocks(bot,trigger):
    if not trigger.group(2):
        x = requests.get("https://finnhub.io/api/v1/quote?symbol=^DJI&token=INSERT_TOKEN_HERE")
        name = "Dow Jones Index"
    else:
        name, symbol = symbol_lookup(trigger.group(2))
        if not name:
             return bot.say("No Results")
        x = requests.get("https://finnhub.io/api/v1/quote?symbol={}&token=INSERT_TOKEN_HERE".format((symbol).upper()))
    if x.json().get('Note'):
        return bot.say('Rate limit reached (30/min), try again in one minute')
    if x.json().get('Error Message'):
        return bot.say('Please enter a valid stock symbol')
    if x.json().get('error'):
        return bot.say(x.json()['error'])
    start = '{0:.2f}'.format(float(x.json()['o']))
    if not start:
        return bot.say("Invalid stock?")
    current = '{0:.2f}'.format(float(x.json()['c']))
    change = '{0:.2f}'.format(float(current) - float(start))
    percent = '{0:.2f}'.format((float(change) / float(start))*100)
    return bot.say("{0}: {1} ({2}/{3}) from {4}".format(name,current,"\x0304"+change+"\x0F" if float(change) < 0 else "\x0303"+change+"\x0F","\x0304"+percent+"%\x0F" if float(percent) < 0 else "\x0303+"+percent+"%\x0F",start))
