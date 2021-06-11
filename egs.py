import requests
import sopel
import datetime

@sopel.module.commands('egs', 'egsfree')
def egs(bot, trigger):
  url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=US&allowCountries=US"
  res = requests.get(url).json()
  freenow = []
  upcomingfree = []
  for x in res['data']['Catalog']['searchStore']['elements']:
    if not x['promotions']:
      continue
    if x['promotions']['promotionalOffers']:
      freenow.append("{} [until {}]".format(x['title'], datetime.datetime.strptime(x['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['endDate'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%m/%d")))
    else:
      upcomingfree.append("{} [starts {}]".format(x['title'], datetime.datetime.strptime(x['promotions']['upcomingPromotionalOffers'][0]['promotionalOffers'][0]['startDate'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%m/%d")))

  bot.say("Free now: {} | Upcoming: {}".format(", ".join(freenow), ", ".join(upcomingfree)))
