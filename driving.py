
# api defaults to return the most "efficient directions" == fastest usually

import urllib2
import json

base_url = 'https://maps.googleapis.com/maps/api/directions/json?'
home = '10+10+Lake+St+NE+Hopkins+MN+55344'
yanisaWork = '333+S+7th+St+Minneapolis+MN+55402'
rampA = ''
# request
f = urllib2.urlopen(base_url + 'origin=' + home
    + '&destination=' + yanisaWork
    + '&alternatives=true'
    + '&key=AIzaSyBITxDjn0W6T6PqB8BOvizdjq-1skXApX8')
##test = 'https://maps.googleapis.com/maps/api/directions/json?origin=Toronto&destination=Montreal&key=AIzaSyBITxDjn0W6T6PqB8BOvizdjq-1skXApX8'
##f = urllib2.urlopen(test)
json_string = f.read()
f.close()
parsed_json = json.loads(json_string)

# only routes with waypoints have more than one leg
# alternatives may return more than one (not always
summary = parsed_json['routes'][0]['summary']
time = parsed_json['routes'][0]['legs'][0]['duration']['text']
print(summary)
print(time)
summary = parsed_json['routes'][1]['summary']
time = parsed_json['routes'][1]['legs'][0]['duration']['text']

