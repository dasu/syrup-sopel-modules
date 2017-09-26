import sopel
import hashlib
import random

@sopel.module.commands('rate','ratewaifu')
def ratewaifu(bot,trigger):
    if trigger.group(2):
        seed = hashlib.md5(("{}".format(trigger.group(2))).encode('utf-8')).hexdigest()
        random.seed(seed)
        bot.say("You're waifu is a {}".format(random.randint(0,10)))
