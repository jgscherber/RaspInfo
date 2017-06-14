

# get weather for 2 locations in the hourly formats

from urllib.request import urlopen
from urllib.request import urlretrieve
import json, os

base_url = 'http://api.wunderground.com/api/899a5c58cf01f8c8/'
file_path = os.path.dirname(os.path.realpath(__file__))

class Location:
    def __init__(self, city, current, hourly):
        self.city = city
        self.current = current
        self.hourly = hourly # list of Weather objects

class Weather:
    def __init__(self, temp, wind_mph, feelsLike, rainChance, rainAmount, icon_url):
        self.temp = temp
        self.feelsLike = feelsLike
        self.icon_url = icon_url
        self.rainChance = rainChance
        self.rainAmount = rainAmount


def getWeather(city):
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
        weather = Weather(temp, wind_mph, feelsLike, pop, qpf, icon_url)
        if x == 0:
            current_weather = weather
        else:
            hourlyTemps.append(weather)
    return Location(city,current_weather,hourlyTemps)

def getCurrent(locations):
    temp = []
    for loc in locations:
        weather = getWeather(loc)
        urlretrieve(weather.current.icon_url, file_path + r"\images\\" + loc + r".jpg")
        for hr in range(len(weather.hourly)):
            urlretrieve(weather.hourly[hr].icon_url,
                        file_path + r"\images\\" + loc + r"Hourly" + str(hr) + r".jpg")
        temp.append(weather)
    return temp

dummyTemp = []
for i in range(20):
    temp = str(i)
    wind_mph = i
    feelsLike = str(2*i)
    gpf = i / 2
    pop = i / 100
    icon = "http://icons-ak.wxug.com/i/c/k/clear.gif"
    dummyTemp.append( Weather(temp,wind_mph,feelsLike,gpf,pop,icon))
dummyCurr = Weather(0, 10, 0, 0.1, 0.9, " ")
dummyRecord = Location("Nowhere", dummyCurr ,dummyTemp)

