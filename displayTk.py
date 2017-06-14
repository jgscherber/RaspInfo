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

        self.cities = cities
        self.destinations = destinations
        self.locations = None
        # create current weather widget
        self.currentWeather = None # Maintain a reference for killing
        self.createCurrentWeather()

        # create drive time widget
        self.travelTime = None
        #self.createTravel()

        # create hourly weather
        self.dummy = weather.dummyRecord # use for UI testing w/o API calls
        self.hourlyWeather = None
        self.createHourlyWeather()



        self.bind('<Configure>', self.resize)
        self.geometry('500x250')
        self.configure(background='white')

    # CURRENT WEATHER
    def createCurrentWeather(self):
        self.currentWeather = Frame(self, relief='groove', borderwidth=3)
        self.locations = weather.getCurrent(self.cities)
        for loc in self.locations:
            self.createCurrentWidget(self.currentWeather, loc).pack(side='left', fill='both', expand=True)
        self.currentWeather.pack(anchor=NW, fill='both', expand=True)
        self.after(1800000 , self.refreshCurrentWeather) # every 30 min

    def refreshCurrentWeather(self):
        self.currentWeather.destroy()
        self.createCurrentWeather()
        self.after(1800000 , self.refreshCurrentWeather) # every 30 min

    def createCurrentWidget(self, root, location): # takes in a Location object (has current and hourly)
        current = Frame(root, borderwidth=5)
        # City
        Label(current,text = location.city, font = self.titleFont).grid(row=0,column=0,columnspan=2,sticky='SW')
        # Image (need to resize for final
        img = ImageTk.PhotoImage(Image.open(self.file_path + r"\images\\" + location.city + r".jpg"))
        icon = Label(current, image = img)
        icon.image = img
        icon.grid(row=1,column=0,rowspan=2, sticky='E')
        # Current temp
        temperWord = "Currently: " + location.current.temp + "° F"
        Label(current, text = temperWord, font = self.infoFont).grid(row=1,column=1, sticky='SW')
        feelsLikeWord = "Feels Like: " + location.current.feelsLike + "° F"
        Label(current, text=feelsLikeWord, font = self.infoFont).grid(row=2, column=1, sticky='NW')

        return current

    # TRAVEL TIME
    def createTravel(self):
        self.travelTime = Frame(self, relief='groove', borderwidth=3)
        for dest in self.destinations:
            info = getTravelInfo(dest)
            tempLabel = Label(self.travelTime,text = '{0}: {1} - {2}'.format(
                info['destination'],info['summary'],info['time']), font = self.infoFont)
            tempLabel.pack()
        self.travelTime.pack(anchor='sw')
        self.after(600000, self.refreshTravel)  # 10 minutes

    def refreshTravel(self):
        self.travelTime.destroy()
        self.createTravel()
        self.after(600000, self.refreshTravel) # 10 minutes

    # HOURLY WEATHER
    def createHourlyWeather(self):
        self.hourlyWeather = Frame(self, relief ='groove', borderwidth = 3)
        for loc in self.locations:
            tempFrame = Frame(self.hourlyWeather)
            hours = len(loc.hourly)
            current_time = datetime.now() + timedelta(hours=1)
            for hr in range(0,5): # LIMIT NUMBER OF RUN WHEN RESIZING
                rowFrame = Frame(tempFrame)
                current_time = current_time + timedelta(hours=1)
                timeWord = current_time.strftime('%I %p').lstrip('0')
                Label(rowFrame, text = timeWord).grid(row = 0, column = 0)
                img = ImageTk.PhotoImage(Image.open(
                    self.file_path + r"\images\\" + loc.city + r"Hourly" + str(hr) + r".jpg"))
                icon = Label(rowFrame, image=img)
                icon.image = img
                icon.grid(row = 0, column = 1, columnspan = 2)
                Label(rowFrame, text=loc.hourly[hr].temp).grid(row =0, column = hr+3)

                rowFrame.pack()
            tempFrame.pack()
        self.hourlyWeather.pack()






    def resize(self, event):
        windowH=self.winfo_height()
        if(windowH//15 > 30):
            self.titleFont.config(size=30)
            self.infoFont.config(size=15)
        else:
            self.titleFont.config(size=windowH//15)
            self.infoFont.config(size=windowH//30)


# cities = ["Hopkins", "Minneapolis"]
cities = ["Hopkins"]
destinations = ('uofm', 'sps', 'rampA')
root = InfoApp(cities, destinations)
root.mainloop()



# main.attributes('-fullscreen', True)
#main.after(360000, createCurrent, currentWeather, loc)
#main.after(1000, createTravel,travelTime,dest)