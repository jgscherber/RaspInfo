
# api defaults to return the most "efficient directions" == fastest usually

import urllib2
import json

base_url = 'https://maps.googleapis.com/maps/api/directions/json?'
locations = {'home':'10+10+Lake+St+NE+Hopkins+MN+55344',
            'sps':'333+S+7th+St+Minneapolis+MN+55402',
            'rampA':'44.979107,-93.278767',
            'uofm':'Marcy-Holmes,+Minneapolis,+MN'}
def getTravelInfo(location):
    # request
    f = urllib2.urlopen(base_url + 'origin=' + locations['home']
        + '&destination=' + locations[location]
        + '&key=AIzaSyBITxDjn0W6T6PqB8BOvizdjq-1skXApX8')

    json_string = f.read()
    f.close()
    parsed_json = json.loads(json_string)

    # only routes with waypoints have more than one leg
    # alternatives may return more than one (not always
    summary = parsed_json['routes'][0]['summary']
    time = parsed_json['routes'][0]['legs'][0]['duration']['text']
    return {'summary':summary, 'time':time}


