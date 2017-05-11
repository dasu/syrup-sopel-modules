from pyvirtualdisplay import Display
import sopel
from selenium import webdriver
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup

def setup(bot):
    display = Display(visible =0, size=(1024,768))
    bot.memory["pixdisplay"] = display.start()
    browser = webdriver.Firefox()
    bot.memory["pixbrowser"] = browser


@sopel.module.commands('pixiven','pixen')
@sopel.module.example('.pixiven word')
def pixiven(bot,trigger):
    #display = Display(visible=0, size=(1024,768))
    #display.start()
    #browser = webdriver.Firefox()
    url = "http://www.pixiv.net/search.php?word="+urllib.request.quote(trigger.group(2))
    bot.memory["pixbrowser"].get(url)
    bs = BeautifulSoup(bot.memory["pixbrowser"].page_source)

    truesearch = bs.find("link", {"rel":"canonical"}).get('href')
    truesearchlink = 'http://www.pixiv.net/'+truesearch
    results = (bs.find("span",{ "class": "count-badge"}).text).replace("results","")
    bot.say("{0} results | {1}".format(results,truesearchlink))
    #bot.memory["pixbrowser"].close()

@sopel.module.commands('pixiv','pix')
def pixiv(bot,trigger):
    url = "http://www.pixiv.net/search.php?word="+urllib.request.quote(trigger.group(2))
    x = urlopen(url).read()
    bs = BeautifulSoup(x)
    truesearch = bs.find("link", {"rel":"canonical"}).get('href')
    truesearchlink = 'http://www.pixiv.net/'+truesearch
    results = (bs.find("span", { "class": "count-badge"}).text).replace("results","")
    bot.say("{0} results | {1}".format(results,truesearchlink))
