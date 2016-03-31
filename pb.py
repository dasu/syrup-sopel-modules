from pushbullet import Pushbullet
import sopel

@sopel.module.commands('pushbullet','pb')
def pushbullet(bot, trigger):
    if trigger.nick == 'NICK_GOES_HERE' or trigger.nick == 'NICK_GOES_HERE':
        url = trigger.group(2)
        pb = Pushbullet('API_KEY_GOES_HERE')
        pb.push_link(url,url)
