"""
Rework of sync. Allows users to ready 
and sync movies or whatever.
"""
from threading import Timer
from sopel.module import commands
from time import sleep
from sopel.tools import Identifier

_current_sync = None # holds the current sync object being used

class Sync:
    DESYNC_TO_CANCEL_MESSAGE = "Type '.desync' if you would like to cancel the sync."
    ALREADY_READY_MESSAGE = "You are already ready!"
    BUCKLE_UP_MESSAGE = "Buckle up syncers!"
    DESYNCING_SYNC_MESSAGE = "Desyncing..."
    NOT_A_SYNCER_MESSAGE = "You are not part of this sync."

    __syncers = []
    __bot = None
    __sync_timer = None
    __channel_user_list = []

    # constructor that sets syncers and starts the mad timer
    def __init__(self, syncer_names, bot, channel_user_list):
        self.__channel_user_list = channel_user_list
        self.__bot = bot
        self.__syncers, non_valid_syncers = self.syncer_list(syncer_names)

        if len(non_valid_syncers) > 0:
            bot.say(self.warn_of_invalid_syncers(non_valid_syncers))
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
            warning = invalid_syncers_string + "is an invalid syncer. " + self.DESYNC_TO_CANCEL_MESSAGE
        elif len(invalid_syncers) > 1:
            warning = invalid_syncers_string + "are invalid syncers. " + self.DESYNC_TO_CANCEL_MESSAGE

        return warning

    # string of syncers
    def syncer_list_string(self, syncer_list):
        syncer_list_string = ""
        syncer_list_length = len(syncer_list)
        last_index = syncer_list_length - 1
        first_item = True

        if syncer_list_length == 1:
            syncer_list_string = syncer_list[0].name
        elif syncer_list_length > 1:
            i = 0
            for invalid_syncer in syncer_list:
                if not first_item and syncer_list_length != 2:
                    syncer_list_string += ", "
                if i == last_index and i > 0:
                    syncer_list_string += " and "
                syncer_list_string += invalid_syncer.name
                first_item = False
                i += 1
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
        self.__bot.say(self.BUCKLE_UP_MESSAGE)

    def timeout_sync(self):
        self.__bot.say("Sync failed.")
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
            self.__bot.say(self.DESYNCING_SYNC_MESSAGE)
        else:
            self.__bot.say(self.NOT_A_SYNCER_MESSAGE)

    def desync_this_sync(self):
        global _current_sync
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

@commands('sync','syncpoi','synczura')
def sync(bot,trigger):
    global _current_sync

    if _current_sync == None:
        message_group = trigger.group(2)
        if message_group != None:
            syncer_names = message_group.split()
        else:
            bot.say("What are you doing, noob?")
            return


        channel_user_list = []
        nicks = bot.channels[trigger.sender.lower()].users
        for nick in nicks:
            channel_user_list.append(Identifier(nick))


        is_user_in_syncer_list = False
        for name in syncer_names:
            if Identifier(trigger.nick) == Identifier(name):
                is_user_in_syncer_list = True
        
        if not is_user_in_syncer_list:
            bot.say("Include yourself in the sync, clown.")
            return

        new_sync = Sync(syncer_names, bot, channel_user_list)
        _current_sync = new_sync
    else:
        bot.say("Wait for the current sync to finish.")

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
        bot.say("There is no sync.")
    return
