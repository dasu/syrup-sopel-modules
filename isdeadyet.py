#I'm actually MAGA but a retard in the channel wanted it so whatevz
import sopel
from bs4 import BeautifulSoup
import requests

@sopel.module.commands("istrumpdeadyet","istrump","itdy")
def istrumpdeadyet(bot,trigger):
    results = requests.get("http://istrumpdeadyet.com").content
    if results:
        bs = BeautifulSoup(results)
        bot.say(bs.h1.text)
