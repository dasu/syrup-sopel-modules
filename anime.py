import sopel
import requests
from datetime import datetime, timedelta
from pytz import timezone
import re

def secondstohours(s):
  hours = s / 60 / 60
  return round(hours)

def parsedayname(n):
  if n == 7: n = 0
  days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
  return days[n]

@sopel.module.commands('release')
def anime(bot, trigger):
  days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
  f = trigger.group(2).lower()
  if not trigger.group(2):
    f = 'today'
  now = datetime.now(timezone('Asia/Tokyo')).weekday()
  if f == 'today': i = parsedayname(now)
  elif f == 'tomorrow': i = parsedayname(now + 1)
  elif f == 'yesterday': i = parsedayname(now - 1)
  else:
    i = f

  now = datetime.now(tz=timezone('Asia/Tokyo'))
  c = requests.get('http://anichart.net/airing')

  token = c.headers['Set-Cookie'].split(';')[0].split('=')[1]
  yum = c.headers['Set-Cookie'].split(';')[3].split(', ')[1]
  yum+=';XSRF-TOKEN={}'.format(token)
  headers = {'X-CSRF-TOKEN':token, 'Cookie':yum}

  x = requests.get('http://anichart.net/api/airing', headers=headers).json()
  res = []
  if i in days:
    for b in x[i]:
      name = b['title_romaji']
      episode = b['airing']['next_episode']
      countdown = (datetime.fromtimestamp(b['airing']['time'], tz=timezone('Asia/Tokyo')) - now)
      #airdatetime = datetime.fromtimestamp(b['airing']['time'],tz=timezone('Asia/Tokyo'))
      res.append("\x02{}\x02 Ep.{} [{}d{}h]".format(name, episode, countdown.days, secondstohours(countdown.seconds)))
    return bot.say(', '.join(res))
  else:
    for d in x:
      for b in x[d]:
        if re.search(re.compile(i,re.IGNORECASE),b['title_romaji']):
          name = b['title_romaji']
          episode = b['airing']['next_episode']
          countdown = (datetime.fromtimestamp(b['airing']['time'], tz=timezone('Asia/Tokyo')) - now)
          res.append("\x02{}\x02 Ep.{} [{}d{}h]".format(name, episode, countdown.days, secondstohours(countdown.seconds)))
    return bot.say(', '.join(res))
