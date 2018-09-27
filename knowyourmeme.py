import requests
from bs4 import BeautifulSoup
import sopel

@sopel.module.commands("kym")
def kym(bot, trigger):
    x = requests.get("http://knowyourmeme.com/search?q={}".format(trigger.group(2)),headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36'})
    bs = BeautifulSoup(x.content,'html.parser')
    try:
        url2 = bs.findAll("tbody")[0].tr.td.a['href']
    except:
        return bot.say("No results.")
    x2 = requests.get("https://knowyourmeme.com{}".format(url2), headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36'})
    bs2 = BeautifulSoup(x2.content,'html.parser')
    about = bs2.find('meta', attrs={"property": "og:description"})['content']
    uri = bs2.find('meta', attrs={"property": "og:url"})['content']
    title = bs2.find('meta', attrs={"property": "og:title"})['content']
    bot.say("{}: {} | {}".format(title, about[0:385], uri))
