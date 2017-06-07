

# get weather for 2 locations in the hourly formats

from urllib.request import urlopen
import json

base_url = 'http://api.wunderground.com/api/899a5c58cf01f8c8/'

class Location(object):
    def __init__(self, location, current, hourly):
        self.location = location
        self.current = current
        self.hourly = hourly # list of Weather objects

class Weather:
    def __init__(self, temp, wind_mph, feelsLike, rainChance, rainAmount, icon_url):
        self.temp = temp
        self.feelsLike = feelsLike
        self.icon_url = icon_url


def getWeather(city):
    # current weather
    f = urlopen(base_url + 'geolookup/conditions/q/MN/' + city + '.json')
    json_string = f.read()
    parsed_json = json.loads(json_string)
    f.close()
    location = parsed_json['location']['city']
    # parse current
    temp = parsed_json['current_observation']['temperature_string']
    wind_mph = parsed_json['current_observation']['wind_mph']
    feelsLike = parsed_json['current_observation']['feelslike_string']
    icon_url = parsed_json['current_observation']['icon_url']
    pop = icon_url = parsed_json['current_observation']['icon_url']
    current_weather = Weather(temp, wind_mph, feelsLike, 0, pop, icon_url)

    # hourly weather
    f = urlopen(base_url + 'hourly/q/MN/' + city + '.json')
    json_string = f.read()
    parsed_json = json.loads(json_string)
    f.close()
    # parse hourly
    hourly_list = parsed_json['hourly_forecast']
    hourlyTemps = []
    for x in range(0, len(hourly_list) // 2):
        temp = hourly_list[x]['temp']['english']
        wind_mph = hourly_list[x]['wspd']['english']
        feelsLike = hourly_list[x]['feelslike']['english']
        qpf = hourly_list[x]['qpf']['english']
        pop = hourly_list[x]['pop']
        icon_url = hourly_list[x]['icon_url']
        weather = Weather(temp,wind_mph,feelsLike,pop,qpf,icon_url)
        hourlyTemps.append(weather)
    return Location(city,current_weather,hourlyTemps)

def getCurrent(locations):
    temp = []
    for x in locations:
        temp.append(getWeather(x))
    return temp

