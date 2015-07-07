#this is slow and can definitely be improved.

import willie
from pyvirtualdisplay import Display
from selenium import webdriver
import urllib.request
from bs4 import BeautifulSoup


@willie.module.commands('pixiv')
@willie.module.example('.pixiv word')
def pixiv(bot,trigger):
    display = Display(visible=0, size=(1024,768))
    display.start()
    browser = webdriver.Firefox()
    url = "http://www.pixiv.net/search.php?word="+urllib.request.quote(trigger.group(2))
    browser.get(url)
    bs = BeautifulSoup(browser.page_source)

    truesearch = bs.find("link", {"rel":"canonical"}).get('href')
    truesearchlink = 'http://www.pixiv.net/'+truesearch
    results = (bs.find("span",{ "class": "count-badge"}).text).replace("results","")
    bot.say("{0} results | {1}".format(results,truesearchlink))
