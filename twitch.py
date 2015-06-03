#twitchtv module with hitbox support customized for #pancakes
#todo announce when someone starts streaming?
#version 1.2.3
import willie
import json
from urllib.request import urlopen
from urllib.error import HTTPError

@willie.module.commands('twitchtv','tv','twitch')
@willie.module.example('.tv  or .tv twitchusername')
def twitch(bot,trigger):
    if not trigger.group(2):
        v = []
        uri = 'https://api.twitch.tv/kraken/streams?channel=coalll,chouxe,kwlpp,dasusp,lurkk,agriks,repppie,squidgay,supersocks,sc00ty,kaask,mole_star,twoiis'
        #uri2 = 'kwlpp','agriks','coal','chouxe','socks'
        bytes = urlopen(uri).read()
        m = json.loads(bytes.decode())
        for stream in m['streams']:
            x = stream['channel']['name']
            y = stream['channel']['url']
            w = stream['viewers']
            status = stream['channel']['status']
            #z = x + " (" + y + " Viewers:" + w + ")"
            z = "{0} ({1} Title:{2} Viewers: {3})".format(x,y,status,w)
            v.append(z)
        #for name in uri2:
        #    uri3 = 'http://api.hitbox.tv/media/live/{0}'.format(name)
        #    bytes2 = web.get(uri3)
        #    c = json.loads(bytes2)
        #    if c['livestream'][0]['media_is_live'] == '1':
        #        x2 = c['livestream'][0]['media_user_name']
        #        y2 = c['livestream'][0]['channel']['channel_link']
        #        z2 = x2 + " (" + y2 + ")"
        #        v.append(z2)
        if v == []:
            return bot.say('No one is currently streaming.')

        else:
            return bot.say('Currently streaming: {0}'.format(", ".join(v)))

    else:
        i = trigger.group(2)
        uri = 'https://api.twitch.tv/kraken/streams/{0}'.format(i)
        try:
            bytes = urlopen(uri).read()
        except (HTTPError, IOError, ValueError):
            return bot.say('{0} does not exist.'.format(i))
        m = json.loads(bytes.decode())
        try:
            if format(m['stream']) == 'None':
                return bot.say('{0} is currently not streaming.'.format(i))
            else:
                return bot.say('{0} is streaming {1}: {2} (Title: {3}, {4} Viewers)'.format(i, m['stream']['game'], m['stream']['channel']['url'],m['stream']['channe$
        except (HTTPError, IOError, ValueError, KeyError):
            return bot.say("Invalid Username.")

            
@willie.module.commands('htv','hitbox')
@willie.module.example('.htv (or .hitbox) hitboxusername')
def hitbox(bot,trigger):
    if not trigger.group(2):
        return bot.say('Enter a hitbox user\'s name.')
    else:
        ret = trigger.group(2)
        uri5 = 'http://api.hitbox.tv/media/live/{0}'.format(ret)
        try:
            bytes3 = urlopen(uri5).read()
        except (HTTPError, IOError, ValueError):
            return bot.say("User might not exist.")
        c3 = json.loads(bytes3.decode())
        if c3['livestream'][0]['media_is_live'] == '1':
            return bot.say('{0} is streaming {1}: {2}'.format(ret, c3['livestream'][0]['category_name'], c3['livestream'][0]['channel']['channel_link']))
        else:
            return bot.say('{0} is currently not streaming.'.format(ret))
