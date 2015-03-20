"""
FOR SYNCING AND SYNC CLUB ver 0.7
Written by agricola
"""
from threading import Timer
from time import sleep
import willie

#sync club related below
@willie.module.commands('sc','syncclub')
def club(bot,trigger):
    '''
    Returns the secret sync club link. Members only!
    '''
    bot.say("http://www.tinyurl.com/syncclub")



#general syncing below
@willie.module.rule('.*')
def name(bot,trigger):
    '''Remembers yo name
    '''
    if trigger.nick.lower() not in name.nerdlist and trigger.nick.lower() != 'py-ctcp':
        name.nerdlist.append(trigger.nick.lower())
    if len(name.nerdlist)>10:
        name.nerdlist.pop(0)
name.nerdlist = []

def namechecker(validnames,names_to_check):
    '''Checks the names of the readylist to the nerdlist'''
    wrongnames=[]
    i=0
    x=0
    while i < len(names_to_check):
        if names_to_check[i] not in validnames:
            wrongnames.insert(x,names_to_check[i])
            x+=1
        i+=1
    return wrongnames

@willie.module.commands('sync')
@willie.module.example('.sync <username1> <username2>')
def sync(bot,trigger):
    '''Starts a session to sync for various media.
    
    INPUT: .sync <username1> <username2> <etc>

    Creates a 1 minute timer to sync and makes a list of syncers
    '''

    if sync.sync_on==0 and len(trigger.group())>6:
        syncers = trigger.group().lower()
        sync.readylist = syncers.split()
        sync.readylist.pop(0)
        sync.namelist=list(set(sync.readylist))
        if trigger.nick.lower() not in name.nerdlist:
            name.nerdlist.append(trigger.nick.lower())
        badnames = namechecker(name.nerdlist,sync.namelist)
        sync.readylist=list(set(sync.readylist))
        if badnames == []:
            if sync.readylist!=[] and bot.nick not in sync.readylist and len(sync.readylist)<=10:
                    sync.madtime=Timer(60.0,mad,[bot,trigger])
                    sync.madtime.start()
                    bot.say("Buckle up syncers!")
                    sync.sync_on=1
            else:
                bot.say('fuck you')
        else:
            bot.say('Never heard of {0}'.format(", ".join(badnames)))
    else:
        bot.say('fuck you')
sync.sync_on = 0
sync.readylist = []
sync.namelist = []
sync.madtime = 0


def mad(bot,trigger):
    '''Bot gets mad.

    Calls out people , ends sync and clears variables.
    '''
    bot.say('Please .ready up: ' + ", ".join(sync.readylist))
    sleep(60)
    if sync.readylist !=[]:
        bot.say('Shit syncers: ' + ", ".join(sync.readylist))
        sync.readylist=[]
        sync.sync_on=0

@willie.module.commands('ready')
def ready(bot,trigger):
    '''User declares they are ready.

    INPUT: .ready

    Removes user from the list and initiates the sync if all are ready.
    '''

    if trigger.nick.lower() in sync.readylist:
        sync.readylist.remove(trigger.nick.lower())
        if sync.readylist == [] and sync.sync_on == 1:
            sync.madtime.cancel()
            bot.say('Lets go {0}!'.format(", ".join(sync.namelist)))
            sleep(2)
            bot.say("3")
            sleep(2)
            bot.say("2")
            sleep(2)
            bot.say("1")
            sleep(2)
            bot.say("GO!")
            sync.sync_on=0
    else:
        bot.say("You're not on the list.")


@willie.module.commands('desync')
def desync(bot,trigger):
    '''Cancels sync

    INPUT: .desync

    Ends the sync if user on the list
    '''
    if sync.readylist !=[] and sync.sync_on == 1:
        if trigger.nick.lower() in sync.readylist:
            bot.say('Aborting sync...')
            sync.madtime.cancel()
            sync.sync_on=0
            sync.readylist=[]
        else:
            bot.say("You're not on the list.")
    else:
        bot.say('fuck you')


if __name__ == '__main__':
    print(__doc__.strip())
