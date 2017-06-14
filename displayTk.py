import os

from tkinter import *
from tkinter import font
from weather import *
from driving import *
from PIL import ImageTk, Image

class InfoApp(Tk): # self is the Tk instance
    def __init__(self, cities, destinations):
        Tk.__init__(self)

        self.file_path = os.path.dirname(os.path.realpath(__file__))
        self.titleFont = font.Font(self, family='arial', size=30, weight='bold')
        self.infoFont = font.Font(self, family='arial', size=14)

        self.cities = cities
        self.destinations = destinations
        # create current weather widget
        self.currentWeather = None # Maintain a reference for killing
        self.createCurrentWeather()

        # create drive time widget
        travelTime = Frame(self, relief='groove', borderwidth=3)
        for dest in destinations:
            self.createTravel(travelTime, dest).pack(anchor='w')

        travelTime.pack(anchor='sw')

        self.bind('<Configure>', self.resize)
        self.geometry('500x250')
        self.configure(background='white')

    def createCurrentWeather(self):
        self.currentWeather = Frame(self, relief='groove', borderwidth=3)
        locations = self.downloadCurrentWeather()
        for loc in locations:
            self.createCurrentWidget(self.currentWeather, loc).pack(side='left', fill='both', expand=True)
        self.currentWeather.pack(anchor=NW, fill='both', expand=True)
        self.after(1800000 , self.refreshCurrentWeather) # every 30 min

    def refreshCurrentWeather(self):
        self.currentWeather.destroy()
        self.createCurrentWeather()
        self.after(1800000 , self.refreshCurrentWeather) # every 30 min

    def downloadCurrentWeather(self):
        return getCurrent(self.cities)

    def createCurrentWidget(self, root, location): # takes in a Location object (has current and hourly)
        current = Frame(root, borderwidth=5)
        # City
        title = Label(current,text = location.city, font = self.titleFont)
        title.grid(row=0,column=0,columnspan=2,sticky='SW')
        # Image (need to resize for final
        img = ImageTk.PhotoImage(Image.open(self.file_path + r"\images\\" + location.city + r".jpg"))
        icon = Label(current, image = img)
        icon.image = img
        icon.grid(row=1,column=0,rowspan=3, sticky='W')
        # Current temp
        temp = Label(current, text = location.current.temp, font = self.infoFont)
        temp.grid(row=1,column=1, sticky='WN')
        feelsLikeWord = Label(current, text='Feels Like:', font = self.infoFont)
        feelsLikeWord.grid(row=2, column=1, sticky='WS')
        feelsLike = Label(current, text=location.current.feelsLike, font = self.infoFont)
        feelsLike.grid(row=3, column=1, sticky='W')

        return current

    def createTravel(self, root, destination):
        info = getTravelInfo(destination)
        return Label(root,text = '{0}: {1} - {2}'.format(
            info['destination'],info['summary'],info['time']), font = self.infoFont)

    def resize(self, event):
        windowH=self.winfo_height()
        if(windowH//15 > 30):
            self.titleFont.config(size=30)
            self.infoFont.config(size=15)
        else:
            self.titleFont.config(size=windowH//15)
            self.infoFont.config(size=windowH//30)


cities = ["Hopkins", "Minneapolis"]
destinations = ('uofm', 'sps', 'rampA')
root = InfoApp(cities, destinations)
root.mainloop()



# main.attributes('-fullscreen', True)
#main.after(360000, createCurrent, currentWeather, loc)
#main.after(1000, createTravel,travelTime,dest)