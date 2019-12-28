from __future__ import print_function
from tkinter import *
from datetime import datetime
import requests
import json
from PIL import ImageTk, Image
import os
import calendar
from tkinter import font

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request





SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
stop_no = '1327&format=json'

image_dict = {
    'Clear': "./icons/Sun.png",  
    'Clouds': "./icons/Cloud.png",  
    'Rain': "./icons/Rain.png",  
    'Snow': "./icons/Snow.png",   
    'Thunderstorm': "./icons/Storm.png",
    'fog': "./icons/Haze.png", 
    'Mist':"./icons/Haze.png",
	'Smoke':"./icons/Haze.png",
	'Haze':"./icons/Haze.png",
	'Dust':"./icons/Haze.png",
	'Fog':"./icons/Haze.png",
	'Sand':"./icons/Haze.png",
	'Dust':"./icons/Haze.png",
	'Ash':"./icons/Haze.png",
	'Squall':"./icons/Haze.png",
}





class Show_time(Frame):
	def __init__(self, parent, *args, **kwargs):
		Frame.__init__(self, parent, bg='black')
		self.timelab=Label(self)
		self.daylab=Label(self)
		self.datelab=Label(self)
		self.clock()

	def clock(self):
		"""Function that prints the time,date and day"""
		#time variables
		self.time = datetime.now().strftime("%H:%M:%S")
		self.timelab.config(text=self.time,fg="white",bg='black',font=("Helvetica", 44))
		self.timelab.pack(side=TOP, anchor=E)
		
		#day variables
		self.day = datetime.now().strftime('%A')
		self.daylab.config(text=self.day,fg="white",bg='black',font=("Helvetica", 20))
		self.daylab.pack(side=TOP, anchor=E)
		
		#date variable
		self.date = datetime.now().strftime("%b %d, %Y")
		self.datelab.config(text=self.date,fg="white",bg='black',font=("Helvetica", 20))
		self.datelab.pack(side=TOP, anchor=E)

		# run itself again after 1000 ms
		self.after(1000, self.clock)
		 


class Bus(Frame):
	def __init__(self, parent, *args, **kwargs):
		Frame.__init__(self, parent, bg='black')
		self.buslab1=Label(self)
		self.get_times()
		
	def get_times(self):
		#create bus data variables
		self.bus_stop =""
		self.url ='https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?stopid='+stop_no
		self.r = requests.get(self.url)
		
		
		#create variables for time and result keys
		self.timestamp = json.loads(self.r.text)['timestamp']
		self.stop_json =json.loads(self.r.text)['results']
		self.length=len(self.stop_json)
		self.error= json.loads(self.r.text)['errormessage']
		
		#print error message
		if self.error!="":
			error_msg="No Real-time Bus Information Avaialable"
			self.buslab1.config(text=error_msg,fg="white",bg='black',font=("Helvetica", 32),justify='left')
			self.buslab1.pack(side=BOTTOM, anchor=W)
			
		#if no error message displaybus time-table	
		else:
			for  i in range (self.length):
				self.stop = self.stop_json[i]
				if self.stop["duetime"] == 'Due':
					self.bus_stop+=self.stop["route"]+ " " + self.stop["destination"]+ " " + self.stop["duetime"] +  "\n"
				else:	
					self.bus_stop+=self.stop["route"]+ " " + self.stop["destination"]+ " " + self.stop["duetime"] +  "m\n"
				
			self.buslab1.config(text=self.bus_stop,fg="white",bg='black',font=("Helvetica", 24),justify='left')
			self.buslab1.pack(side=BOTTOM, anchor=W)	
			
		self.after(30000, self.get_times) # run itself again after 1000 ms

