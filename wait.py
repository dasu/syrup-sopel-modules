import sopel
import requests
import base64
from PIL import Image
from io import BytesIO

expire = 0

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
    global expire
    if not trigger.group(2):
        return bot.say("Provide an animu screenshot")
    imageurl = trigger.group(2)
    if not check_image(imageurl):
        return bot.say("Doesn't seem to be an image type.  Direct image links only.")
    imgdata = requests.get(imageurl)
    if int(imgdata.headers['Content-Length']) >= 819200:
        img = Image.open(BytesIO(imgdata.content))
        img.save("/tmp/temp.jpg")
        with open("/tmp/temp.jpg", "rb") as img_tmp:
            b64 = base64.b64encode(img_tmp.read())
            img_tmp.seek(0)
            length = len(img_tmp.read())
    else:
        b64 = base64.b64encode(imgdata.content)
        length = imgdata.headers['Content-Length']
    data = {'data':b64}
    baseurl = 'https://whatanime.ga/search'
    headers ={
    "accept":"application/json, text/javascript, */*; q=0.01",
    "accept-encoding":"gzip, deflate, br",
    "accept-language":"en-US,en;q=0.8",
    "content-length": length,
    "content-type":"application/x-www-form-urlencoded; charset=UTF-8",
    "origin":"https://whatanime.ga",
    "referer":"https://whatanime.ga/?url={0}".format(imageurl),
    "user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
    "x-requested-with":"XMLHttpRequest"
    }
    try:
        req = requests.post(baseurl, data=data, headers=headers)
    except:
        return bot.say("Website may be down")
    if req.ok:
        try:
            if req.json()['quota'] == 0:
                expire = req.json()['expire']
            if req.json()['docs']:
                animu_eng = req.json()['docs'][0]['title_english']
                animu_rom = req.json()['docs'][0]['title_romaji']
                accuracy = round(100 - req.json()['docs'][0]['diff'],2)
                episode = req.json()['docs'][0]['episode']
                return bot.say("{} [{}] Episode:{} Confidence: {}% | https://whatanime.ga/?url={}".format(animu_eng, animu_rom, episode, accuracy, imageurl))
            else:
                return bot.say("No results.")
        except:
            return bot.say("JSON parse error D:")
    elif req.status_code == 413:
        return bot.say("File too large, try a smaller file. (<1MB?)")
    elif req.status_code == 429:
        if expire:
            return bot.say("Quota reached, wait {} minutes, or check https://whatanime.ga/?url={0}".format(round(expire/60,2),imageurl))
        else:
            return bot.say("Quota reached... Check https://whatanime.ga/?url={0}".format(imageurl))
    else:
        return bot.say("Unknown error. ({})".format(req.status_code))
