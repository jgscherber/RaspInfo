
# displays info
# library imports
import pygame, sys, os
from pygame.locals import *
from urllib.request import urlretrieve

# local imports
import weather
import driving

# should include command line for testing (load local vs. get new)

cities = ["Hopkins", "Minneapolis"]
locations = []
file_path = os.path.dirname(os.path.realpath(__file__))

# SETUP BACKGROUND
pygame.init()               
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (210, 210, 210)

WINDOW_HEIGHT = 500
WINDOW_WIDTH = 1000
PADDING = WINDOW_WIDTH // 100

# Fullscreen
MAIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
MAIN.fill(WHITE)

pygame.draw.rect(MAIN, GRAY,
                 (PADDING, PADDING, WINDOW_WIDTH // 2,
                  WINDOW_HEIGHT // 2), 3) # width = 0 == filled

# width = 0 --> filled
pygame.draw.rect(MAIN, GRAY,
                 (PADDING, WINDOW_HEIGHT // 2 + 2*PADDING,
                  WINDOW_WIDTH // 2,
                  WINDOW_HEIGHT // 2 - 3*PADDING), 3) 

# GET INFO
def updateCurrent():
    global locations
    locations = weather.getCurrent(cities)

    # download and save image
    global file_path
    for i in range(0, len(locations)):
        urlretrieve(locations[i].current.icon_url,
                    file_path + r"/images/icon" + str(i) + r".png")
    

school = driving.getTravelInfo('uofm')

# SETUP CURRENT WEATHER
updateCurrent()
nCities = len(cities)
FONT = pygame.font.SysFont('arial',WINDOW_HEIGHT // 20)


ICON_SIZE = ((WINDOW_HEIGHT // 2) // nCities+1 ) - 2*PADDING
weatherImgX = 2*PADDING + 3
weatherImgY = 2*PADDING + 3


cityTitles = []
images = []

# load images into surfaces
def loadCurrentImages():
    global cityTitles, images

    for i in range(0, nCities):
        # icons should be saved by updateCurrent()
        img = pygame.image.load(file_path +
                                r"/images/icon" + str(i) + r".png")
        img = pygame.transform.scale(img, (ICON_SIZE, ICON_SIZE))
        images.append(img)

        # not sure what this does...
        tempSurf = FONT.render(cities[i], True, BLACK)
        cityTitles.append(tempSurf)



# place images and titles
maxCityLength = 0
def placeCurrentImages():
    global weatherImgX, weatherImgY, maxCityLength, cityTitles, images
    for i in range(0, nCities):
        img = images[i]
        MAIN.blit(img, (weatherImgX, weatherImgY))
        titleRect = cityTitles[i].get_rect()
        titleRect.topleft = (weatherImgX, weatherImgY)
        if(titleRect.width > maxCityLength):
            maxCityLength = titleRect.width
        MAIN.blit(cityTitles[i], titleRect)
        weatherImgY += ICON_SIZE + PADDING



# descriptions
descX = weatherImgX + maxCityLength + 3*PADDING
descY = 2*PADDING + 3
for loc in locations:
    currentDescriptions = FONT.render(loc.current.temp, True, BLACK)
    descRect = currentDescriptions.get_rect()
    descRect.topleft = (descX,descY)
    MAIN.blit(currentDescriptions,descRect)
    descY += ICON_SIZE + PADDING
# SETUP HOURLY WEATHER

# SETUP AGENDA

loadCurrentImages()
placeCurrentImages()

pygame.display.update()



# LOOP (slow clock or clock conditional?)
CLOCK = pygame.time.Clock()
FPS = 1
WEATHER_COUNT = 0
while 1:
    # update every 10 minutes
    WEATHER_COUNT += 1
    if(WEATHER_COUNT == 600 * FPS):
        WEATHER_COUNT = 0
        updateCurrent()
    
    for event in pygame.event.get(): # returns Eventlist
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    CLOCK.tick(FPS)
    



