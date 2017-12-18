import sopel
from ouimeaux.environment import Environment

@sopel.module.require_admin
@sopel.module.commands('lights')
def wemo(bot, trigger):
    a = trigger.group(2)
    if not a:
        return
    env = Environment()
    env.start()
    env.discover(seconds=1)
    l = env.get_switch('Light')
    if a.lower() == 'on':
        l.on()
        return bot.say('Lights on')
    elif a.lower() == 'status':
        if l.get_state() == 1:
            bot.say('Light is on')
        elif l.get_state() == 0:
            bot.say('Light is off')
        else:
            bot.say('Unknown')
    elif a.lower() == 'off':
        l.off()
        return bot.say('Lights off')
