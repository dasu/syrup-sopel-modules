import sopel
import datetime
import requests
import pytz
from pytz import timezone

@sopel.module.commands("wc")
def worldcup(bot, trigger):
  x = requests.get("http://api.football-data.org/v1/competitions/467/fixtures?timeFrame=n2").json()
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
      starth = str(round(((date - now).total_seconds()/60/60),1)) #hours
      #startm = int((date - now).total_seconds()/60) #minutes
      starta = '{}H away'.format(starth)
    if f['status'] == 'IN_PLAY':
      if f['result'].get('penalty'):
        score = "{} ({}) - {} ({})".format(f['result']['goalsHomeTeam'],f['result']['penalty']['goalsHomeTeam'],f['result']['goalsAwayTeam'],f['result']['penalty']['goalsAwayTeam'])
      else:
        score = "{} - {}".format(f['result']['goalsHomeTeam'],f['result']['goalsAwayTeam'])
      start = "LIVE"
    if f['status'] == 'FINISHED':
      if f['result'].get('penalty'):
        score = "{} ({}) - {} ({})".format(f['result']['goalsHomeTeam'],f['result']['penalty']['goalsHomeTeam'],f['result']['goalsAwayTeam'],f['result']['penalty']['goalsAwayTeam'])
      else:
        score = "{} - {}".format(f['result']['goalsHomeTeam'],f['result']['goalsAwayTeam'])
    games.append("{} [{}]{}".format(game,"{} | {}".format(start,starta) if starta else start, " {}".format(score) if score else ""))
  bot.say(", ".join(games))
