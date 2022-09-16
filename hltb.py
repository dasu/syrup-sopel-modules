import requests
import json
import sopel


@sopel.module.commands('hltb','howlong','howlongtobeat')
@sopel.module.example('.hltb game name')
def hltb(bot,trigger):
    if not trigger.group(2):
        return bot.say("Enter a game name to search.")
    game = trigger.group(2)
    url = "https://howlongtobeat.com/api/search"
    payload = json.dumps( {"searchType":"games","searchTerms":game.split(),"searchPage":1,"size":20,"searchOptions":{"games":{"userId":0,"platform":"","sortCategory":"popular","rangeCategory":"main","rangeTime":{"min":0,"max":0},"gameplay":{"perspective":"","flow":"","genre":""},"modifier":""},"users":{"sortCategory":"postcount"},"filter":"","sort":0,"randomizer":0}})
    test = {'Content-type':'application/json', 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36','origin':'https://howlongtobeat.com','referer':'https://howlongtobeat.com'}
    session = requests.Session()
    r = session.post(url, headers=test, data=payload)
    res = r.json()
    if not res['data']:
        return bot.say("No results.")

    name = res['data'][0]['game_name']
    timesecs = res['data'][0]['comp_main']
    if ((timesecs/60) >= 120):
        time = "{:.0f}{} hours".format(timesecs/60/60, '½' if timesecs/60/60 % 1 >= 0.5 else '')
    else:
        time = "{:.0f} minutes".format(timesecs/60)
    bot.say('{} - {}'.format(name, time))

@sopel.module.commands('althltb','althowlong','althowlongtobeat')
@sopel.module.example('.althltb game name')
def althltb(bot,trigger):
    if not trigger.group(2):
        return bot.say("Enter a game name to search.")
    game = trigger.group(2)
    url = "https://howlongtobeat.com/api/search"
    payload = json.dumps( {"searchType":"games","searchTerms":game.split(),"searchPage":1,"size":20,"searchOptions":{"games":{"userId":0,"platform":"","sortCategory":"rating","rangeCategory":"main","rangeTime":{"min":0,"max":0},"gameplay":{"perspective":"","flow":"","genre":""},"modifier":""},"users":{"sortCategory":"postcount"},"filter":"","sort":0,"randomizer":0}})
    test = {'Content-type':'application/json', 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36','origin':'https://howlongtobeat.com','referer':'https://howlongtobeat.com'}
    session = requests.Session()
    r = session.post(url, headers=test, data=payload)
    res = r.json()
    if not res['data']:
        return bot.say("No results.")

    name = res['data'][0]['game_name']
    timesecs = res['data'][0]['comp_main']
    if ((timesecs/60) >= 120):
        time = "{:.0f}{} hours".format(timesecs/60/60, '½' if timesecs/60/60 % 1 >= 0.5 else '')
    else:
        time = "{:.0f} minutes".format(timesecs/60)
    bot.say('{} - {}'.format(name, time))
