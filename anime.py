import sopel
import requests
from datetime import datetime, timedelta
from pytz import timezone
import re

def secondstocountdown(s):
  days = int(s/86400)
  hours = int(abs((s - (days * 86400))/60/60))
  return "{}{}d{}h".format("-" if s < 0 else "", days, hours)

def aniquery(weekstart, weekend, page):
  variable = {"weekStart":weekstart,"weekEnd":weekend,"page":page}
  query = """
    query ($weekStart: Int, $weekEnd: Int, $page: Int) {
      Page(page: $page) {
        pageInfo {
          hasNextPage
          total
        }
        airingSchedules(airingAt_greater: $weekStart, airingAt_lesser: $weekEnd) {
          episode
          airingAt
          media {
            title {
              romaji
              native
              english
            }
            isAdult
            startDate {
              year
              month
              day
            }
            endDate {
              year
              month
              day
            }
            status
            season
            format
            synonyms
            duration
          }
        }
      }
    }
  """
  x = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variable})
  return x.json()

@sopel.module.commands('release')
def anime(bot, trigger):
  days = {'monday':0, 'tuesday':1, 'wednesday':2, 'thursday':3, 'friday': 4, 'saturday':5, 'sunday': 6}
  try:
    f = trigger.group(2).lower()
  except:
    pass
  if not trigger.group(2):
    f = 'today'
  nowweekday = datetime.now(timezone('Asia/Tokyo')).weekday()
  if f == 'today': weekday = nowweekday
  elif f == 'tomorrow': weekday = 0 if (nowweekday+1) == 7 else (nowweekday+1)
  elif f == 'yesterday': weekday = 6 if (nowweekday-1) == -1 else (nowweekday-1)
  else:
    try:
      weekday = days[f]
    except:
      weekday = nowweekday

  now = datetime.now(tz=timezone('Asia/Tokyo'))
  weekstart = int(datetime.timestamp((now - timedelta(days=1)).replace(hour=5,minute=0,second=0, microsecond=0)))
  weekend = int(datetime.timestamp((now - timedelta(days=1)).replace(hour=5,minute=0,second=0, microsecond=0) + timedelta(days=7)))

  z = []
  nextpage = True
  page = 1
  while nextpage:
    req = aniquery(weekstart, weekend, page)
    page+=1
    nextpage = req['data']['Page']['pageInfo']['hasNextPage']
    z.extend(req['data']['Page']['airingSchedules'])
  z = [x for x in z if ((x['media']['isAdult'] == False) and (x['media']['format'] == 'TV' or x['media']['format'] == 'TV_SHORT') and (x['episode'] < 100))]

  res = []
  res2 = []
  if (f == 'today' or f == 'yesterday' or f == 'tomorrow' or f in days):
    for n in z:
      if (datetime.fromtimestamp(n['airingAt'], tz=timezone('Asia/Tokyo'))).weekday() != weekday: continue
      name = n['media']['title']['romaji']
      episode = n['episode']
      countdown = (datetime.fromtimestamp(n['airingAt'], tz=timezone('Asia/Tokyo'))-now)
      if len(', '.join(res)) > 375:
        res2.append("\x02{}\x02 Ep.{} [{}]".format(name, episode, secondstocountdown(countdown.total_seconds())))
      else:
        res.append("\x02{}\x02 Ep.{} [{}]".format(name, episode, secondstocountdown(countdown.total_seconds())))
    if res2:
      bot.say(', '.join(res))
      return bot.say(', '.join(res2))
    else:
      return bot.say(', '.join(res))
  else:
    for n in z:
      if(re.search(re.compile(f, re.IGNORECASE),", ".join([", ".join(n['media']['synonyms'] or ''), n['media']['title']['native'] or '', n['media']['title']['english'] or '', n['media']['title']['romaji' or '']]))):
        name = n['media']['title']['romaji']
        episode = n['episode']
        countdown = (datetime.fromtimestamp(n['airingAt'], tz=timezone('Asia/Tokyo')) - now)
        if len(', '.join(res)) > 375:
          res2.append("\x02{}\x02 Ep.{} [{}]".format(name, episode, secondstocountdown(countdown.total_seconds())))
        else:
          res.append("\x02{}\x02 Ep.{} [{}]".format(name, episode, secondstocountdown(countdown.total_seconds())))
    if res2:
      bot.say(', '.join(res))
      return bot.say(', '.join(res2))
    else:
      return bot.say(', '.join(res))
