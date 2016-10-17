"""
Rework of sync. Allows users to ready 
and sync movies or whatever.
"""
from threading import Timer
from sopel.module import commands
from time import sleep
from sopel.tools import Identifier

ALREADY_READY_MESSAGE = "You are already ready!"
BUCKLE_UP_MESSAGE = "Buckle up "
DESYNCING_SYNC_MESSAGE = "Desyncing..."
NOT_A_SYNCER_MESSAGE = "You are not part of this sync."
IS_INVALID_MESSAGE = "is an invalid syncer. "
ARE_INVALID_MESSAGE = "are invalid syncers. "
SYNC_FAILED_MESSAGE = "Sync failed."
WHAT_DOING_MESSAGE = "What are you doing, noob?"
INCLUDE_SELF_MESSAGE = "Include yourself in the sync, clown."
WAIT_FOR_SYNC_MESSAGE = "Wait for the current sync to finish."
NO_SYNC_MESSAGE = "There is no sync."
NO_PREV_SYNC_MESSAGE = "No previous sync."
WAS_LAST_SYNCER_MESSAGE = "was in the last sync."
WERE_LAST_SYNCERS_MESSAGE = "were in the last sync."
NOT_IN_PREV_SYNC_MESSAGE = "You were not in the last sync."

_current_sync = None # holds the current sync object being used
_previous_sync = None

class Sync:
    __syncers = []
    __bot = None
    __sync_timer = None
    __channel_user_list = []
    __syncer_names = []
    __valid = True

    # constructor that sets syncers and starts the mad timer
    def __init__(self, syncer_names, bot, channel_user_list):
        self.__channel_user_list = channel_user_list
        self.__bot = bot
        self.__syncer_names = syncer_names
        self.__syncers, non_valid_syncers = self.syncer_list(syncer_names)

        self.start_sync_if_valid(non_valid_syncers)

    @property
    def syncer_names(self):
        return self.__syncer_names

    @property
    def syncers(self):
        return self.__syncers

    @property
    def is_valid(self):
        return self.__valid

    def reinitialization_arguments(self):
        return self.__syncer_names, self.__channel_user_list


    def start_sync_if_valid(self, non_valid_syncers):
        if len(non_valid_syncers) > 0:
            self.__bot.say(self.warn_of_invalid_syncers(non_valid_syncers))
            self.__valid = False
            self.desync_this_sync()
        else:
            self.start_timer()        

    # create list of syncers
    def syncer_list(self, syncer_names):
        syncers = []
        non_valid_syncers = []

        for syncer_name in syncer_names:
            new_syncer = Syncer(syncer_name)
            if self.is_syncer_valid(new_syncer):
                syncers.append(new_syncer)
            else:
                non_valid_syncers.append(new_syncer)
        return syncers, non_valid_syncers

    # warn syncers of invalid syncers
    def warn_of_invalid_syncers(self, invalid_syncers):
        invalid_syncers_string = ""
        
        invalid_syncers_string = self.syncer_list_string(invalid_syncers)

        invalid_syncers_string += " "

        if len(invalid_syncers) == 1:
            warning = invalid_syncers_string + IS_INVALID_MESSAGE + DESYNCING_SYNC_MESSAGE
        elif len(invalid_syncers) > 1:
            warning = invalid_syncers_string + ARE_INVALID_MESSAGE + DESYNCING_SYNC_MESSAGE

        return warning

    # string of syncers
    def syncer_list_string(self, syncer_list):
        names = []
        for syncer in syncer_list:
            names.append(syncer.name)

        syncer_list_string = ", ".join(names[:-2] + [" and ".join(names[-2:])])
        return syncer_list_string

    # checks if sync is ready IS THIS NEEDED?
    def are_all_syncers_ready(self):
        are_all_syncers_ready = True

        for syncer in self.__syncers:
            if syncer.is_ready == False:
                are_all_syncers_ready = False

        return are_all_syncers_ready

    # method that starts a timer
    def start_timer(self):
        self.__sync_timer=Timer(120.0, self.timeout_sync)
        self.__sync_timer.start()
        self.__bot.say(BUCKLE_UP_MESSAGE + self.syncer_list_string(self.__syncers) + "!")

    def timeout_sync(self):
        self.__bot.say(SYNC_FAILED_MESSAGE)
        self.desync_this_sync()


    # checks if a sync is valid
    def is_syncer_valid(self, syncer):
        is_syncer_valid = syncer.is_syncer_name_valid(self.__channel_user_list, self.__bot)
        return is_syncer_valid

    # initiate the sync
    def initiate_sync(self):
        self.desync_this_sync()
        self.__bot.say("Let's go " + self.syncer_list_string(self.__syncers) + "!")
        sleep(2)
        self.__bot.say("3")
        sleep(2)
        self.__bot.say("2")
        sleep(2)
        self.__bot.say("1")
        sleep(2)
        self.__bot.say("GO!")


    # sets syncer to ready
    def ready_syncer(self, syncer_name):
        syncer = self.find_syncer_based_on_name(syncer_name)

        if self.is_syncer_part_of_sync(syncer):
            if syncer.is_ready == False:
                syncer.is_ready = True
                if self.are_all_syncers_ready() == True:
                    self.initiate_sync()
            else:
                self.__bot.say(ALREADY_READY_MESSAGE)

    # find syncer in the sync list by name
    def find_syncer_based_on_name(self, syncer_name):
        syncer = None

        for s in self.__syncers:
            if Identifier(s.name) == Identifier(syncer_name.lower()):
                syncer = s

        return syncer

    # checks if it contains the syncer
    def is_syncer_part_of_sync(self, given_syncer):
        is_part_of_sync = False

        for syncer in self.__syncers:
            if given_syncer == syncer:
                is_part_of_sync = True

        return is_part_of_sync

    # desyncs the sync
    def syncer_desync_this_sync(self, syncer_name):
        syncer = self.find_syncer_based_on_name(syncer_name)

        if syncer != None:
            self.desync_this_sync()
            self.__bot.say(DESYNCING_SYNC_MESSAGE)
        else:
            self.__bot.say(NOT_A_SYNCER_MESSAGE)

    def desync_this_sync(self):
        global _current_sync, _previous_sync
        _previous_sync = _current_sync
        _current_sync = None
        if self.__sync_timer != None:
            self.__sync_timer.cancel()


