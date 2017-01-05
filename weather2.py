# coding=utf-8
# Copyright 2008, Sean B. Palmer, inamidst.com
# Copyright 2012, Elsie Powell, embolalia.com
# Licensed under the Eiffel Forum License 2.
# A modification of sopel's weather.py after it was broken by yahoo's requirement for oauth authentication 
# This module requires api keys for darksky.net and google url shortener
# This can be cleaned up a lot and made more efficient.
from __future__ import unicode_literals, absolute_import, print_function, division
import requests
import json
from sopel import web
from sopel.module import commands, example, NOLIMIT
from datetime import datetime
from pytz import timezone

forecastapi = '' #darksky.net API key.
gurlapi = '' #google url shortner api key

def get_short_url(gurl):
    global gurlapi
    short_url_service = 'https://www.googleapis.com/urlshortener/v1/url?key={0}'.format(gurlapi)
    payload = {'longUrl': gurl}
    headers = {'content-type': 'application/json'}
    r = requests.post(short_url_service, data=json.dumps(payload), headers=headers)
    return r.json()['id']

def woeid_search(query):
    """
    Find the first Where On Earth ID for the given query. Result is the etree
    node for the result, so that location data can still be retrieved. Returns
    None if there is no result, or the woeid field is empty.
    """
    query = 'q=select * from geo.places where text="%s"&format=json' % query
    body = requests.get('http://query.yahooapis.com/v1/public/yql?' + query)
    return body

def reversewoeid_search(query):
    """
    Find the first Where On Earth ID for the given query. Result is the etree
    node for the result, so that location data can still be retrieved. Returns
    None if there is no result, or the woeid field is empty.
    """
    query = 'q=select * from geo.places where woeid="%s"&format=json' % query
    body = requests.get('http://query.yahooapis.com/v1/public/yql?' + query)
    return body

def get_temp(forecast):
    try:
        temp = round(forecast.json()['currently']['temperature'])
        app_temp = round(forecast.json()['currently']['apparentTemperature'])
    except (KeyError, ValueError):
        return 'unknown'
    high = round(forecast.json()['daily']['data'][0]['temperatureMax'])
    low = round(forecast.json()['daily']['data'][0]['temperatureMin'])
    if forecast.json()['flags']['units'] == 'us':
        if temp == app_temp:
            return (u'%d\u00B0F (H:%d|L:%d)' % (temp, high, low))
        else:
            return (u'%d\u00B0F, (App:%d, H:%d|L:%d)' % (temp, app_temp, high, low))
    else:
        if temp == app_temp:
            return (u'%d\u00B0C (H:%d|L:%d)' % (temp, high, low))
        else:
            return (u'%d\u00B0C, (App:%d, H:%d|L:%d)' % (temp, app_temp, high, low))
    
