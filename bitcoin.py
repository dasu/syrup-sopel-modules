import json
import decimal
import requests
import sopel

lastPrice = 0
lastLTCPrice = 0
lastDogePrice = 0
lastETHPrice = 0

def calcdoge2usd(num):
   uri = "http://api.cryptocoincharts.info/tradingPair/doge_btc"
   data = requests.get(uri).json()
   return calcbtc2usd(decimal.Decimal(num) * decimal.Decimal(data["price"]))

@sopel.module.commands('doge2usd')
def doge2usd(bot, trigger):
   arg = trigger.group(2)
   #If an argument is provided, convert the exchange rate
   if arg:
      rate = calcdoge2usd(arg)
      usd = decimal.Decimal(arg)
      output = '%s DOGE will get you $%s' % (usd, rate)
      bot.say(output)

@sopel.module.commands('doge')
def dogecoin(bot, trigger):
   global lastDogePrice
   uri = "http://api.cryptocoincharts.info/tradingPair/doge_btc"   
   data = requests.get(uri).json()
   data["price"] = calcbtc2usd(data["price"])
   diff = decimal.Decimal(data["price"]) - lastDogePrice
   diffStr = ""
   if diff != decimal.Decimal(0):
      sign = "+" if diff > 0 else ''
      diffStr = " (%s%s)" % (sign, diff)
   output = 'Current Price of 1 DOGE: $%s%s' % (data["price"], diffStr)
   lastDogePrice = decimal.Decimal(data["price"])
   bot.say(output)


def calcbtc2usd(num):
   uri = "https://coinbase.com/api/v1/currencies/exchange_rates"
   data = requests.get(uri).json()
   return decimal.Decimal(num) * decimal.Decimal(data["btc_to_usd"])

def calcusd2btc(num):
   uri = "https://coinbase.com/api/v1/currencies/exchange_rates"
   data = requests.get(uri).json()
   return decimal.Decimal(num) * decimal.Decimal(data["usd_to_btc"])

@sopel.module.commands('btc')
def bitcoin(bot, trigger):
   global lastPrice
   uri = "https://coinbase.com/api/v1/prices/spot_rate"
   data = requests.get(uri).json()
   diff = decimal.Decimal(data["amount"]) - lastPrice
   diffStr = ""
   if diff != decimal.Decimal(0):
      sign = "+" if diff > 0 else ''
      diffStr = " (%s%s)" % (sign, diff)
   output = 'Current Price of ฿1: $%s%s' % (data["amount"], diffStr)
   lastPrice = decimal.Decimal(data["amount"])
   bot.say(output)

   
@sopel.module.commands('btc2usd')
def btc2usd(bot, trigger):
   arg = trigger.group(2)
   #If an argument is provided, convert the exchange rate
   if arg:
      rate = calcbtc2usd(arg)
      usd = decimal.Decimal(arg)
      output = '฿%s will get you $%s' % (usd, rate)
      bot.say(output)

@sopel.module.commands('usd2btc')
def usd2btc(bot, trigger):
   arg = trigger.group(2)
   #If an argument is provided, convert the exchange rate
   if arg:
      rate = calcusd2btc(arg)
      usd = decimal.Decimal(arg)
      output = '$%s will get you ฿%s' % (usd, rate)
      bot.say(output)

def calcltc2usd(num):
   uri = "https://btc-e.com/api/3/ticker/ltc_usd"
   data = requests.get(uri).json()
   return decimal.Decimal(num) * decimal.Decimal(data["ltc_usd"]["last"])

def calcusd2ltc(num):
   uri = "https://btc-e.com/api/3/ticker/ltc_usd"
   data = requests.get(uri).json()
   usdPerLtc = decimal.Decimal("1.0") / decimal.Decimal(data["ltc_usd"]["last"])
   return decimal.Decimal(num) * usdPerLtc

def calceth2usd(num):
   uri = "https://btc-e.com/api/3/ticker/eth_usd"
   data = requests.get(uri).json()
   return decimal.Decimal(num) * decimal.Decimal(data["eth_usd"]["last"])

def calcusd2eth(num):
   uri = "https://btc-e.com/api/3/ticker/eth_usd"
   data = requests.get(uri).json()
   usdPerEth = decimal.Decimal("1.0") / decimal.Decimal(data["eth_usd"]["last"])
   return decimal.Decimal(num) * usdPerEth

   
@sopel.module.commands('ltc')
def litecoin(bot, trigger):
   global lastLTCPrice
   uri = "https://btc-e.com/api/3/ticker/ltc_usd"
   data = requests.get(uri).json()
   diff = decimal.Decimal(data["ltc_usd"]["last"]) - lastLTCPrice
   diffStr = ""
   if diff != decimal.Decimal(0):
      sign = "+" if diff > 0 else ''
      diffStr = " (%s%0.5f)" % (sign, diff)
   output = 'Current Price of Ł1: $%0.5f%s' % (data["ltc_usd"]["last"], diffStr)
   lastLTCPrice = decimal.Decimal(data["ltc_usd"]["last"])
   bot.say(output)

@sopel.module.commands('ltc2usd')
def ltc2usd(bot, trigger):
   arg = trigger.group(2)
   #If an argument is provided, convert the exchange rate
   if arg:
      rate = calcltc2usd(arg)
      usd = decimal.Decimal(arg)
      output = 'Ł%s will get you $%.05f' % (usd, rate)
      bot.say(output)

@sopel.module.commands('usd2ltc')
def usd2ltc(bot, trigger):
   arg = trigger.group(2)
   #If an argument is provided, convert the exchange rate
   if arg:
      rate = calcusd2ltc(arg)
      usd = decimal.Decimal(arg)
      output = '$%s will get you Ł%.05f' % (usd, rate)
      bot.say(output)
      
@sopel.module.commands('eth')
def ETH(bot, trigger):
   global lastETHPrice
   uri = "https://btc-e.com/api/3/ticker/eth_usd"
   data = requests.get(uri).json()
   diff = decimal.Decimal(data["eth_usd"]["last"]) - lastETHPrice
   diffStr = ""
   if diff != decimal.Decimal(0):
      sign = "+" if diff > 0 else ''
      diffStr = " (%s%0.5f)" % (sign, diff)
   output = 'Current Price of Ξ1: $%0.5f%s' % (data["eth_usd"]["last"], diffStr)
   lastETHPrice = decimal.Decimal(data["eth_usd"]["last"])
   bot.say(output)

@sopel.module.commands('eth2usd')
def eth2usd(bot, trigger):
   arg = trigger.group(2)
   #If an argument is provided, convert the exchange rate
   if arg:
      rate = calceth2usd(arg)
      usd = decimal.Decimal(arg)
      output = 'Ξ%s will get you $%.05f' % (usd, rate)
      bot.say(output)

@sopel.module.commands('usd2eth')
def usd2eth(bot, trigger):
   arg = trigger.group(2)
   #If an argument is provided, convert the exchange rate
   if arg:
      rate = calcusd2eth(arg)
      usd = decimal.Decimal(arg)
      output = '$%s will get you Ξ%.05f' % (usd, rate)
      bot.say(output)

@sopel.module.commands('ticker','tick')
def ticker(bot, trigger):
   bitcoin(bot, trigger)
   litecoin(bot, trigger)
   dogecoin(bot, trigger)
   ETH(bot,trigger)
