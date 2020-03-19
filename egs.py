
import requests
import sopel
import datetime

@sopel.module.commands('egs', 'egsfree')
def egs(bot, trigger):
  variables={"namespace":"epic","country":"US","locale":"en-US"}
  query= """
          query promotionsQuery($namespace: String!, $country: String!, $locale: String!) {
            Catalog {
              catalogOffers(namespace: $namespace, locale: $locale, params: {category: \"freegames\", country: $country, sortBy: \"effectiveDate\", sortDir: \"asc\"}) {
                elements {
                  title
                  description
                  promotions {
                    promotionalOffers {
                      promotionalOffers {
                        startDate
                        endDate
                      }
                    }
                    upcomingPromotionalOffers {
                      promotionalOffers {
                        startDate
                        endDate
                      }
                    }
                  }
                }
              }
            }
          }
        """

  res = (requests.post('https://graphql.epicgames.com/graphql', json={'query': query, 'variables': variables})).json()
  freenow = []
  upcomingfree = []
  for x in res['data']['Catalog']['catalogOffers']['elements']:
    if not x['promotions']:
      continue
    if x['promotions']['promotionalOffers']:
      freenow.append("{} [until {}]".format(x['title'], datetime.datetime.strptime(x['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['endDate'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%m/%d")))
    else:
      upcomingfree.append("{} [starts {}]".format(x['title'], datetime.datetime.strptime(x['promotions']['upcomingPromotionalOffers'][0]['promotionalOffers'][0]['endDate'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%m/%d")))

  bot.say("Free now: {} | Upcoming: {}".format(", ".join(freenow), ", ".join(upcomingfree)))