def get_wind(forecast):
    try:
        if forecast.json()['flags']['units'] == 'us':
            wind_data = forecast.json()['currently']['windSpeed']
            kph = float(wind_data / 0.62137)
            m_s = float(round(wind_data, 1))
            speed = int(round(kph / 1.852, 0))
            unit = 'mph'
        elif forecast.json()['flags']['units'] == 'si':
            wind_data = forecast.json()['currently']['windSpeed']
            m_s = float(wind_data)
            kph = float(m_s * 3.6)
            speed = int(round(kph / 1.852, 0))
            unit = 'm/s'
        elif forecast.json()['flags']['units'] == 'ca':
            wind_data = forecast.json()['currently']['windSpeed']
            kph = float(wind_data)
            m_s = float(round(kph / 3.6, 1))
            speed = int(round(kph / 1.852, 0))
            unit = 'm/s'
        else:
            wind_data = forecast.json()['currently']['windSpeed']
            kph = float(wind_data / 0.62137)
            m_s = float(round(wind_data, 1))
            speed = int(round(kph / 1.852, 0))
            unit = 'mph'
        degrees = int(forecast.json()['currently']['windBearing'])
    except (KeyError, ValueError):
        return 'unknown'
    if speed < 1:
        description = 'Calm'
    elif speed < 4:
        description = 'Light air'
    elif speed < 7:
        description = 'Light breeze'
    elif speed < 11:
        description = 'Gentle breeze'
    elif speed < 16:
        description = 'Moderate breeze'
    elif speed < 22:
        description = 'Fresh breeze'
    elif speed < 28:
        description = 'Strong breeze'
    elif speed < 34:
        description = 'Near gale'
    elif speed < 41:
        description = 'Gale'
    elif speed < 48:
        description = 'Strong gale'
    elif speed < 56:
        description = 'Storm'
    elif speed < 64:
        description = 'Violent storm'
    else:
        description = 'Hurricane'
    if (degrees <= 22.5) or (degrees > 337.5):
        degrees = u'\u2193'
    elif (degrees > 22.5) and (degrees <= 67.5):
        degrees = u'\u2199'
    elif (degrees > 67.5) and (degrees <= 112.5):
        degrees = u'\u2190'
    elif (degrees > 112.5) and (degrees <= 157.5):
        degrees = u'\u2196'
    elif (degrees > 157.5) and (degrees <= 202.5):
        degrees = u'\u2191'
    elif (degrees > 202.5) and (degrees <= 247.5):
        degrees = u'\u2197'
    elif (degrees > 247.5) and (degrees <= 292.5):
        degrees = u'\u2192'
    elif (degrees > 292.5) and (degrees <= 337.5):
        degrees = u'\u2198'
    return description + ' ' + str(m_s) + unit + '(' + degrees + ')'

def get_alert(forecast):
    try:
        if forecast.json()['alerts'][0]:
            title = forecast.json()['alerts'][0]['title']
            alert = get_short_url(forecast.json()['alerts'][0]['uri'])
            return 'Alert: ' + title + ' ' + alert
        else:
            return ''
    except:
        return ''        

def get_forecast(bot,trigger,location=None):
    global forecastapi
    forecast,woeid,body,first_result,alert,result,error = '','','','','','',''
    if not location:
        woeid = bot.db.get_nick_value(trigger.nick, 'woeid')
        if not woeid:
            bot.msg(trigger.sender, "I don't know where you live. " +
                           'Give me a location, like .weather London, or tell me where you live by saying .setlocation London, for example.')
            error = 'yes'
            return location, forecast, error
        body = reversewoeid_search(woeid)
        result = body.json()['query']['results']['place']
        longlat = result['centroid']['latitude']+","+result['centroid']['longitude']
    else:
        location = location.strip()
        longlat = None
        woeid = bot.db.get_nick_value(location, 'woeid')
        if woeid is None:
            first_result = woeid_search(location)
            result = first_result.json()['query']['results']['place']
            if type(result) is list:
                woeid = 'filler'
                longlat = result[0]['centroid']['latitude']+","+result[0]['centroid']['longitude']
            else:
                woeid = 'filler'
                longlat = result['centroid']['latitude']+","+result['centroid']['longitude']
    if not woeid:
        bot.reply("I don't know where that is.")
        error = 'yes'
        return location,forecast, error
    forecast = requests.get('https://api.darksky.net/forecast/{0}/{1}?units=auto'.format(forecastapi,longlat))
    if body:
        result = body.json()['query']['results']['place']
        if result['locality1']:
            location = result['locality1']['content'] + ", " + (result['admin1']['code'].split("-")[-1] if result['admin1']['code'] != '' else result['country']['content'])
        else:
            location = result['admin2']['content'] + ", " + (result['admin1']['code'].split("-")[-1] if result['admin1']['code'] != '' else result['country']['content'])
    else:
        result = first_result.json()['query']['results']['place']
        if type(result) is list:
            if result[0]['locality1']:
                location = result[0]['locality1']['content'] + ", " + (result[0]['admin1']['code'].split("-")[-1] if result[0]['admin1']['code'] != '' else result[0]['country']['content'])
            elif result[0]['admin2']:
                location = result[0]['admin2']['content'] + ", " + (result[0]['admin1']['code'].split("-")[-1] if result[0]['admin1']['code'] != '' else result[0]['country']['content'])
            elif result[0]['admin1']:
                location = result[0]['admin1']['content'] + ", " + result[0]['country']['content']
            else:
                location = result[0]['name']
        else:
            if result['locality1']:
                location = result['locality1']['content'] + ", " + (result['admin1']['code'].split("-")[-1] if result['admin1']['code'] != '' else result['country']['content'])
            elif result['admin2']:
                location = result['admin2']['content'] + ", " + (result['admin1']['code'].split("-")[-1] if result['admin1']['code'] != '' else result['country']['content'])
            elif result['admin1']:
                location = result['admin1']['content'] + ", " + result['country']['content']
            else:
                location = result['name']
    return location, forecast, error
    
