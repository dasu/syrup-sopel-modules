import sopel
from sopel.tools import SopelMemory
import re
import requests
from bs4 import BeautifulSoup

steamregex = re.compile('.*https?:\/\/store\.steampowered\.com\/app\/(.*?\/)(?:.*?\/)?(?:.*)((?=[\s])|$)')
def setup(bot):
    if not bot.memory.contains('url_callbacks'):
        bot.memory['url_callbacks'] = SopelMemory()
    bot.memory['url_callbacks'][steamregex] = steamirc

def shutdown(bot):
    del bot.memory['url_callbacks'][steamregex]

def altsteamsearch(query):
    b = requests.get('https://duckduckgo.com/html', {'k1':'us-en', 'q':'steam charts {}'.format(query)}, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'}).text
    r_duck = re.compile(r'nofollow" class="[^"]+" href="(?!(?:https?:\/\/r\.search\.yahoo)|(?:https?:\/\/duckduckgo\.com\/y\.js)(?:\/l\/\?kh=-1&amp;uddg=))(.*?)">')
    r_appid = re.compile(r'.*https?:\/\/steamcharts\.com\/app\/(.*?$)')
    if 'web-result' in b:
        b = b.split('web-result')[1]
    m = r_duck.search(b)
    if m:
        appid = r_appid.search(m.group(1))
        if not appid:
            return None
    else:
        return None
    return appid.group(1)
    
def getsteamappid(game):
    try:
        url = "https://store.steampowered.com/search/suggest?term={}&f=games&cc=US&l=english&v=5208404".format(game)
        bs = BeautifulSoup(requests.get(url).content, "html.parser")
        appid = bs.find_all('a', {'class':'match ds_collapse_flag '})[0]['data-ds-appid']
    except:
        try:
            url = "http://store.steampowered.com/search/?term={}".format(game)
            bs = BeautifulSoup(requests.get(url).content, "html.parser")
            appid = bs.find_all('a', {'class':'search_result_row'})[0]['data-ds-appid']
        except:
            appid = None
    return appid

def getgameinfo(appid):
    gameinfo = {}
    x = requests.get("http://store.steampowered.com/api/appdetails?appids={}&cc=US".format(appid)).json()
    gameinfo['name'] = x[appid]['data']['name']
    if x[appid]['data']['is_free']:
        gameinfo['price'] = 'Free To Play'
        gameinfo['discount'] = ''
    else:
        if x[appid]['data'].get('price_overview', False):
            gameinfo['price'] = "$"+str(x[appid]['data']['price_overview']['final']/100)
            if x[appid]['data']['price_overview']['discount_percent'] > 0:
                gameinfo['discount'] = x[appid]['data']['price_overview']['discount_percent']
            else:
                gameinfo['discount'] = ''
        else:
            gameinfo['price'] = ''
            gameinfo['discount'] = ''
    if x[appid]['data']['release_date']['coming_soon']:
        gameinfo['release'] = x[appid]['data']['release_date']['date']
    else:
        gameinfo['release'] = ''
    return gameinfo
    
def getaverageplayers24h(appid, full=False):
    try:
        bs = BeautifulSoup(requests.get("http://steamcharts.com/app/{}".format(appid)).content, "html.parser")
        _24h = bs.find_all('div',{'class':'app-stat'})[1].span.text
        if full:
            current = bs.find_all('div',{'class':'app-stat'})[0].span.text
            alltime = bs.find_all('div',{'class':'app-stat'})[2].span.text
    except:
        return ''
    if not full:
        if _24h == '0':
            _24 = ''
        return "{:,}".format(int(_24h)) if _24h else ''
    else:
        return "{:,}".format(int(current)), "{:,}".format(int(_24h)), "{:,}".format(int(alltime))

def getreviewdata(appid):
    review = {}
    try:
        x = requests.get("https://store.steampowered.com/appreviews/{}?start_offset=0&day_range=30&start_date=-1&end_date=-1&date_range_type=all&filter=summary&language=english&l=english&review_type=all&purchase_type=all&review_beta_enabled=1".format(appid)).json()
        bs = BeautifulSoup(x['review_score'],"html.parser")
        review['reviewsummary'] = bs.findAll("span")[1].text
        review['reviewpercentage'] = bs.findAll("span")[1]['data-tooltip-html'].split('%')[0]+'%'
    except:
        review['reviewsummary'] = ''
        return review
    return review

def getlowestprice(appid):
    try:
        url = 'https://steamdb.info/api/GetPriceHistory/?appid={}&cc=us'.format(appid)
        x = requests.get(url, headers={'referer': 'https://steamdb.info/app/{}/'.format(appid),'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36'})
        data = x.json()['data']
        low = list(reversed(data['final']))[list(reversed([i[1] for i in data['final']])).index(min([i[1] for i in data['final']]))]  #lol
        #low = sorted([x for x in data["final"] if x[1] == sorted(data["final"], key=lambda item: item[1])[0][1]], key=lambda other_item: other_item[0], reverse=True)[0]   #ALTERNATIVE BY sc00ty
        lowestdate = datetime.fromtimestamp(low[0]/1000)
        lowestprice = data['formatted'][str(low[0])]['final']
        lowestdiscount = "{}%".format(data['formatted'][str(low[0])]['discount'])
    except:
        return '','',''
    return lowestdate, lowestprice, lowestdiscount

@sopel.module.commands('steam')
def steam(bot,trigger):
    if trigger.group(2):
        appid = getsteamappid(trigger.group(2))
        if not appid:
            return
        gameinfo = getgameinfo(appid)
        averageplayers = getaverageplayers24h(appid)
        rating = getreviewdata(appid)
        lowestdate, lowestprice, lowestdiscount = getlowestprice(appid)
        bot.say("[{0}]{1}{2}{3}{4}{5}{6}".format(gameinfo['name'],
                                            " Rating: {} ({}) |".format(rating['reviewsummary'], rating['reviewpercentage']) if rating['reviewsummary'] else '',
                                            " Peak Players 24H: {} |".format(averageplayers) if averageplayers else '',
                                            " Price: {}{} |".format(gameinfo['price'], " (-{}%)".format(gameinfo['discount']) if gameinfo['discount'] else '') if gameinfo['price'] else '',
                                            " Coming soon: {} |".format(gameinfo['release']) if gameinfo['release'] else '',
                                            " Lowest Price: {} (-{}) on {} |".format(lowestprice, lowestdiscount, lowestdate.strftime("%m-%Y")) if lowestprice else '',
                                            " http://store.steampowered.com/app/{}/".format(appid)))

@sopel.module.rule('.*https?:\/\/store\.steampowered\.com\/app\/(.*?\/)(?:.*?\/)?(?:.*)((?=[\s])|$)')
def steamirc(bot,trigger, match=None):
    match = match or trigger
    appid = match.group(1)[:-1]
    gameinfo = getgameinfo(appid)
    averageplayers = getaverageplayers24h(appid)
    rating = getreviewdata(appid)
    lowestdate, lowestprice, lowestdiscount = getlowestprice(appid)
    bot.say("[{0}]{1}{2}{3}{4}{5}".format(gameinfo['name'],
                                            " Rating: {} ({}) |".format(rating['reviewsummary'], rating['reviewpercentage']) if rating['reviewsummary'] else '',
                                            " Peak Players 24H: {} |".format(averageplayers) if averageplayers else '',
                                            " Price: {}{} |".format(gameinfo['price'], " (-{}%)".format(gameinfo['discount']) if gameinfo['discount'] else '') if gameinfo['price'] else '',
                                            " Lowest Price: {} (-{}) on {} ".format(lowestprice, lowestdiscount, lowestdate.strftime("%m-%Y")) if lowestprice else '',
                                            " Coming soon: {} ".format(gameinfo['release']) if gameinfo['release'] else ''))

@sopel.module.commands('steamp','players','steamchart')
def steamp(bot, trigger):
    if trigger.group(2):
        appid = getsteamappid(trigger.group(2))
        if not appid:
            return
        gameinfo = getgameinfo(appid)
        try:
            current, _24h, alltime = getaverageplayers24h(appid, True)
        except:
            return bot.say("Not a valid video game.")
        if not current:
            return
        bot.say("[{}] Current: {} | 24h: {} | All-Time: {}".format(gameinfo['name'], current, _24h, alltime))

@sopel.module.commands('altsteam', 'steamalt')
def altsteam(bot, trigger):
  if trigger.group(2):
    appid = altsteamsearch(trigger.group(2))
    if appid == None:
      return
    gameinfo = getgameinfo(appid)
    averageplayers = getaverageplayers24h(appid)
    rating = getreviewdata(appid)
    lowestdate, lowestprice, lowestdiscount = getlowestprice(appid)
    bot.say("[{0}]{1}{2}{3}{4}{5}{6}".format(gameinfo['name'],
                                        " Rating: {} ({}) |".format(rating['reviewsummary'], rating['reviewpercentage']) if rating['reviewsummary'] else '',
                                        " Peak Players 24H: {} |".format(averageplayers) if averageplayers else '',
                                        " Price: {}{} |".format(gameinfo['price'], " (-{}%)".format(gameinfo['discount']) if gameinfo['discount'] else '') if gameinfo['price'] else '',
                                        " Lowest Price: {} (-{}) on {} |".format(lowestprice, lowestdiscount, lowestdate.strftime("%m-%Y")) if lowestprice else '',
                                        " Coming soon: {} |".format(gameinfo['release']) if gameinfo['release'] else '',
                                        " http://store.steampowered.com/app/{}/".format(appid)))

@sopel.module.commands('altplayers', 'playersalt')
def altplayers(bot, trigger):
  if trigger.group(2):
    appid = altsteamsearch(trigger.group(2))
    if appid == None:
      return
    gameinfo = getgameinfo(appid)
    try:
      current, _24h, alltime = getaverageplayers24h(appid, True)
    except:
      return bot.say("Not a valid video game.")
    if not current:
      return
    bot.say("[{}] Current: {} | 24h: {} | All-Time: {}".format(gameinfo['name'], current, _24h, alltime))

@sopel.module.commands('steamsale', 'sale', 'nextsale')
def steamsale(bot, trigger):
    x = requests.get("https://whenisthenextsteamsale.com")
    bs = BeautifulSoup(x.content, "html.parser")
    res = json.loads(bs.find(id="hdnNextSale").get('value'))
    if res:
        bot.say("Next Steam Sale: {} [{}] | {}-{} (In {})".format(res['Name'],
                                                                  "Confirmed" if res['IsConfirmed'] else "Unconfirmed",
                                                                  datetime.strptime(res['StartDate'], '%Y-%m-%dT%H:%M:%S').strftime("%m/%d"),
                                                                  datetime.strptime(res['EndDate'],
                                                                  '%Y-%m-%dT%H:%M:%S').strftime("%m/%d"),
                                                                  res['RemainingTime'].split('.')[0] + ' days' if len(res['RemainingTime'].split('.')) == 3 else res['RemainingTime'].split('.')[0].split(':')[0] + ' hours'))
    else:
        bot.say("No known upcoming steam sale.")
