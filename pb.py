from pushbullet import Pushbullet
import sopel

@sopel.module.commands('pushbullet','pb')
def pushbullet(bot, trigger):
    if trigger.nick == 'NICK_GOES_HERE' or trigger.nick == 'NICK_GOES_HERE':
        url = trigger.group(2)
        pb = Pushbullet('API_KEY_GOES_HERE')
        pb.push_link(url,url)

@sopel.module.commands('pblast')
def pushbulletlast(bot,trigger):
    if trigger.group(2):
        return
    if trigger.nick == 'NICK_GOES_HERE' or trigger.nick == 'NICK_GOES_HERE':
        if trigger.sender not in bot.memory['last_seen_url']:
            return
        url = bot.memory['last_seen_url'][trigger.sender]
        pb = Pushbullet('API_KEY_GOES_HERE')
        pb.push_link(url,url)
