import sopel
import pymysql
import datetime
from urllib.parse import urlparse
from sopel.tools import Identifier
from bs4 import BeautifulSoup
import re
import soundcloud
from mutagen.easyid3 import EasyID3
import requests
import shutil
import random
import string
#import youtube_dl
import yt_dlp
from nicovideo import Nicovideo
import os
import sys
sys.stderr.isatty = lambda: False #to avoid youtube_dl errors with isatty()
#what a mess

def convert_date(date):
    """Parses an ISO 8601 datestamp and reformats it to be a bit nicer"""
    date = re.sub("\..*Z","Z", date)
    date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    return date.strftime('%Y-%m-%d %H:%M:%S UTC')

def convert_duration(duration):
    """Converts an ISO 8601 duration to a human-readable duration"""
    units = {
        'hour': 0,
        'minute': 0,
        'second': 0
    }
    for symbol, unit in zip(('H', 'M', 'S'), ('hour', 'minute', 'second')):
        match = re.search(r'(\d+)' + symbol, duration)
        if match:
            units[unit] = int(match.group(1))
    time = datetime.time(**units)
    output = str(time)
    match = re.search('(\d+)D', duration)
    if match:
        output = match.group(1) + ' days, ' + output
    return output

def fetch_yt_video_info(bot,id):
    url = "https://www.googleapis.com/youtube/v3/videos?key=API_KEY_GOES_HERE&part=contentDetails,status,snippet,statistics&id={0}".format(id)
    results = requests.get(url).json()
    video = results['items'][0]
    if video['snippet']['liveBroadcastContent'] == 'live':
        return None, None
    info = {
        'title': video['snippet']['title'],
        'uploader': video['snippet']['channelTitle'],
        'uploaded': convert_date(video['snippet']['publishedAt']),
        'duration': convert_duration(video['contentDetails']['duration']),
        'views': video['statistics'].get('viewCount') or '0',
        'comments': video['statistics'].get('commentCount') or '0',
        'likes': video['statistics'].get('likeCount') or '0',
        'dislikes': video['statistics'].get('dislikeCount') or '0',
        'link': 'https://youtu.be/' + video['id']
    }
    bksongname = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noprogress': True,
        'no_warnings': True,
        'max_filesize': 52428800, #50MB
        'outtmpl': '/path/to/songs/folder/{}'.format(bksongname+".%(ext)s"),
        'postprocessors':[{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        x = ydl.download(['http://www.youtube.com/watch?v={}'.format(id)])
    bksongname=bksongname+".mp3"
    return info, bksongname

def soundcloudinfo(link):
    client = soundcloud.Client(client_id='')
    track = client.get('/resolve', url = link, client_id='')
    stream = "https://api.soundcloud.com/i1/tracks/{}/streams?client_id={}".format(track.id,client.client_id)
    try:
        stream_url = requests.get(stream).json()['http_mp3_128_url']
        r = requests.get(stream_url)
        bksongname = ''.join(random.choice(string.ascii_lowercase) for i in range(10))+".mp3"
        with open('/path/to/songs/folder/{}'.format(bksongname), 'wb') as f:
            f.write(r.content)
    except:
        bksongname = ""
    return "{0} - {1}".format(track.user['username'],track.title),bksongname

def mysql(name=None, link=None, song=None, sdate=None, bksongname=None, action=None):
    connection = pymysql.connect(host='', user='',passwd='', db='',charset='utf8')
    cursor = connection.cursor()
    if action == 'insert':
        sql = "INSERT INTO sotd (name, link, song, sdate, dlname) VALUES(%s,%s,%s,%s,%s)"
        cursor.execute(sql, (name, link, song, sdate, bksongname))
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
        res = mysql(action='select')
        if trigger.group(2).strip() == res[2].strip():
            return bot.say("Duplicate, song not added!")
        match = re.match(r'[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}(youtube|youtu|sc0tt|soundcloud|bandcamp|nicovideo)\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)', trigger.group(2), re.I)
        if match:
            bksongname = ""
            name = Identifier(trigger.nick)
            link = match.group(0)
            domain = urlparse(link)
            if(domain.netloc == 'youtu.be' or domain.netloc == 'www.youtu.be'):
                yt,bksongname = fetch_yt_video_info(bot, domain.path[1:])
                if yt == None:
                    return bot.say("Please do not .sotd a live channel")
                song = yt['title']
                if not os.path.exists("/path/to/songs/folder/{}".format(bksongname)):
                    bksongname = ""
            elif(domain.netloc == 'youtube.com' or domain.netloc == 'www.youtube.com'):
                yt,bksongname = fetch_yt_video_info(bot, domain.query[2:])
                if yt == None:
                    return bot.say("Please do not .sotd a live channel")
                song = yt['title']
                if not os.path.exists("/home/desu/htdocs/sotd/songs/{}".format(bksongname)):
                    bksongname = ""
            elif(domain.netloc == 'soundcloud.com' or domain.netloc == 'www.soundcloud.com'):
                song,bksongname = soundcloudinfo(link)
            elif(domain.netloc == 'i.sc0tt.net'):
                bksongname = ''.join(random.choice(string.ascii_lowercase) for i in range(10))+".mp3"
                filename = "/path/to/songs/folder/{0}".format(bksongname)
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
            elif('bandcamp.com' in domain.netloc):
                try:
                    bs = BeautifulSoup(requests.get(link).content, "html.parser")
                    title = bs.findAll('h2', {"class":"trackTitle"})[0].text.strip()
                    artist = bs.findAll('meta', {"itemprop":"name"})[0].get('content')
                    song = "{0} - {1}".format(artist,title)
                except:
                    song = ""
            elif(domain.netloc == 'nicovideo.jp' or domain.netloc == 'www.nicovideo.jp'):
                id = domain.path[7:]
                nico = Nicovideo()
                nico.append(id)
                song = nico._video[id].title
            else:
                song = ""
            sdate = datetime.datetime.now()
            mysql(name, link, song, sdate, bksongname,'insert')
            return bot.say("Song saved.")
        else:
            return bot.say("Enter a valid link.")
    else:
        res = mysql(action='select')
        bot.say("Last SotD: {0} - {1}".format(res[2],res[3]))

@sopel.module.commands('sotdweb')
@sopel.module.commands('websotd')
def sotdweb(bot,trigger):
    bot.say("Website for history: weblink")
