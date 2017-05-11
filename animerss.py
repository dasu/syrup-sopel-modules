import feedparser
import datetime
import time
import sopel
import urllib.request as urlrequest
import json

def get_short_url(gurl):
    short_url_service = 'https://www.googleapis.com/urlshortener/v1/url?key=API_KEY_GOES_HERE'
    long_url = json.dumps({'longUrl': gurl})
    request =  urlrequest.Request(short_url_service)
    request.add_header('Content-Type','application/json')
    opener = urlrequest.build_opener()
    output = opener.open(request,bytes(long_url,'UTF-8')).read()
    return json.loads(output.decode())['id']

def parse(now):
    new = []
    x = allnew = anew = ''
    url = 'http://www.animenewsnetwork.com/news/rss.xml'
    x = feedparser.parse(url)
    for items in x.entries:
        if now < items.published_parsed:
            if items.title == 'Daily Briefs' in items.title or 'Ranking' in items.title or 'New York Times' in items.title or 'Boruto' in items.title or 'Naruto' in items.title:
                continue
            else:
                rssurl = get_short_url(items.link)
                anew = "{0} {1}".format(items.title,rssurl)
                new.append(anew)
    if new:
        allnew = " | ".join(new)
        return allnew
        
#@sopel.module.commands('startrss','rssstart')
@sopel.module.event('JOIN')
@sopel.module.rule('.*')
def rss(bot, trigger):
    if sopel.tools.Identifier(trigger.sender) == "#pancakes" and trigger.nick == bot.nick:
        time.sleep(5)
        bot.say("Starting RSS.")
        now = time.gmtime()
        time.sleep(3600)
        while True:
            time.sleep(7200)
            quietnow = datetime.datetime.utcnow().time()
            out = parse(now)
            if out:
                if quietnow >= datetime.time(3,00) or quietnow <= datetime.time(11,00):
                    pass
                else:
                    bot.say(out)
            now = time.gmtime()
