#code based off https://github.com/theappleman/pyvndb
#this is a mess and can be refactored significantly

import json
from socket import socket as ss
import sopel
import re
from sopel.tools import SopelMemory

vndbregex = re.compile('.*(https?:\/\/vndb.org\/v(.*?((?=[\s])|$)))')

def setup(bot):
    if not bot.memory.contains('url_callbacks'):
        bot.memory['url_callbacks'] = SopelMemory()
    bot.memory['url_callbacks'][vndbregex] = vndbirc

def shutdown(bot):
    del bot.memory['url_callbacks'][vndbregex]

def login(sock):
    sock.connect(("api.vndb.org", 19534))
    test = bytes("login {\"protocol\":1,\"client\":\"syrup\",\"clientver\":0.9}\x04", "utf-8")
    sock.sendall(test)
    recv(sock)

def recv(sock):
    data = sock.recv(4096)
    if not data.endswith(b"\x04"):
        data += recv(sock)
    return data

def gettags(tags):
    json_data=open("/home/desu/vndb/tags.json").read()
    tagsjs = json.loads(json_data)
    tah = []
    for tag in tags:
        if tag[2] == 0 and tag[1] >= 2.95:
            for b in tagsjs:
                if b['id'] == tag[0]:
                    tah.append(b['name'])
    tags2 = ", ".join(tah)
    return tags2

def getlength(vnlength):
    length = {}
    length[1] = "Very short (< 2 hours)"
    length[2] = "Short (2 - 10 hours)"
    length[3] = "Medium (10 - 30 hours)"
    length[4] = "Long (30 - 50 hours)"
    length[5] = "Very Long (> 50 hours)"
    return length[vnlength]

@sopel.module.commands('vndb','vn')
@sopel.module.example('.vn or .vndb visualnoveltitle')
def vndb(bot, trigger):
    sock = ss()
    if not trigger.group(2):
        return bot.say("Enter a VN name to search.")
    i = trigger.group(2)
    request = "get vn basic,details,stats,tags (search ~ \"{0}\")\x04".format(i)
    test = bytes(request, "utf-8")
    login(sock)
    sock.sendall(test)
    #bot.say(sock)
    vn = recv(sock)
    #bot.say(vn)
    if str(vn, "utf-8")[0:5] == 'error':
        return bot.say("An error occured.")
    else:
        js = json.loads((str(vn, "utf-8"))[8:-1])
        if js['items']:
            tags = js['items'][0]['tags']
            tags2 = gettags(tags)
            if not tags2:
                tags2 = "None"
            if not js['items'][0]['length']:
                vnlength = 'Unknown'
            else:
                vnlength = getlength(js['items'][0]['length'])
            if not js['items'][0]['released']:
                released = 'Unknown'
            else:
                released = js['items'][0]['released']
            return bot.say('{0}: http://vndb.org/v{1} , Released: {2}, Length: {3}, Tags: {4}'.format(js['items'][0]['title'],js['items'][0]['id'],released,vnlength,tags2))
        else:
            return bot.say("No results.")
    sock.close()
    
def vndbirc(bot, trigger, match = None):
match = match or trigger
request = "get vn basic,details,stats,tags (id = {0})\x04".format(match.group(2))
sock = ss()
test = bytes(request, "utf-8")
login(sock)
sock.sendall(test)
vn = recv(sock)
if str(vn, "utf-8")[0:5] == 'error':
    return bot.say("An error occured.")
else:
    js = json.loads((str(vn, "utf-8"))[8:-1])
    if js['items']:
        title = js['items']
        tags = js['items'][0]['tags']
        tags2 = gettags(tags)
        if not tags2:
            tags2 = "None"
        if not js['items'][0]['length']:
            vnlength = 'Unknown'
        else:
            vnlength = getlength(js['items'][0]['length'])
        if not js['items'][0]['released']:
            released = 'Unknown'
        else:
            released = js['items'][0]['released']
        return bot.say('{0} | Released: {1}, Length: {2}, Rating: {3} Tags: {4}'.format(js['items'][0]['title'],released,vnlength,js['items'][0]['rating'],tags2))
    else:
        pass
sock.close()
