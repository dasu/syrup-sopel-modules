import sopel
import json
import requests

@sopel.module.commands('dji','stocks')
def stocks(bot,trigger):
    if not trigger.group(2):
        x = requests.get("http://finance.google.com/finance/info?client=ig&q=.DJI")
    else:
        x = requests.get("http://finance.google.com/finance/info?client=ig&q={0}".format(trigger.group(2)))
    try:
        data = json.loads(x.text[6:-3])
    except:
        return bot.say("Doesn't exist.")
    if not data['lt']:
        return bot.say("Doesn't exist.")
    name = data['t']
    if not trigger.group(2):
        name = "Dow Jones Index"
    start = data['pcls_fix']
    current = data['l_fix']
    change = data['c_fix']
    percent = data['cp_fix']
    bot.say("{0}: {1} ({2}/{3}) from {4}".format(name,current,"\x0304"+change+"\x0F" if float(change) < 0 else "\x0303+"+change+"\x0F","\x0304"+percent+"%\x0F" if float(percent) < 0 else "\x0303+"+percent+"%\x0F",start))
