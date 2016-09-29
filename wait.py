import sopel
import requests
import base64

def check_image(imgurl):
    try:
        response = requests.head(imgurl)
        if response.headers['Content-Type'].startswith('image'):
            return True
        else:
            return False
    except:
        return False

@sopel.module.commands('wait')
def wait(bot,trigger):
    if not trigger.group(2):
        return bot.say("Provide an animu screenshot")
    imageurl = trigger.group(2)
    if not check_image(imageurl):
        return bot.say("Doesn't seem to be an image type.  Direct image links only.")
    imgdata = requests.get(imageurl)
    b64 = base64.b64encode(imgdata.content)
    data = {'data':b64}
    baseurl = 'https://whatanime.ga/search'
    headers ={
    "accept":"application/json, text/javascript, */*; q=0.01",
    "accept-encoding":"gzip, deflate, br",
    "accept-language":"en-US,en;q=0.8",
    "content-length": imgdata.headers['Content-Length'],
    "content-type":"application/x-www-form-urlencoded; charset=UTF-8",
    "origin":"https://whatanime.ga",
    "referer":"https://whatanime.ga/?url={0}".format(imageurl),
    "user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
    "x-requested-with":"XMLHttpRequest"
    }
    req = requests.post(baseurl, data=data, headers=headers)
    if req.ok:
        try:
            if req.json()['docs']:
                animu_eng = req.json()['docs'][0]['title_english']
                animu_rom = req.json()['docs'][0]['title_romaji']
                accuracy = round(100 - req.json()['docs'][0]['diff'],2)
                episode = req.json()['docs'][0]['episode']
                return bot.say("{} [{}] Episode:{} Confidence: {}% | https://whatanime.ga/?url={}".format(animu_eng, animu_rom, episode, accuracy, imageurl))
            else:
                return bot.say("No results.")
        except:
            return bot.say("Error D:")
    else:
        return bot.say("Quota reached...maybe.  Wait an hour, or check https://whatanime.ga/?url={0}".format(imageurl))
