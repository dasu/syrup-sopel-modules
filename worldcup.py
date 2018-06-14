#this is currently in progress

import sopel
import datetime
import requests
import pytz
from pytz import timezone

@sopel.module.commands("wc")
def worldcup(bot, trigger):
  x = requests.get("http://api.football-data.org/v1/competitions/467/fixtures?timeFrame=n1").json()
  now = datetime.datetime.utcnow()
  est = timezone('US/Eastern')
  games = []
  for f in x['fixtures']:
    game = "{} vs {}".format(f['homeTeamName'], f['awayTeamName'])
    date = datetime.datetime.strptime(f['date'],"%Y-%m-%dT%H:%M:%SZ")
    date2 = (pytz.utc.localize(date)).astimezone(est)
    start = date2.strftime("%m/%d %H:%MEST")
    score = None
    starta = None
    if f['status'] == 'TIMED':
      starth = int((date - now).total_seconds()/60/60) #hours
      startm = int((date - now).total_seconds()/60) #minutes
      starta = '{}H{}M away'.format(starth,startm)
    if f['status'] == 'IN_PLAY':
      score = "{} - {}".format(f['result']['goalsHomeTeam'],f['result']['goalsAwayTeam'])
      start = "LIVE"
    games.append("{} [{}]{}".format(game,"{} | {}".format(start,starta) if starta else start, " {}".format(score) if score else ""))

  bot.say(", ".join(games))
