import os

from tkinter import *
from tkinter import font
from weather import *
from driving import *
from urllib.request import urlretrieve
from PIL import ImageTk, Image


file_path = os.path.dirname(os.path.realpath(__file__))


def updateCurrent(locList):
    # get info
    locList = getCurrent(cities)

    # download and save image
    for i in range(len(locList)):
        urlretrieve(locList[i].current.icon_url, file_path + r"\images\\" + locList[i].city + r".jpg")
    return locList

def createCurrent(root, location): # takes in a Location object (has current and hourly)
    current = Frame(root, borderwidth=5)
    # City
    title = Label(current,text = location.city, font = titleFont)
    title.grid(row=0,column=0,columnspan=2,sticky='SW')
    # Image
    img = ImageTk.PhotoImage(Image.open(file_path + r"\images\\" + location.city + r".jpg"))
    icon = Label(current, image = img)
    icon.image = img
    icon.grid(row=1,column=0,rowspan=3, sticky='W')
    # Current temp
    temp = Label(current, text = location.current.temp, font = infoFont)
    temp.grid(row=1,column=1, sticky='WN')
    feelsLikeWord = Label(current, text='Feels Like:', font = infoFont)
    feelsLikeWord.grid(row=2, column=1, sticky='WS')
    feelsLike = Label(current, text=location.current.feelsLike, font = infoFont)
    feelsLike.grid(row=3, column=1, sticky='W')

    return current

def createTravel(root, destination):
    info = getTravelInfo(destination)
    return Label(root,text = '{0}: {1} - {2}'.format(
        info['destination'],info['summary'],info['time']), font = infoFont)

def resize(event):
    windowH=main.winfo_height()
    if(windowH//15 > 30):
        titleFont.config(size=30)
        infoFont.config(size=15)
    else:
        titleFont.config(size=windowH//15)
        infoFont.config(size=windowH//30)

main = Tk()

titleFont = font.Font(main,family='arial',size=30,weight='bold')
infoFont = font.Font(main, family='arial',size=14)



cities = ["Hopkins", "Minneapolis"]
# cities = ["Hopkins"]
locations = updateCurrent(cities)

currentWeather = Frame(main,relief = 'groove',borderwidth=3)
for loc in locations:
    createCurrent(currentWeather, loc).pack(side='left', fill = 'both',expand=True)
# fill both directions
currentWeather.pack(anchor=NW, fill = 'both',expand=True)

destinations = ('uofm','sps','rampA')
travelTime = Frame(main,relief='groove',borderwidth=3)
for dest in destinations:
    createTravel(travelTime, dest).pack()

travelTime.pack(anchor='sw')


main.bind('<Configure>',resize)
main.geometry('500x250')
main.configure(background='white')
# main.attributes('-fullscreen', True)
main.mainloop()