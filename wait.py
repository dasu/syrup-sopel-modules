import sopel
import requests
import base64
from PIL import Image
from io import BytesIO
import sys

expire = 0
token = '' #api token for trace.moe, instruction to get one: https://soruly.github.io/trace.moe/ #2018-10-24 addendum: may not be necessary anymore

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
    global token
    if not trigger.group(2):
        return bot.say("Provide an animu screenshot")
    imageurl = trigger.group(2)
    if not check_image(imageurl):
        return bot.say("Doesn't seem to be an image type.  Direct image links only.")
    imgdata = requests.get(imageurl)
    b64 = base64.b64encode(imgdata.content)
    if sys.getsizeof(b64) > 999999:
        img = Image.open(BytesIO(imgdata.content))
        if img.format == "GIF":
            try:
                img.seek(2)
            except:
                img.seek(0)
            img = img.convert("RGB")
        if img.mode in ('RGBA', 'LA'):
            img = img.convert("RGB")
        img.save("/tmp/temp.jpg")
        with open("/tmp/temp.jpg", "rb") as img_tmp:
            b64 = base64.b64encode(img_tmp.read())
    data = {'image':b64}
    baseurl = 'https://trace.moe/api/search' #?token={}'.format(token)
    headers ={"content-type":"application/x-www-form-urlencoded; charset=UTF-8"}
    try:
        req = requests.post(baseurl, data=data, headers=headers)
    except:
        return bot.say("trace.moe may be down")
    if req.ok:
        try:
            if req.json()['quota'] == 0:
                expire = req.json()['expire']
            if req.json()['docs']:
                animu_eng = req.json()['docs'][0]['title_english']
                animu_rom = req.json()['docs'][0]['title_romaji']
                animu_title = req.json()['docs'][0]['title']
                season = req.json()['docs'][0]['season']
                accuracy = round(req.json()['docs'][0]['similarity'] * 100,2)
                episode = req.json()['docs'][0]['episode']
                return bot.say("{} [{}] Episode:{} Confidence: {}% | https://trace.moe/?url={}".format(animu_eng, animu_rom, episode, accuracy, imageurl))
            else:
                return bot.say("No results.")
        except:
            return bot.say("JSON parse error D:")
    elif req.status_code == 413:
        return bot.say("File too large, try a smaller file. (<1MB?)")
    elif req.status_code == 429:
        if expire:
            return bot.say("Quota reached, wait {} seconds, or check https://trace.moe/?url={0}".format(expire,imageurl))
        else:
            return bot.say("Quota reached... Check https://trace.moe/?url={0}".format(imageurl))
    else:
        return bot.say("Unknown error. ({})".format(req.status_code))
