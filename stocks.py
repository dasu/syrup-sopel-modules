import sopel
import requests

def symbol_lookup(symb):
    s = requests.get("https://query2.finance.yahoo.com/v1/finance/search?q={}&lang=en-US&region=US&quotesCount=3&newsCount=0".format(symb),headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36'}).json()
    if not s['quotes']:
        return None, None
    return s['quotes'][0]['shortname'], s['quotes'][0]['symbol']

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
    start = '{0:.2f}'.format(float(x.json()['pc']))
    if not start:
        return bot.say("Invalid stock?")
    current = '{0:.2f}'.format(float(x.json()['c']))
    change = '{0:.2f}'.format(float(current) - float(start))
    percent = '{0:.2f}'.format((float(change) / float(start))*100)
    return bot.say("{0}: {1} ({2}/{3}) from {4}".format(name,current,"\x0304"+change+"\x0F" if float(change) < 0 else "\x0303"+change+"\x0F","\x0304"+percent+"%\x0F" if float(percent) < 0 else "\x0303+"+percent+"%\x0F",start))