def get_sun(tz, forecast):
    if 'sunriseTime' not in forecast:
      return ""
    sunrise = datetime.fromtimestamp(forecast['sunriseTime'], tz=timezone(tz)).strftime('%H:%M')
    sunset = datetime.fromtimestamp(forecast['sunsetTime'], tz=timezone(tz)).strftime('%H:%M')
    return ", \u2600 \u2191 " + sunrise + " \u2193 " + sunset

@commands('weather7', 'wea7')
@example('.weather7 London')
def weather7(bot,trigger):
    location = trigger.group(2)
    if not location:
        location, forecast, error = get_forecast(bot,trigger)
    else:
        location, forecast, error = get_forecast(bot,trigger,location)
    if error:
        return
    summary = forecast.json()['daily']['summary']
    sevendays = []
    weekdays = {1:'M',2:'Tu',3:'W',4:'Th',5:'F',6:'Sa',7:'Su'}
    for day in forecast.json()['daily']['data']:
        wkday = weekdays[datetime.fromtimestamp(int(day['time'])).isoweekday()]
        maxtemp = round(day['temperatureMax'])
        mintemp = round(day['temperatureMin'])
        sevendays.append("{0}:({1}|{2})".format(wkday,mintemp,maxtemp))
    del sevendays[0]
    sevendays = ", ".join(sevendays)
    bot.say("{0}: [{1}] {2}".format(location, summary, str(sevendays)))

@commands('weather', 'wea')
@example('.weather London')
def weather(bot, trigger):
    """.weather location - Show the weather at the given location."""
    location = trigger.group(2)
    if not location:
        location, forecast, error = get_forecast(bot,trigger)
    else:
        location, forecast, error = get_forecast(bot,trigger,location)
    if error:
        return
    summary = forecast.json()['currently']['summary']
    temp = get_temp(forecast)
    humidity = forecast.json()['currently']['humidity']
    wind = get_wind(forecast)
    alert = get_alert(forecast)
    sun = get_sun(forecast.json()['timezone'], forecast.json()['daily']['data'][0])
    bot.say(u'%s: %s, %s, Humidity: %s%%, %s %s %s' % (location, summary, temp, round(humidity*100), wind, sun, alert))

@commands('setlocation', 'setwoeid')
@example('.setlocation Columbus, OH')
def update_woeid(bot, trigger):
    """Set your default weather location."""
    if not trigger.group(2):
        bot.reply('Give me a location, like "Washington, DC" or "London".')
        return NOLIMIT
    first_result = woeid_search(trigger.group(2))
    if first_result is None:
        return bot.reply("I don't know where that is.")
    if type(first_result.json()['query']['results']['place']) is list:
        found = first_result.json()['query']['results']['place'][0]
    else:
        found = first_result.json()['query']['results']['place']
    woeid = found['woeid']
    bot.db.set_nick_value(trigger.nick, 'woeid', woeid)
    neighborhood = found['locality2'] or ''
    if neighborhood:
        neighborhood = neighborhood['#text'] + ', '
    city = found['locality1'] or ''
    # This is to catch cases like 'Bawlf, Alberta' where the location is
    # thought to be a "LocalAdmin" rather than a "Town"
    if city:
        city = city['content']
    else:
        city = found['name']
    state = found['admin1']['content'] or ''
    country = found['country']['content'] or ''
    uzip = found['postal'] or ''
    if uzip:
        uzip = uzip['content']
    bot.reply('I now have you at WOEID %s (%s%s, %s, %s %s)' %
              (woeid, neighborhood, city, state, country, uzip))
