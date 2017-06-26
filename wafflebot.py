import datetime
import redis
import markovify
import sopel

# Change this if you want, it will increase the DB size eventually.
timeout = 60 * 60 * 24 * 30 # 60s * 60m * 24h * 30d = 1 month
ignore = ["http"]

MAX_OVERLAP_RATIO = 0.7
MAX_OVERLAP_TOTAL = 15
global llines
llines = 0

db = redis.Redis(db=0)
class WaffleBotText(markovify.Text):
  def test_sentence_input(self, sentence):
    return True

  def _prepare_text(self, text):
    text = text.strip()

    #if not text.endswith((".", "?", "!")):
    #  text += "."

    return text

  def sentence_split(self, text):
    lines = text.splitlines()
    text = " ".join([self._prepare_text(line) for line in lines if line.strip()])

    return markovify.split_into_sentences(text)

def setup(bot):
  global fullresults
  global fullmodel
  #global llines
  #llines = 0
  fullresults = []
  for k in db.keys('*'):
    fullresults.extend(db.smembers(k))
  fullmodel = WaffleBotText("\n".join([r.decode('utf8') for r in fullresults]), state_size=3)

@sopel.module.interval(86400)
def refresh_results(bot):
  fullresults = []
  for k in db.keys('*'):
    fullresults.extend(db.smembers(k))
  fullmodel = WaffleBotText("\n".join([r.decode('utf8') for r in fullresults]), state_size=3)

@sopel.module.rule(r'.*$')
def wafflebot(bot, trigger):
  for ignored_item in ignore:
    if ignored_item.lower() in trigger.lower():
      continue

  # have at least 5 words
  if len(str(trigger).split(" ")) < 5:
    return

  today = datetime.datetime.now()
  key = "%s%s:%s" % (today.month, today.day, trigger.nick.lower())
  db.sadd(key, str(trigger))
  #db.expire(key, timeout)
  global llines
  llines+=1
  if llines > 1000:
    llines = 0
    nicklist = []
    fullresp = []
    nicks = bot.channels[trigger.sender.lower()].users
    for nick in nicks:
      nicklist.append(nick)
    while not fullresp:
      fullresp = fullmodel.make_short_sentence(140,
          max_overlap_total=MAX_OVERLAP_TOTAL,
          max_overlap_ratio=MAX_OVERLAP_RATIO)
    while any(word in fullresp.lower().split() for word in nicklist):
      fullresp = fullmodel.make_short_sentence(140,
          max_overlap_total=MAX_OVERLAP_TOTAL,
          max_overlap_ratio=MAX_OVERLAP_RATIO)
    bot.say(fullresp)
  
@sopel.module.commands('talk', 'wb')
def wafflebot_talk(bot, trigger):
  nick = trigger.group(2)
  if nick:
    pattern = "*:%s" % nick.lower()
    min_lines = 200
    results = []
    for k in db.keys(pattern):
      results.extend(db.smembers(k))
  else:
    #pattern = "*"
    min_lines = 100
    results = fullresults

  #results = []
  #for k in db.keys(pattern):
  #  results.extend(db.smembers(k))

  if len(results) < min_lines:
    bot.say("Sorry %s, there is not enough data." % trigger.nick)
  else:
    if nick:
      model = WaffleBotText("\n".join([r.decode('utf8') for r in results]), state_size=3)
      nicklist = []
      resp = []
      nicks = bot.channels[trigger.sender.lower()].users
      for nick in nicks:
        nicklist.append(nick)
      while not resp:
        resp = model.make_short_sentence(140,
          max_overlap_total=MAX_OVERLAP_TOTAL,
          max_overlap_ratio=MAX_OVERLAP_RATIO)
      while any(word in resp.lower().split() for word in nicklist):
        resp = model.make_short_sentence(140,
          max_overlap_total=MAX_OVERLAP_TOTAL, 
          max_overlap_ratio=MAX_OVERLAP_RATIO)
      bot.say(resp)
    else:
      nicklist = []
      fullresp = []
      nicks = bot.channels[trigger.sender.lower()].users
      for nick in nicks:
        nicklist.append(nick)
      while not fullresp:
        fullresp = fullmodel.make_short_sentence(140,
          max_overlap_total=MAX_OVERLAP_TOTAL,
          max_overlap_ratio=MAX_OVERLAP_RATIO)
      if fullresp:
        while any(word in fullresp.lower().split() for word in nicklist):
          fullresp = fullmodel.make_short_sentence(140,
            max_overlap_total=MAX_OVERLAP_TOTAL,
            max_overlap_ratio=MAX_OVERLAP_RATIO)
        bot.say(fullresp)

@sopel.module.commands('wbknows')
def wafflebotknows(bot,trigger):
  #knows = db.dbsize()
  knows = len(fullresults)
  bot.say("I know about %s things" % (knows))

@sopel.module.commands('lines')
def lines(bot,trigger):
  if not trigger.group(2):
    return bot.say("Enter a nick")
  db = redis.Redis(db=0)
  linessaid = 0
  for x in db.keys("*{0}".format(trigger.group(2))):
    print(x)
    linessaid+=len(db.smembers(x))
  bot.say("{} has said {} lines".format(trigger.group(2),linessaid))
