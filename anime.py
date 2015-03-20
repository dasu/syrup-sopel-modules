from urllib.request import urlopen
from bs4 import BeautifulSoup
import random
import re
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import time
import willie

def parse_dayname(i):
    days = {'sunday': 0,'monday': 1,'tuesday': 2,'wednesday': 3,'thursday': 4,'friday': 5,'saturday': 6}
    now = datetime.now(timezone('Asia/Tokyo'))
    today = days[now.strftime("%A").lower()]
    destday = days[i.lower()]
    if destday < today: destday = destday + 7
    days_between = destday - today
    return days_between

def GetInHMS(seconds):
    hours = seconds / 3600
    seconds -= 3600*hours
    minutes = seconds / 60
    seconds -= 60*minutes
    if hours == 0:
        return "%02d:%02d" % (minutes, seconds)
    return "%02d:%02d:%02d" % (hours, minutes, seconds)

def get_time_until(i):
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    jp = timezone('Asia/Tokyo')
    jt = datetime.now(timezone('Asia/Tokyo'))
    now_jst = jt.strftime(fmt)
    jp_lt = jp.localize(datetime.strptime(i,'%Y-%m-%d %H:%M:%S')) 
    days_remaining = (jp_lt-jt).days
    seconds_remaining = (jp_lt-jt).seconds
    if days_remaining < 0 or days_remaining == 6: 
        diff=datetime.strptime('23:59:59','%H:%M:%S')-datetime.strptime(GetInHMS(seconds_remaining),'%H:%M:%S')
        return 'Aired {0} ago'.format(diff)
    else:
        return ('{0} days {1}'.format(days_remaining, GetInHMS(seconds_remaining))).replace('1 days','1 day').replace('0 days ','')

@willie.module.commands('release')
def anime(bot, trigger):
    if not trigger.group(2):
        return bot.say("Enter Input can be: today, tomorrow, monday-sunday, or show name.")
    i = trigger.group(2)
    print(i)    
    days = []
    daynames = 'sunday monday tuesday wednesday thursday friday saturday'
    show_name = ''
    
    now = datetime.now(timezone('Asia/Tokyo'))
    curday = now.day - 1
    month = now.strftime("%m")
    year = now.year
    
    url = "http://www.animecalendar.net/{0}/{1}".format(year,month)
    
    try:
        urlopen(url)
        data = urlopen(url)
        soup = BeautifulSoup(data)
    except: 
        bot.say('Website is down.')
    days = soup.findAll('div',{"class":re.compile(r'^da.+')})

    if 29 - int(curday) < 7:
        days_nextmonth = []
        url = "http://www.animecalendar.net/{0}/{1}".format(year, int(month) + 1)
        try:
            urlopen(url)
            data = urlopen(url)
            soup = BeautifulSoup(data)
        except:
            bot.say('Website is down.')
        days_nextmonth = soup.findAll('div', {"class":re.compile(r'^da.+')})
        days = days + days_nextmonth

    if i.lower() in daynames \
    or i == 'today' \
    or i == 'tomorrow' \
    or i == 'yesterday':
        if i.lower() in daynames: curday = curday + parse_dayname(i)
        elif i == 'today': curday = curday
        elif i == 'tomorrow': curday = curday + 1
        elif i == 'yesterday': curday = curday -1
        show_date = days[curday].thead.h2.a['href'].replace('/','',1)
        result = ''
        res=[]
        res2=[]
        shows = days[curday].table.tbody.findAll('div',{'class': 'tooltip'})
        for show in shows:
            show_name = show.find('td', {'class': 'tooltip_title'}).h4.text.strip()
            show_time =  show.find('td', {'class': 'tooltip_info'}).h4.text.split(' on')[0].strip()
            air_time = show_time.split('at ')[1].split(' ')[0].strip() + ':00'
            air_date = show_date.replace('/','-')
            time_until = get_time_until('{0} {1}'.format(air_date, air_time))
            try:
                if len(', '.join(res)) > 400:
                    res2.append('{0}\x02{1}\x02: {2} [{3}]'.format(result, show_name, show_time, time_until))
                else:
                    res.append('{0}\x02{1}\x02: {2} [{3}]'.format(result, show_name, show_time, time_until))
            except:
                res2+='{0}\x02{1}\x02: {2} [{3}]'.format(result, show_name, show_time, time_until)
        if res2:
            bot.say(', '.join([str(x) for x in res]))
            bot.say(', '.join([str(x) for x in res2]))
        else:
            bot.say(', '.join([str(x) for x in res])) 
        return 'Sent!'
    else:
        while curday is not len(days):
            if days[curday].find(text=re.compile(".*"+i+".*", re.IGNORECASE)):
                show_date =  days[curday].thead.h2.a['href'].replace('/','',1)
                shows = days[curday].findAll('tr')
                for show in shows:
                    if show.find(text=re.compile(".*"+i+".*",re.IGNORECASE)):
                        show_name = show.find('td', {'class': 'tooltip_title'}).h4.text.strip()
                        show_time =  show.find('td', {'class': 'tooltip_info'}).h4.text.split(' on')[0].strip()
                        air_time = show_time.split('at ')[1].split(' ')[0].strip() + ':00'
                        air_date = show_date.replace('/','-')
                        time_until = get_time_until('{0} {1}'.format(air_date,air_time))
                        try:
                            bot.say('\x02{0}\x02: {1} on {2} [{3}]\n'.format(show_name.decode('utf-8'), show_time, show_date, time_until))
                        except:
                            bot.say('\x02{0}\x02: {1} on {2} [{3}]\n'.format(show_name, show_time, show_date, time_until))
                        return
            curday = curday + 1
