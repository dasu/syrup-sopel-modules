import requests
import sopel
from sopel.tools import SopelMemory
import re

anilistregex = re.compile('.*https?:\/\/anilist.co\/anime\/(\d.*?(?=\/))\/?.*?((?=[\s])|$)')

def setup(bot):
  if not bot.memory.contains('url_callbacks'):
    bot.memory['url_callbacks'] = SopelMemory()
  bot.memory['url_callbacks'][anilistregex] = anilistirc

def shutdown(bot):
  del bot.memory['url_callbacks'][anilistregex]

def aniquery(bot, trigger, id=None, search=None):
  target = "id" if id else "search"
  query = id or search
  variable = {'{}'.format(target):'{}'.format(query)}
  query = """
    query (${0}: {1}) {{
      Media ({0}: ${0}, type: ANIME) {{
        id
        title {{
          romaji
          english
        }}
        startDate {{
          year
        }}
        episodes
        format
        genres
        status
        siteUrl
      }}
    }}
  """.format(target, "String" if search else "Int")
  x = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variable})
  return x

@sopel.module.commands('anilist', 'mal')
def anilist(bot, trigger):
  if not trigger.group(2):
    return bot.say("Enter a valid anime name")
  x = aniquery(bot, trigger, search = trigger.group(2))
  if not x.ok:
    return bot.say("API Error")
  name = x.json()['data']['Media']['title']['romaji']
  genres = ", ".join(x.json()['data']['Media']['genres'])
  year = x.json()['data']['Media']['startDate']['year']
  type = x.json()['data']['Media']['format']
  episodes = x.json()['data']['Media']['episodes']
  status = x.json()['data']['Media']['status']
  link = x.json()['data']['Media']['siteUrl']
  return bot.say("{0} [{1}] - Type: {2} Eps: {3} Genres: {4} status: {5} | {6}".format(name, year, type, episodes, genres, status, link))

@sopel.module.rule('.*https?:\/\/anilist.co\/anime\/(\d.*?(?=\/))\/?.*?((?=[\s])|$)')
def anilistirc(bot,trigger, match=None):
  match = match or trigger
  x = aniquery(bot, trigger, id=match.group(1))
  if not x.ok:
    return
  name = x.json()['data']['Media']['title']['romaji']
  genres = ", ".join(x.json()['data']['Media']['genres'])
  year = x.json()['data']['Media']['startDate']['year']
  type = x.json()['data']['Media']['format']
  episodes = x.json()['data']['Media']['episodes']
  status = x.json()['data']['Media']['status']
  return bot.say("{0} [{1}] - Type: {2} Eps: {3} Genres: {4} status: {5}".format(name, year, type, episodes, genres, status))
