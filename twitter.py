import requests
from bs4 import BeautifulSoup
import sopel
import re

twitterregex = re.compile(".*(https?:\/\/twitter\.com\/(?:#!\/)?(\w+)\/status(es)?\/(\d+))")
xregex = re.compile(".*(https?:\/\/x\.com\/(?:#!\/)?(\w+)\/status(es)?\/(\d+))")

def setup(bot):
  if not bot.memory.contains('url_callbacks'):
    bot.memory['url_callbacks'] = SopelMemory()
  bot.memory['url_callbacks'][twitterregex] = twatterirc
  bot.memory['url_callbacks'][xregex] = xirc

@sopel.module.rule(".*(https?:\/\/twitter\.com\/(?:#!\/)?(\w+)\/status(es)?\/(\d+))")
def twatterirc(bot,trigger):
  url = "https://publish.twitter.com/oembed?url={}".format(trigger.group(1))
  x = requests.get(url)
  user = x.json()['author_name']
  bs = BeautifulSoup(x.json()['html'], "html.parser")
  for a_tag in bs.find_all('a'):
    if((a_tag.text.startswith("#")) or (a_tag.text.startswith("@"))):
      continue
    a_tag.string = a_tag.get('href')
  bot.say("[Twitter] {}: {}".format(user, bs.p.text))


@sopel.module.rule(".*(https?:\/\/x\.com\/(?:#!\/)?(\w+)\/status(es)?\/(\d+))")
def xirc(bot,trigger):
  url = "https://publish.x.com/oembed?url={}".format(trigger.group(1))
  x = requests.get(url)
  user = x.json()['author_name']
  bs = BeautifulSoup(x.json()['html'], "html.parser")
  for a_tag in bs.find_all('a'):
    if((a_tag.text.startswith("#")) or (a_tag.text.startswith("@"))):
      continue
    a_tag.string = a_tag.get('href')
  bot.say("[X] {}: {}".format(user, bs.p.text))