class Calendar_events(Frame):
	def __init__(self, parent, *args, **kwargs):
		Frame.__init__(self, parent, bg='black') 
		self.callab=Label(self)
		self.main()

	def main(self):
		"""Shows basic usage of the Google Calendar API.
		Prints the start and name of the next 10 events on the user's calendar.
		"""
		cal_txt ='\tUpcoming Events'
		creds = None
		# The file token.pickle stores the user's access and refresh tokens, and is
		# created automatically when the authorization flow completes for the first
		# time.
		if os.path.exists('token.pickle'):
			with open('token.pickle', 'rb') as token:
				creds = pickle.load(token)
		# If there are no (valid) credentials available, let the user log in.
		if not creds or not creds.valid:
			if creds and creds.expired and creds.refresh_token:
				creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file(
					'credentials.json', SCOPES)
				creds = flow.run_local_server(port=0)
			# Save the credentials for the next run
			with open('token.pickle', 'wb') as token:
				pickle.dump(creds, token)

		service = build('calendar', 'v3', credentials=creds)

		# Call the Calendar API
		now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
	
		events_result = service.events().list(calendarId='primary', timeMin=now,
											maxResults=5, singleEvents=True,
											orderBy='startTime').execute()
		events = events_result.get('items', [])
	   
		

		if not events:
			cal_txt ='No upcoming events found.'
		for event in events:
			start = event['start'].get('dateTime', event['start'].get('date'))
		   
				#edit the time information
			
			if start[-1] == 'Z':
				start= start[0:-1]
				d1 = datetime.fromisoformat(start)
				new_format = "%b %d, %Y at %H:%M "
				event_time= d1.strftime(new_format)

			else:
				d1 = datetime.fromisoformat(start)
				new_format = "%b %d, %Y at %H:%M "
				event_time= d1.strftime(new_format)
				
			if 'location' in event:
				location = event['location']
				cal_txt +="\n• "+ event_time +" " + event['summary'] +"\n  "+location
	  
			else:
				cal_txt +="\n• "+ event_time +" " + event['summary'] 
				
		#display calendar events
		self.callab.config(text=cal_txt,fg="white",bg='black',font=("Helvetica", 18),justify='left')
		self.callab.pack(side=BOTTOM, anchor=E)
		
				
				
class Weather(Frame):
	def __init__(self, parent, *args, **kwargs):
		Frame.__init__(self, parent, bg='black')
		
		#initialise weather labels
		self.wlab1=Label(self)
		self.wlab2=Label(self)
		self.wlab3=Label(self)
		
		self.get_weather()
		
	def get_weather(self):
		"""function that requests weather data 
		and prints it in readible format"""
		
		#create weather data variables
		self.url ='http://api.openweathermap.org/data/2.5/weather?id=7778677&appid=9da3d1abfb8e1a3677d26c96350597c3&units=metric'
		self.res = requests.get(self.url)

		self.data = self.res.json()

		self.temp = str(int(self.data['main']['temp']))+"°c"
		self.min = self.data['main']['temp_min']
		self.max = self.data['main']['temp_max']
		
		
		
		self.description = self.data['weather'][0]['description'].capitalize()
		
		#display temperature
		self.wlab1.config(text=self.temp,fg="white",bg='black',font=("Helvetica", 70) ,anchor='e')
		#self.wlab1.pack(side=LEFT, anchor=W)
		self.wlab1.grid(row=0, column=0)
		
		#display weather icons
		wtype= self.data['weather'][0]['main']
		wimage = None
		if wtype in  image_dict:
			 wimage = image_dict[wtype]
			 
		if wimage is not None:
			self.img= Image.open(wimage)
			self.img=self.img.resize((150,150), Image.ANTIALIAS)
			self.img = ImageTk.PhotoImage(self.img)
			self.panel = Label(self, image = self.img,bg='black')
			self.panel.grid(row=0, column=1)
		
		#self.panel.pack(side=TOP,anchor=W)
		
		
		#display description
		self.wlab3.config(text=self.description,fg="white",bg='black',font=("Helvetica", 32))
		self.wlab3.grid(row=1, column=0)
		
class FullscreenWindow:

    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background='black')
        self.topFrame = Frame(self.tk, background = 'black')
        self.bottomFrame = Frame(self.tk, background = 'black')
        self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
        self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
        self.state = False
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        
        # ~ # clock
        self.clock = Show_time(self.topFrame)
        self.clock.pack(side=RIGHT, anchor=N, padx=100, pady=60)
        
        # weather
        self.weather = Weather(self.topFrame)
        self.weather.pack(side=LEFT, anchor=N, padx=100, pady=60)
        # Bus time-table
        self.bus = Bus(self.bottomFrame)
        self.bus.pack(side=LEFT, anchor=S, padx=100, pady=60)
        # calender 
        self.calendar1 = Calendar_events(self.bottomFrame)
        self.calendar1.pack(side=RIGHT, anchor=S, padx=100, pady=60)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"		
			
if __name__ == '__main__':
    w = FullscreenWindow()
    w.tk.mainloop()
