
# api defaults to return the most "efficient directions" == fastest usually

import googlemaps
from datetime import datetime, timedelta



def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

# this should be read from a file
locList = {'home': ('Home', '10+10+Lake+St+NE+Hopkins+MN+55344'),
            'sps': ('SPS Commerce','333+S+7th+St+Minneapolis+MN+55402'),
            'rampA':('Ramp A','44.979107,-93.278767'),
            'uofm':('U of M','Marcy-Holmes,+Minneapolis,+MN')
            }
def getTravelInfo(location: str) -> dict:
    # request
    gmaps = googlemaps.Client(key='AIzaSyBITxDjn0W6T6PqB8BOvizdjq-1skXApX8')
    fifteenMin = datetime.now() + timedelta(minutes=15)

    # alternatives may return more than one (not always)
    # returns list of routes (?)
    directions = gmaps.directions(locList['home'][1],
                                  locList[location][1],
                                  mode='driving',
                                  traffic_model='best_guess',
                                  departure_time=fifteenMin)[0]

    # directions keys:
    # (['bounds', 'copyrights', 'legs', 'overview_polyline', 'summary',
    #   'warnings', 'waypoint_order'])
    # legs keys
    # ['distance', 'duration', 'duration_in_traffic', 'end_address',
    #  'end_location', 'start_address', 'start_location', 'steps',
    #  'traffic_speed_entry', 'via_waypoint'])
    # for l in directions['legs'][0]['steps']:
    #     print(str(l['html_instructions']))

    # TODO handle multiple options (legs > 0)
    steps = directions['legs'][0]['steps']
    cleanSteps = []
    time = directions['legs'][0]['duration']['text']
    # drop first couple and last couple steps
    for i in range(2, len(steps)-1):
        # remove tags from html descriptions
        line = steps[i]['html_instructions']
        end = 0
        for j in range(len(line)-1,-1,-1):
            if(line[j] == '>'):
                end = j
            if(line[j]== '<'):
                line = line[0:j] + line[end+1:]
        cleanSteps.append(line)
    # return as block string for input into frame
    summary = "\n".join(cleanSteps)
    return {'destination':locList[location][0],'summary':summary, 'time':time}


