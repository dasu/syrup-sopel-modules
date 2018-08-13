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

def getsteamappid(url):
    try:
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
        return current, _24h, alltime

def getreviewdata(appid):
    review = {}
    try:
        x = requests.get("https://store.steampowered.com/appreviews/{}?start_offset=0&day_range=30&start_date=-1&end_date=-1&date_range_type=all&filter=summary&language=english&l=english&review_type=all&purchase_type=all&review_beta_enabled=1".format(appid)).json()
        bs = BeautifulSoup(x['review_score'],"html.parser")
        review['reviewsummary'] = bs.findAll("span")[1].text
        review['reviewpercentage'] = bs.findAll("span")[1]['data-tooltip-text'].split('%')[0]+'%'
    except:
        review['reviewsummary'] = ''
        return review
    return review

@sopel.module.commands('steam')
def steam(bot,trigger):
    if trigger.group(2):
        url = "http://store.steampowered.com/search/?term={}".format(trigger.group(2))
        appid = getsteamappid(url)
        if not appid:
            return
        gameinfo = getgameinfo(appid)
        averageplayers = getaverageplayers24h(appid)
        rating = getreviewdata(appid)
        bot.say("[{0}]{1}{2}{3}{4}{5}".format(gameinfo['name'],
                                            " Rating: {} ({}) |".format(rating['reviewsummary'], rating['reviewpercentage']) if rating['reviewsummary'] else '',
                                            " Peak Players 24H: {} |".format(averageplayers) if averageplayers else '',
                                            " Price: {}{} |".format(gameinfo['price'], " (-{}%)".format(gameinfo['discount']) if gameinfo['discount'] else '') if gameinfo['price'] else '',
                                            " Coming soon: {}".format(gameinfo['release']) if gameinfo['release'] else '',
                                            " http://store.steampowered.com/app/{}/".format(appid)))

@sopel.module.rule('.*https?:\/\/store\.steampowered\.com\/app\/(.*?\/)(?:.*?\/)?(?:.*)((?=[\s])|$)')
def steamirc(bot,trigger, match=None):
    match = match or trigger
    appid = match.group(1)[:-1]
    gameinfo = getgameinfo(appid)
    averageplayers = getaverageplayers24h(appid)
    rating = getreviewdata(appid)
    bot.say("[{0}]{1}{2}{3}{4}".format(gameinfo['name'],
                                            " Rating: {} ({}) |".format(rating['reviewsummary'], rating['reviewpercentage']) if rating['reviewsummary'] else '',
                                            " Peak Players 24H: {} |".format(averageplayers) if averageplayers else '',
                                            " Price: {}{} |".format(gameinfo['price'], " (-{}%)".format(gameinfo['discount']) if gameinfo['discount'] else '') if gameinfo['price'] else '',
                                            " Coming soon: {}".format(gameinfo['release']) if gameinfo['release'] else ''))

@sopel.module.commands('steamp','players','steamchart')
def steamp(bot, trigger):
    if trigger.group(2):
        url = "http://store.steampowered.com/search/?term={}".format(trigger.group(2))
        appid = getsteamappid(url)
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
