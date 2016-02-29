from datetime import datetime
import json
import willie

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
    with open('/home/desu/phenny-master/modules/data.txt', 'w') as bdayfile:
        json.dump(dict, bdayfile, default=date_handler)

def readjson():
    with open('/home/desu/phenny-master/modules/data.txt','r') as bdayfile:
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
    dict = readjson()
    name = trigger.nick
    #bot.say(trigger.group(1))
    try:
        date = datetime.strptime(trigger.group(1), '%m-%d')
    except:
        bot.say("Please enter a valid date.  Accepts MONTH-DAY only.")
        return
    dict[name] = date
    #bot.say(name+str(date))
    writejson(dict)    
    bot.say("Birthday saved.")
#setbday.rule = r'^.setbday (\d{1,2}-\d{1,2})$'


@willie.module.commands('bday','birthday')
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
