import requests
import sopel

@sopel.module.commands('mtg','magic')
def mtg(bot,trigger):
    if not trigger.group(2):
        return bot.say("Please enter a card name.")
    x = requests.get('https://api.magicthegathering.io/v1/cards?name={0}'.format(trigger.group(2))).json()
    if not x['cards']:
        return bot.say('Card not found.')
    js = x['cards'][0]
    if 'Creature' in js['types']:
        if 'power' in js:
            bot.say('{0} [{1}] {2}| {3} | {4}/{5}'.format(js['name'], js['type'], js.get('manaCost', ''), js.get('text',''), js['power'], js['toughness']))
        else:
            bot.say('{0} [{1}] {2}| {3}'.format(js['name'], js['type'], js.get('manaCost',''), js.get('text','')))
    else:
        bot.say('{0} [{1}] {2}| {3}'.format(js['name'], js['type'], js.get('manaCost', ''), js.get('text','')))
