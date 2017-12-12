import os

from tkinter import *
from tkinter import font
from datetime import datetime, timedelta
import weather
from driving import *
from PIL import ImageTk, Image

class InfoApp(Tk): # self is the Tk instance
    def __init__(self, cities, destinations):
        Tk.__init__(self)

        self.file_path = os.path.dirname(os.path.realpath(__file__))
        self.titleFont = font.Font(self, family='arial', size=30, weight='bold')
        self.infoFont = font.Font(self, family='arial', size=14)
        self.summaryFont = font.Font(self, family='arial', size=10)

        self.cities = cities
        self.destinations = destinations
        self.locations = None
        # create current weather widget
        self.weatherFrame = None # Maintain a reference for killing
        self.createWeather()

        # create drive time widget
        self.travelTime = None
        self.createTravel()



        self.bind('<Configure>', self.resize)
        self.geometry('1000x500')
        self.configure(background='white')

    # WEATHER
    def createWeather(self):
        self.weatherFrame = Frame(self)
        self.locations = weather.getCurrent(self.cities)
        print('Data Acquired.')
        for loc in self.locations:
            cityFrame = Frame(self.weatherFrame)
            self.createCurrentWidget(cityFrame, loc).pack(fill='both',expand=True)
            self.createHourlyWidget(cityFrame, loc).pack()
            cityFrame.pack(side='left')
        # self.weatherFrame.pack(anchor='nw', fill='both',expand=True)
        self.weatherFrame.grid(row=0,column=0,rowspan=2)
        self.after(1800000, self.refreshWeather)  # every 30 min

    def refreshWeather(self):
        self.weatherFrame.destroy()
        self.createWeather()
        self.after(1800000, self.refreshWeather)  # every 30 min

        # takes in a Location object (has current and hourly)
    def createCurrentWidget(self, root, location): 
        current = Frame(root, bd = 1, relief = 'groove')
        # City
        Label(current,text = location.city, font = self.titleFont).grid(row=0,column=0,columnspan=2,sticky='SW')
        # Image (need to resize for final)
        img = ImageTk.PhotoImage(
            Image.open(self.file_path + r"\images\\" + location.city + r".jpg"))
        icon = Label(current, image = img)
        icon.image = img
        icon.grid(row=1,column=0,rowspan=2, sticky='E')
        # Current temp
        temperWord = "Actual: " + location.current.temp + "° F"
        Label(current, text = temperWord, font = self.infoFont).grid(row=1,column=1, sticky='SW')
        feelsLikeWord = "Feels Like: " + location.current.feelsLike + "° F"
        Label(current, text=feelsLikeWord, font = self.infoFont).grid(row=2, column=1, sticky='NW')

        return current

    def createHourlyWidget(self, root, loc):
        locFrame = Frame(root)
        hours = len(loc.hourly)
        current_time = datetime.now() + timedelta(hours=1)
        # Max of 17 hours pull, change range to set number of hours
        for hr in range(0, 11):  
            rowFrame = Frame(locFrame, bd = 1, relief = 'groove')
            current_time = current_time + timedelta(hours=1)
            timeWord = current_time.strftime('%I %p').lstrip('0')
            Label(rowFrame, text=timeWord).grid(row=0, column=0)
            img = ImageTk.PhotoImage(
                Image.open(self.file_path + r"/images/" + loc.city + r"Hourly" + str(hr) + r".jpg"))
            icon = Label(rowFrame, image=img)
            icon.image = img
            icon.grid(row=0, column=1, columnspan=2, rowspan = 2)
            temperWord = "Actual: " + loc.hourly[hr].temp + "° F"
            Label(rowFrame, text=temperWord).grid(row=0, column= 3)
            feelsLikeWord = "Feels Like: " + loc.hourly[hr].feelsLike + "° F"
            Label(rowFrame, text = feelsLikeWord).grid(row=1, column = 3)
            rainChanceWord = "Rain Chance: " + str(loc.hourly[hr].rainChance) + "%"
            Label(rowFrame, text = rainChanceWord).grid(row=0, column = 4)
            rainAmountWord = "Rain Amount: " + str(loc.hourly[hr].rainAmount) + " in."
            Label(rowFrame, text = rainAmountWord).grid(row=1, column = 4)


            rowFrame.pack()
        return locFrame


    # TRAVEL TIME
    def createTravel(self):
        self.travelTime = Frame(self, relief='groove', borderwidth=3)
        for dest in self.destinations:
            info = getTravelInfo(dest)
            travelHeadLabel = Label(self.travelTime,text = '{0} - {1}'.format(
                info['destination'],info['time']), font = self.infoFont)
            travelInfoLabel = Label(self.travelTime, text = info['summary'], font = self.summaryFont)
            travelHeadLabel.pack()
            travelInfoLabel.pack()
        self.travelTime.grid(row=0,column=1,sticky=N)
        self.after(600000, self.refreshTravel)  # 10 minutes

    def refreshTravel(self):
        self.travelTime.destroy()
        self.createTravel()
        # set event to refresh after 10 minutes
        self.after(600000, self.refreshTravel)
        
    def resize(self, event):
        windowH=self.winfo_height()
        if(windowH//15 > 30):
            self.titleFont.config(size=30)
            self.infoFont.config(size=15)
        else:
            self.titleFont.config(size=windowH//15)
            self.infoFont.config(size=windowH//30)


cities = ["Hopkins", "Minneapolis"]
# cities = ["Hopkins"]
destinations = ('uofm', 'sps', 'rampA')
root = InfoApp(cities, destinations)
root.mainloop()



# main.attributes('-fullscreen', True)
#main.after(360000, createCurrent, currentWeather, loc)
#main.after(1000, createTravel,travelTime,dest)
