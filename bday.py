from datetime import datetime
import json
import sopel

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

def date_hook(json_dict):
    for(key, value) in json_dict.items():
        try:
            json_dict[key] = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
        except:
            pass
    return json_dict

def writejson(dict):
    with open('/home/desu/.sopel/data.txt', 'w') as bdayfile:
        json.dump(dict, bdayfile, default=date_handler)

def readjson():
    with open('/home/desu/.sopel/data.txt','r') as bdayfile:
        dict = json.loads(bdayfile.read(), object_hook=date_hook)
    return dict

def datetonext(dict):
    res = []
    today = datetime.today()
    for x,y in dict.items():
        delta = y.replace(year=(datetime.today().year)) - today
        if delta.total_seconds() < 0:
            delta = y.replace(year=(datetime.today().year+1)) - today
        res.append([x,delta])
    res.sort(key=lambda x: x[1])
    return res

def setbday(bot, trigger):
    #disabled function
    dict = readjson()
    name = trigger.nick
    try:
        date = datetime.strptime(trigger.group(1), '%m-%d')
    except:
        return bot.say("Please enter a valid date.  Accepts MONTH-DAY only.")
    dict[name] = date
    writejson(dict)
    bot.say("Birthday saved.")
#setbday.rule = r'^.setbday (\d{1,2}-\d{1,2})$'


@sopel.module.commands('bday','birthday')
def nextbday(bot, trigger):
    dict = readjson()
    res = datetonext(dict)
    if trigger.group(2):
        user = (trigger.group(2)).lower()
        try:
            bot.say("{0}'s birthday is on {1}".format(user, dict[user].strftime("%B %d")))
        except:
            bot.say("Name not found...")
    else:
        btoday = 0
        for c in dict.items():
            if c[1].date() == datetime.today().replace(year=1904).date():
                btoday = "Today is {0} birthday!".format(c[0])
        nname=res[0][0]
        nbday=(dict[nname]).strftime('%B %d')
        daysaway=(res[0][1]).days + 1
        if btoday:
            bot.say("{0} - Next birthday: {1} on {2} ({3} days away)".format(btoday, nname, nbday, daysaway))
        else:
            bot.say("Next birthday: {0} on {1} ({2} days away)".format(nname, nbday, daysaway))


@sopel.module.interval(21600)
def announce_bday(bot):
    announce = []
    dict = readjson()
    res = datetonext(dict)
    for people in res:
        if people[1].days == 0:
            announce.append(people[0])
    if announce:
        bot.say("Happy Birthday {0}!".format(", ".join(announce)))
