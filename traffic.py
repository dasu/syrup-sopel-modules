
import sopel
import requests

api = ''

def reversewoeid_search(query):
    """
    Find the first Where On Earth ID for the given query. Result is the etree
    node for the result, so that location data can still be retrieved. Returns
    None if there is no result, or the woeid field is empty.
    """
    query = 'q=select * from geo.places where woeid="%s"&format=json' % query
    body = requests.get('http://query.yahooapis.com/v1/public/yql?' + query)
    return body

def woeid_search(query):
    """
    Find the first Where On Earth ID for the given query. Result is the etree
    node for the result, so that location data can still be retrieved. Returns
    None if there is no result, or the woeid field is empty.
    """
    query = 'q=select * from geo.places where text="%s"&format=json' % query
    body = requests.get('http://query.yahooapis.com/v1/public/yql?' + query)
    return body

@sopel.module.commands('traffic','timeto')
@sopel.module.example('.traffic NYC, NY')
def traffic(bot,trigger):
    if not trigger.group(2):
        return bot.say("Enter a destination")
    woeid = bot.db.get_nick_value(trigger.nick, 'woeid')
    if not woeid:
        return bot.say("I don't know where you live, you can set a location using .setlocation place")
    #origin = (reversewoeid_search(woeid)).json()['query']['results']['place']['postal']['content']
    origin = "{0},{1}".format((reversewoeid_search(woeid)).json()['query']['results']['place']['centroid']['latitude'],(reversewoeid_search(woeid)).json()['query']['results']['place']['centroid']['longitude'])
    if origin:
        dest = trigger.group(2)
        #dest = "{0},{1}".format((woeid_search(trigger.group(2))).json()['query']['results']['place']['centroid']['latitude'],(woeid_search(trigger.group(2))).json()['query']['results']['place']['centroid']['longitude'])
        if dest:
            url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&avoid=tolls&departure_time=now&traffic_model=best_guess&units=imperial&key={2}'.format(origin,dest,api)
            result = requests.get(url).json()
            if result['rows'][0]['elements'][0]['status'] == 'NOT_FOUND':
                return bot.say("No clue where that is from.")
            else:
                address = result['destination_addresses'][0]
                miles = result['rows'][0]['elements'][0]['distance']['text']
                duration = result['rows'][0]['elements'][0]['duration']['text']
                traffic = result['rows'][0]['elements'][0]['duration_in_traffic']['text']
                return bot.say("Duration to {0}[{1}]: {2} ({3} in traffic)".format(address,miles,duration,traffic))
    else:
        return bot.say("Not really sure where you are.  Maybe .setlocation again?")

    if x.json()[0]['elements'][0]['status'] == 'NOT_FOUND':
        return bot.say("No clue where that is from")
