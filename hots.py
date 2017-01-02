from bs4 import BeautifulSoup
import requests
import sopel
import sys

#github.com/afengg
# if a > b, return 1. else return 0
def comparePercentages(a, b):
  a = 1 if (float(a[:-2]) > float(b[:-2])) else 0
  return a

def hotsSearch(url):
  r = requests.get(url)
  data = r.text
  soup = BeautifulSoup(data, "html.parser")

  # initialize talent lists
  desired_talents = []
  full_talents = []
  # find the appropriate section of webpage
  talent_details = soup.find("div", {"id": "ctl00_MainContent_RadGridHeroTalentStatistics"})
  # the section includes a table with the necessary information,
  # so gather all table cells into result set
  table_data = talent_details.find_all('td')
  talent = []

  for row in table_data:
      if 'Level: ' in row.text or '\xa0' in row.text:
        full_talents.append(talent)
        talent = []
      
      else:
        talent.append(row.text)
  #append last talent, since there is no 'Level: ' or '\xa0' after the final talent to trigger the append       
  full_talents.append(talent)

  # After appending all of the talents from the table, remove the head of the full_talents list twice
  # to remove unnecessary elements
  full_talents.pop(0)
  full_talents.pop(0)
  # set some initial values
  prev_level = '1';
  max_talent = full_talents[0]
  for talent in full_talents:
    # if we are still within the same talent tier
    if talent[0] == prev_level:
        if comparePercentages(talent[5], max_talent[5]) > 0:
          max_talent = talent 
        prev_level = talent[0]
      else:
        desired_talents.append(max_talent[2])
        max_talent = talent
        prev_level = talent[0]
  #append last talent
  desired_talents.append(max_talent[2])      
  return ' > '.join(desired_talents)

@sopel.module.commands('hots')
def hots(bot, trigger):
  if not trigger.group(2):
    return bot.say("Enter a HotS character.")
  i = trigger.group(2)
  
  url = 'http://www.hotslogs.com/Sitewide/HeroDetails?Hero={0}'.format(i)
  line = hotsSearch(url)
  bot.say(line)
    
    
    
    