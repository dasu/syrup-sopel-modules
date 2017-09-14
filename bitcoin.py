# Flexible crypto currency module
# Created by @sc0tt (https://github.com/sc0tt)
import requests
import sys
import json
import sopel

last_prices = {}
main_coins = ["btc", "bch", "xrp", "eth"]
single_url = "https://api.bitfinex.com/v1/pubticker/{0}usd"
#multi_url = "http://api.cryptocoincharts.info/tradingPairs"

# @sopel.module.rule('^\.(\w+)2(\w+)\s?(.+)?$')
# def crypto_exchange(bot, trigger):
  # from_cur = trigger.group(1)
  # to_cur = trigger.group(2)
  # quantity = float(trigger.group(3)) if trigger.group(3) is not None else 1

  # api_result = requests.get(single_url.format(from_cur, to_cur)).json()
  # calc_result = quantity * float(api_result["price"])

  # bot.say("{0} {1} is about {2:.4f} {3}".format(quantity, api_result["coin1"], float(calc_result), api_result["coin2"]))

@sopel.module.rule('^\.({0})$'.format("|".join(main_coins)))
def crypto_spot(bot, trigger):
  from_cur = trigger.group(1)
  global last_prices
  from_cur = from_cur.lower()
  if from_cur not in main_coins:
    bot.say("Invalid currency!")

  api_result = requests.get(single_url.format(from_cur)).json()

  if from_cur not in last_prices:
    last_prices[from_cur] = 0

  diffStr = getDiffString(float(api_result["last_price"]), last_prices[from_cur])
  last_prices[from_cur] = float(api_result["last_price"])
  bot.say("{0}: ${1:.4f}{2}".format(from_cur, float(api_result["last_price"]), diffStr))

@sopel.module.commands('ticker','tick')
def tick(bot, trigger):
  global last_prices
  results = []
  for coin in main_coins:
    api_result = requests.get(single_url.format(coin)).json()
    if coin not in last_prices:
      last_prices[coin] = 0
    diffStr = getDiffString(float(api_result["last_price"]), last_prices[coin])
    last_prices[coin] = float(api_result["last_price"])
    results.append("{0}: ${1:.4f}{2}".format(coin, float(api_result["last_price"]), diffStr))
  bot.say(" | ".join(results))

def getDiffString(current_price, last_price, crates=False):
  diff = current_price - last_price
  diffStr = ""
  if diff != 0:
    sign = "+" if diff > 0 else ''
    diffStr = " ({0}{1:.{2}f})".format(sign, diff, 2 if crates else 4)
  return diffStr

def getSteamMarketPrice(item):
  global last_prices
  steam_price = requests.get("https://steamcommunity.com/market/priceoverview/?appid=578080&currency=1&market_hash_name={}".format(item)).json()
  name = item.replace(" CRATE","")
  name = name.replace(" INVITATIONAL","")
  lowest_price = steam_price['lowest_price']
  if name not in last_prices:
    last_prices[name] = '$0'
    last_price = '$0'
  last_price = last_prices[name]
  diffStr = getDiffString(float(lowest_price[1:]),float(last_price[1:]), True)
  last_prices[name] = lowest_price
  return "{0}: {1}{2}".format(name, lowest_price, diffStr)

@sopel.module.commands('crates')
def crates(bot, trigger):
  crates = ['SURVIVOR CRATE','WANDERER CRATE','GAMESCOM INVITATIONAL CRATE']
  results = []
  for crate in crates:
    results.append(getSteamMarketPrice(crate))
  bot.say(" | ".join(results))
