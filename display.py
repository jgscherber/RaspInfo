
# displays info

import pygame, sys, os
from pygame.locals import *
from urllib.request import urlretrieve

# local imports
from weather import *
from driving import *

# GET INFO
cities = ["Hopkins", "Minneapolis"]
locations = []

def updateCurrent():
    locations = getCurrent(cities)

    # download and save image
    file_path = os.path.dirname(os.path.realpath(__file__))
    for i in range(0, len(locations)):
        urlretrieve(locations[i].current.icon_url, file_path + r"\images\icon" + str(i) + r".png")
    

##school = getTravelInfo('uofm')

# SETUP BACKGROUND
pygame.init()
updateCurrent()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (210, 210, 210)

WINDOW_HEIGHT = 500
WINDOW_WIDTH = 1000
PADDING = WINDOW_WIDTH // 100

MAINSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),0,32) #FULLSCREEN
MAINSURF.fill(WHITE)
pygame.draw.rect(MAINSURF, GRAY,
                 (PADDING, PADDING, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), 3) # width = 0 == filled

pygame.draw.rect(MAINSURF, GRAY,
                 (PADDING, WINDOW_HEIGHT // 2 + 2*PADDING, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 3*PADDING), 3) # width = 0 == filled

# SETUP CURRENT WEATHER

# SETUP HOURLY WEATHER

# SETUP AGENDA

pygame.display.update()



# LOOP (slow clock or clock conditional?)
CLOCK = pygame.time.Clock()
FPS = 1
WEATHER_COUNT = 0
while 1:
    # update every 10 minutes
    WEATHER_COUNT++
    if(WEATHER_COUNT == 600 * FPS):
        WEATHER_COUNT = 0
        updateCurrent()
    
    for event in pygame.event.get(): # returns Eventlist
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    CLOCK.tick(FPS)
    



