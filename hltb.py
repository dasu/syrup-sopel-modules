import requests
from bs4 import BeautifulSoup
import sopel


@sopel.module.commands('hltb','howlong','howlongtobeat')
@sopel.module.example('.hltb game name')
def hltb(bot,trigger):
    if not trigger.group(2):
        return bot.say("Enter a game name to search.")
    game = trigger.group(2)
    url = "http://howlongtobeat.com/search_main.php?page=1"
    payload = {"queryString":game,"t":"games","sorthead":"popular","sortd":"Normal Order","length_type":"main","detail":"0"}
    test = {'Content-type':'application/x-www-form-urlencoded', 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36','origin':'https://howlongtobeat.com','referer':'https://howlongtobeat.com'}
    session = requests.Session()
    session.post(url, headers=test, data=payload)
    r = session.post(url, headers=test, data=payload)
    if len(r.content) < 250:
        return bot.say("No results.")
    bs = BeautifulSoup(r.content)
    first = bs.findAll("div", {"class":"search_list_details"})[0]
    name = first.a.text
    time = first.findAll('div')[3].text
    bot.say('{} - {}'.format(name, time))
