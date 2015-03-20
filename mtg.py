#card name, card type, mana cost, card effect, power +
#toughness if the card type is a creature
from urllib.request import urlopen
import json
import willie

@willie.module.commands('mtg','magic')
def mtg(bot,trigger):
    if not trigger.group(2):
        return bot.say("Please enter a card name.")
    i = trigger.group(2)
    x = urlopen('http://api.mtgdb.info/search/{0}'.format(i))
    c = x.read()
    js = json.loads(c.decode('utf-8'))[0]
    if js['type'] == 'Creature':
        bot.say('Name: {0}, Type: {1}, Cost: {2}, Effect: {3}, Power: {4}, Toughness: {5}'.format(js['name'], js['type'], js['manaCost'], js['description'], js['power'], js['toughness']))
    else:
        bot.say('Name: {0}, Type: {1}, Cost: {2}, Effect: "{3}"'.format(js['name'], js['type'], js['manaCost'], js['description']))
