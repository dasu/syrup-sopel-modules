import requests
import sopel
from sopel.tools import SopelMemory

@sopel.module.commands('anilist','anime')
def anilist(bot, trigger):
  if not trigger.group(2):
    return bot.say("Enter a valid anime name")
  variable = {'search':'{}'.format(trigger.group(2))}
  query= """
    query ($search: String) {
      Media (search: $search, type: ANIME) {
        id
        title {
          romaji
          english
        }
        startDate {
          year
        }
        episodes
        format
        genres
        status
        siteUrl
      }
    }
  """
  x = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variable})
  if not x.ok:
    return bot.say("API Error")
  name = x.json()['data']['Media']['title']['romaji']
  name_eng = x.json()['data']['Media']['title']['english']
  genres = ", ".join(x.json()['data']['Media']['genres'])
  year = x.json()['data']['Media']['startDate']['year']
  type = x.json()['data']['Media']['format']
  episodes = x.json()['data']['Media']['episodes']
  status = x.json()['data']['Media']['status']
  link = x.json()['data']['Media']['siteUrl']
  return bot.say("{0} [{1}] - Type: {2} Eps: {3} Genres: {4} status: {5} | {6}".format(name, year, type, episodes, genres, status, link))














