#in progress
import sopel
import pymysql
import requests
import datetime
from sopel.tools import Identifier


def mysql(date,name,content,eventdate,cametrue,action):
    connection = pymysql.connect(host='',user='',passwd='',db='',charset='utf8')
    cursor = connection.cursor()
    if action == 'insert':
        sql = "INSERT INTO ssthis (date1, name, content, eventdate, cametrue) VALUES(%s,%s,%s,%s,%s)"
        cursor.execute(sql, (date, name, content, eventdate, cametrue))
        connection.commit()

    if action == 'select':
        sql = "SELECT * FROM ssthis ORDER BY id desc LIMIT 0,1"
        cursor.execute(sql)
        res = cursor.fetchone()
        connection.close()
        return res
    connection.close()

def processdate(content):
    res = requests.get("https://api.wit.ai/message?v=20171003&q={}".format(requests.utils.quote(content)), headers = {'Authorization':'API_KEY_GOES_HERE'}).json()
    try:
        x = res['entities']['datetime'][0]['value']
    except:
        try:
            x = res['entities']['datetime'][0]['to']['value']
        except:
            return None
    return x

@sopel.module.commands('ssthis', 'ss')
def ssthis(bot,trigger):
    if(trigger.group(2)):
        date = datetime.datetime.now()
        name = Identifier(trigger.nick)
        content = trigger.group(2)
        eventdate = processdate(content)
        if eventdate:
            eventdate = datetime.datetime.strptime(eventdate.split('.')[0],"%Y-%m-%dT%H:%M:%S")
        else:
            return bot.say("Couldn't parse date...")
        cametrue = None
        mysql(date,name,content,eventdate,cametrue, 'insert')
        bot.say("ss'd")
    else:
        bot.say("Make a prediction nerd, requires a date the prediction will happen.  Site: site.to/database.lol ")
