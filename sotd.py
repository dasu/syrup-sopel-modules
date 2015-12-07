import sopel
import pymysql
import datetime
from urllib.parse import urlparse
from sopel.tools import Identifier
import re
from youtoob import fetch_video_info 
#youtoob is this module slightly renamed: https://github.com/ridelore/willie-modules/blob/master/youtube.py
import soundcloud
from mutagen.easyid3 import EasyID3
import requests
import shutil
import random
import string
#what a mess


def soundcloudtitle(link):
    client = soundcloud.Client(client_id='clientidgoeshere')
    track = client.get('/resolve', url = link, client_id='clientidgoeshere')
    return "{0} - {1}".format(track.user['username'],track.title)


def mysql(name=None, link=None, song=None, sdate=None, action=None):
    connection = pymysql.connect(host='', user='',passwd='', db='',charset='utf8')
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



@sopel.module.commands('sotd')
@sopel.module.example('.sotd weblink | website for history: weblink')
def sotd(bot, trigger):
    if(trigger.group(2)):
        match = re.match(r'[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}(youtube|sc0tt|pomf|soundcloud)\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)', trigger.group(2), re.I)
        if match:
            name = Identifier(trigger.nick)
            link = match.group(0)
            domain = urlparse(link)
            if(domain.netloc == 'youtu.be' or domain.netloc == 'www.youtu.be'):
                yt = fetch_video_info(bot, domain.path[1:])
                song = yt['title']
            elif(domain.netloc == 'youtube.com' or domain.netloc == 'www.youtube.com'):
                yt = fetch_video_info(bot, domain.query[2:])
                song = yt['title']
            elif(domain.netloc == 'soundcloud.com' or domain.netloc == 'www.soundcloud.com'):
                song = soundcloudtitle(link)
                elif(domain.netloc == 'i.sc0tt.net'):
                filename = "/tmp/{0}".format(''.join(random.choice(string.ascii_lowercase) for i in range(10))+".mp3")
                response = requests.head(link)
                if (int(response.headers['Content-Length']) < 26214400):
                    try:
                        r = requests.get(link,stream=True)
                        with open(filename,'wb') as x:
                            shutil.copyfileobj(r.raw, x)
                        a = EasyID3(filename)
                        song = a['artist'][0]+" - "+a['title'][0]
                    except:
                        song = ""
                else:
                    song = ""
            else:    
                song = ""
            sdate = datetime.datetime.now()
            mysql(name, link, song, sdate,'insert')
            return bot.say("Song saved.")
        else:
            return bot.say("Enter a valid link.")
    else:
        res = mysql(action='select')
        bot.say("Last SotD: {0}".format(res[2]))

@sopel.module.commands('sotdweb')
@sopel.module.commands('websotd')
def(bot,trigger):
    bot.say("Website for history: website1 OR website2")
