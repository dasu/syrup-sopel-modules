import requests
import willie


def lookup(word, api_key):
  payload = {'api_key': '', 'limit': 1}
  try:
    response = requests.get("http://api.wordnik.com:80/v4/word.json/{0}/definitions".format(word.lower(), params=payload)).json()
    return response[0]['text']
  except:
    return None

@willie.module.commands('define')
def define(bot, trigger):
  word = trigger.group(2)
  if not word:
    bot.say("-- .define <word>")
  else:
    definition = lookup(word, '')
    if definition is None:
      bot.say("Word not found!")
    else:
      bot.say("{0}: {1}".format(word, definition))

@willie.module.commands('wotd')
def wotd(bot, trigger):
  payload = {'api_key': ''}
  response = requests.get("http://api.wordnik.com:80/v4/words.json/wordOfTheDay", params=payload).json()
  definition = lookup(response['word'], '')
  bot.say("Word of the day: {0} - {1}".format(response['word'], definition))

@willie.module.commands('rword')
def rword(bot, trigger):
  payload = {'api_key': '',
             'hasDictionaryDef': 'true' }
  response = requests.get("http://api.wordnik.com:80/v4/words.json/randomWord", params=payload).json()
  definition = lookup(response['word'], '')
  bot.say("Random word: {0} - {1}".format(response['word'], definition))
