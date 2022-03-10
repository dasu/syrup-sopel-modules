import requests
import sopel

@sopel.module.commands('ygo','yugioh')
def ygo(bot,trigger):
    if not trigger.group(2):
        return bot.say("Please enter a card name.")
    x = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php?fname={0}'.format(trigger.group(2))).json()
    if x.get('error',''):
        return bot.say('Card not found.')
    js = x['data'][0]
    if 'Monster' in js['type']:
        if 'Link' in js['type']:
            bot.say('{0} [{1}/{2}/{3}] LINK-{4} | {6} | {5}'.format(js['name'], js['race'], js['type'].replace(' Monster', ''), js['attribute'], js['linkval'], js.get('desc','').replace("\n", ' '), js['atk']), max_messages=3)
        elif 'Pendulum' in js['type']:
            bot.say('{0} [{1}/{2}/{3}] L{4} {5}/{6} {7}/{8} | {9}'.format(js['name'], js['race'], js['type'].replace(' Monster', ''), js.get('attribute',''), js['level'], js['atk'], js['def'], js['scale'], js['scale'], js.get('desc','').replace("\n", ' ')), max_messages=3)
        else:
            bot.say('{0} [{1}/{2}/{3}] L{4} | {5}/{6} | {7}'.format(js['name'], js['race'], js['type'].replace(' Monster', ''), js['attribute'], js['level'], js['atk'], js['def'], js.get('desc','').replace("\n", ' ')), max_messages=3)
    else:
        bot.say('{0} [{1} - {2}] | {3}'.format(js['name'], js['type'], js['race'], js.get('desc','').replace("\n", ' ')),max_messages=3)

@sopel.module.commands('ygoart')
def ygoart(bot,trigger):
    if not trigger.group(2):
        return bot.say("Please enter a card name.")
    x = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php?fname={0}'.format(trigger.group(2))).json()
    if x.get('error',''):
        return bot.say('Card not found.')
    js = x['data'][0]
    bot.say('{0}: {1}'.format(js['name'],js['card_images'][0]['image_url']))
