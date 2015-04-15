import willie
import pymysql
import datetime
from willie.tools import Identifier
import re


def mysql(name=None, link=None, song=None, sdate=None, action=None):
    connection = pymysql.connect(host='', user='',passwd='', db='')
    cursor = connection.cursor()
    if action == 'insert':
        sql = "INSERT INTO sotd (name, link, song, sdate) VALUES(%s,%s,%s,%s)"
        cursor.execute(sql, (name, link, song, sdate))
        connection.commit()

    if action == 'select':
        sql = "SELECT * FROM sotd order by id desc limit 0,1"
        cursor.execute(sql)
        res = cursor.fetchone()
        connection.close()
        return res
    connection.close()



@willie.module.commands('sotd')
@willie.module.example('.sotd weblink | website for history: weblink')
def sotd(bot, trigger):
    if(trigger.group(2)):
        match = re.match(r'[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)', trigger.group(2), re.I)
        if match:
            name = Identifier(trigger.nick)
            link = match.group(0)
            song = ""
            sdate = datetime.datetime.now()
            mysql(name, link, song, sdate,'insert')
            return bot.say("Song saved.")
        else:
            return bot.say("Enter a valid link.")
    else:
        res = mysql(action='select')
        bot.say("Last SotD: {0}".format(res[2]))
