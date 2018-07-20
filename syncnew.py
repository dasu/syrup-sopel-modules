from sopel.module import commands
from sopel.tools import Identifier
from sync import *  #https://github.com/kds14/sync3

def channel_user_list(bot, trigger):
    channel_user_list = []
    nicks = bot.channels[trigger.sender.lower()].users
    for nick in nicks:
        channel_user_list.append(Identifier(nick))
    return channel_user_list

@commands('sync')
def sopel_sync(bot,trigger):
    message_group = trigger.group(2)
    if message_group != None:
        syncers_names = [Identifier(s) for s in message_group.split()]
    else:
        return bot.say("What are you doing, nerd?")
    channel_list = channel_user_list(bot,trigger)
    start_sync(Identifier(trigger.nick), syncers_names, channel_list, bot.say)

@commands('desync')
def sopel_desync(bot,trigger):
    desync(Identifier(trigger.nick), bot.say)

@commands('ready')
def sopel_ready(bot,trigger):
    ready_syncer(Identifier(trigger.nick), bot.say)

@commands('resync')
def sopel_resync(bot,trigger):
    channel_list = channel_user_list(bot, trigger)
    resync(Identifier(trigger.nick), channel_list, bot.say)

@commands('syncg_create')
def sopel_sync_group(bot,trigger):
    group = trigger.group(3)
    syncers_names = [Identifier(s) for s in trigger.group(2).strip().split(" ")[1:]]
    channel_list = channel_user_list(bot, trigger)
    create_sync_group(Identifier(trigger.nick),group, syncers_names, channel_list, bot.say)

@commands('syncg')
def sopel_start_syncgroup(bot,trigger):
    group = trigger.group(2)
    channel_list = channel_user_list(bot, trigger)
    start_sync_by_group(Identifier(trigger.nick), group, channel_list, bot.say)
