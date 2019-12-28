This script displays the time, date, weather, calendar and Dublin bus real time information.


# Install all python modules
download the modules using pip
just enter this line into your command prompt

pip install tk pillow requests --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

# Setup Google Calendar
go to the following link to setup your own google calendar api.
remember to copy the credentials.json file into this folder.<br>
https://developers.google.com/calendar/quickstart/python

# Setup weather
go to the folowing link to sign up for weather api <br>
https://home.openweathermap.org/users/sign_up

once signed in go to API keys
copy the key.

Then go to this link<br>
https://openweathermap.org/current

To set the weather to your city change the city name and country address eg Boston,us.
Then change the key  which in this case is 'b6907d289e10d714a6e88b30761fae22' to your own key

sample of the url in imperial:<br>
api.openweathermap.org/data/2.5/weather?q=London,uk&appid=b6907d289e10d714a6e88b30761fae22&units=imperial

sample in metric:<br>
api.openweathermap.org/data/2.5/weather?q=London&appid=b6907d289e10d714a6e88b30761fae22&units=imperial

For more specific weather use city id <br>
Then copy the full link and paste it  on line 204 of  smart_mirror.py<br>
self.url ='api.openweathermap.org/data/2.5/weather?q=London&appid=b6907d289e10d714a6e88b30761fae22&units=imperial'

# Setup Dublin bus 
Edit the line 22  with your own specific bus stop number ie "stop_no = '1329&format=json'"

# The display
![Smart Mirror](https://i.imgur.com/iEqfpd7.png)
