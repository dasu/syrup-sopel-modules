"""
RE-Rework of sync (v4?). Allows users to ready 
and sync movies or whatever.  By @agricola
"""
import sopel.module
from sopel.tools import Identifier
import time

old_syncs = []
current_syncs = []
sync_id = 0
max_old_syncs = 100

class Sync:
	def __init__(self, syncers, channel):
		global sync_id
		self.syncers = syncers
		self.timeout = 10
		self.id = sync_id
		self.channel = channel
		sync_id += 1

	def ready(self):
		return all([r for s,r in self.syncers.items()])

	def names(self):
		return ", ".join([str(s) for s,r in self.syncers.items()])

def check_valid(bot, trigger, sync):
	channel_users = [Identifier(n) for n in bot.channels[trigger.sender.lower()].users]
	if Identifier(bot.nick) in sync.syncers:
		bot.say("Sorry! I'm shy!!!")
		return False

	if len(sync.syncers) < 2:
		bot.say("Not enough syncers! Get some friends!")
		return False

	for nick in sync.syncers:
		if nick not in channel_users:
			bot.say("{} is invalid! Get em outta here!".format(str(nick)))
			return False
		else:
			for s in current_syncs:
				if s is not sync and nick in s.syncers:
					bot.say("{} is busy with sync {:X}".format(str(nick), s.id))
					return False
	return True

def find_sync(bot, trigger, nick, sync_list, sid=None):
	sync = None
	for s in sync_list:
		if Identifier(nick) in s.syncers and check_valid(bot, trigger, s):
			if sid is None or s.id == sid:
				sync = s
				break
	return sync

def add_old_sync(sync):
	global old_syncs
	old_syncs.insert(0, sync)
	if len(old_syncs) > max_old_syncs:
		old_syncs = old_syncs[:len(old_syncs)-max_old_syncs]

@sopel.module.interval(10)
def sync_update(bot):
	global current_syncs
	for s in current_syncs:
		if s.channel not in bot.channels:
			continue
		s.timeout -= 1
		if s.timeout <= 0:
			add_old_sync(s)
			bot.say("Sync {:X} failed!".format(s.id), s.channel)

	current_syncs = [s for s in current_syncs if s.timeout > 0]

@sopel.module.commands("sync")
@sopel.module.commands("s")
@sopel.module.priority("high")
def sync(bot, trigger):
	if trigger.group(2) == None:
		return bot.say("Please include syncer names!")

	syncers = trigger.group(2).split()
	syncers.append(trigger.nick)
	sync = Sync({Identifier(s): False for s in set(syncers)}, trigger.sender)

	if check_valid(bot, trigger, sync):
		sync.syncers[Identifier(trigger.nick)] = True
		current_syncs.append(sync)
		bot.say("Buckle up syncers! (ID: {:X})".format(sync.id))

@sopel.module.commands("desync")
@sopel.module.commands("ds")
@sopel.module.priority("high")
def desync(bot, trigger):
	global current_syncs
	sync = find_sync(bot, trigger, Identifier(trigger.nick), current_syncs)

	if sync is None:
		bot.say("Sorry! You are not in a sync!")
	else:
		current_syncs = [s for s in current_syncs if s is not sync]
		add_old_sync(sync)
		bot.say("Desyncing... (ID: {:X})".format(sync.id))

@sopel.module.commands("ready")
@sopel.module.commands("rdy")
@sopel.module.commands("r")
@sopel.module.commands("lady")
@sopel.module.priority("high")
def ready(bot, trigger):
	global current_syncs
	sync = find_sync(bot, trigger, Identifier(trigger.nick), current_syncs)

	# Debug
	#bot.say("{}".format([s.id for s in current_syncs]))
	#bot.say("{}".format([s.id for s in old_syncs]))

	if sync is None:
		bot.say("Sorry! Could not find you in a valid sync!")
	else:
		sync.syncers[Identifier(trigger.nick)] = True
		if sync.ready():
			current_syncs = [s for s in current_syncs if s is not sync]
			add_old_sync(sync)
			bot.say("Lets go {}!".format(sync.names()))
			time.sleep(2)
			for i in reversed(range(1,4)):
				bot.say("{}".format(i))
				time.sleep(2)
			bot.say("GO!")
	
		
@sopel.module.commands("resync")
@sopel.module.commands("rs")
@sopel.module.priority("high")
def resync(bot, trigger):
	global old_syncs
	sid = trigger.group(2)
	if sid is not None:
		sid = int(sid, 16) 

	sync = find_sync(bot, trigger, Identifier(trigger.nick), old_syncs, sid)

	if sync is None:
		bot.say("Sorry! You were not in a recent sync!")
	else:
		sync.syncers = {s:False for s in sync.syncers}
		sync.syncers[Identifier(trigger.nick)] = True
		sync.timeout = 10

		old_syncs = [s for s in old_syncs if s is not sync]
		current_syncs.append(sync)
	bot.say("Buckle up resyncers! {} (ID: {:X})".format(sync.names(), sync.id))