class Syncer:
    __name = None
    __is_ready = False

    # get property of name
    @property
    def name(self):
        return self.__name
    
    # get/set property of ready
    @property
    def is_ready(self):
        return self.__is_ready

    @is_ready.setter
    def is_ready(self, value):
        self.__is_ready = value

    # constructor that sets name and checks if it is valid
    def __init__(self, syncer_name):
        self.__name = syncer_name.lower()

    # checks if the syncer is valid
    def is_syncer_name_valid(self, users_list, bot):
        is_valid = False

        nicknames = users_list

        for nick in nicknames:

            if self.__name == nick:
                is_valid = True

        return is_valid

def channel_user_list(bot, trigger):
    channel_user_list = []
    nicks = bot.channels[trigger.sender.lower()].users
    for nick in nicks:
        channel_user_list.append(Identifier(nick))
    return channel_user_list

def is_in_syncer_list(trigger, syncer_names):
    is_user_in_syncer_list = False
    for name in syncer_names:
        if Identifier(trigger.nick) == Identifier(name):
            is_user_in_syncer_list = True
    return is_user_in_syncer_list


@commands('sync','syncpoi','synczura')
def sync(bot,trigger):
    global _current_sync

    if _current_sync == None:
        message_group = trigger.group(2)
        if message_group != None:
            syncer_names = message_group.split()
        else:
            return bot.say(WHAT_DOING_MESSAGE)

        user_list = channel_user_list(bot, trigger)

        is_user_in_syncer_list = is_in_syncer_list(trigger, syncer_names)

        if not is_user_in_syncer_list:
            return bot.say(INCLUDE_SELF_MESSAGE)

        new_sync = Sync(syncer_names, bot, user_list)
        _current_sync = new_sync
        if not new_sync.is_valid:
            _current_sync = None
    else:
        bot.say(WAIT_FOR_SYNC_MESSAGE)

@commands('desync','desyncpoi','desynczura')
def desync(bot,trigger):
    if _current_sync != None:
        _current_sync.syncer_desync_this_sync(Identifier(trigger.nick))
    return

@commands('ready','readypoi','readyzura')
def ready(bot,trigger):
    if _current_sync != None:
        _current_sync.ready_syncer(Identifier(trigger.nick))
    else:
        bot.say(NO_SYNC_MESSAGE)
    return

@commands('resync','resyncpoi','resynczura')
def resync(bot,trigger):
    global _current_sync
    if _current_sync == None:
        if _previous_sync != None:
            _current_sync = _previous_sync
            user_list = channel_user_list(bot, trigger)
            syncer_names = _previous_sync.syncer_names

            is_user_in_syncer_list = is_in_syncer_list(trigger, syncer_names)
            if not is_user_in_syncer_list:
                _current_sync = None
                return bot.say(NOT_IN_PREV_SYNC_MESSAGE)

            _current_sync.__init__(_previous_sync.syncer_names, bot, user_list)
        else:
            bot.say(NO_PREV_SYNC_MESSAGE)
    else:
        bot.say(WAIT_FOR_SYNC_MESSAGE)

@commands('lastsync')
def last_sync(bot,trigger):
    if _previous_sync != None:
        syncers = _previous_sync.syncers
        message = ""
        if len(syncers) == 1:
            message = _previous_sync.syncer_list_string(syncers) + " " + WAS_LAST_SYNCER_MESSAGE
        elif len(syncers) > 1:
            message = _previous_sync.syncer_list_string(syncers) + " " + WERE_LAST_SYNCERS_MESSAGE

        bot.say(message)
    else:
        bot.say(NO_PREV_SYNC_MESSAGE)
