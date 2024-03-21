#Mihir Katyal
#mkatyal@uci.edu
#19099879

import urllib.request
import urllib.error
import json
from WebAPI import WebAPI

class OpenWeather(WebAPI):
    def __init__(self, zip_code='92617', country_code='US'):
        super().__init__()
        self.zip_code = zip_code
        self.country_code = country_code
        # Initializing attributes to store weather data
        self.temperature = 0
        self.high_temperature = 0
        self.low_temperature = 0
        self.longitude = 0
        self.latitude = 0
        self.description = ''
        self.humidity = 0
        self.sunset = 0
        self.city = ''

    def load_data(self):
        url = f"http://api.openweathermap.org/data/2.5/weather?zip={self.zip_code},{self.country_code}&appid={self.api_key}&units=metric"
        data = self._download_url(url)
        # Assigning data to attributes
        self.temperature = data['main']['temp']
        self.high_temperature = data['main']['temp_max']
        self.low_temperature = data['main']['temp_min']
        self.longitude = data['coord']['lon']
        self.latitude = data['coord']['lat']
        self.description = data['weather'][0]['description']
        self.humidity = data['main']['humidity']
        self.sunset = data['sys']['sunset']
        self.city = data['name']

    def transclude(self, message: str) -> str:
        if '@weather' in message:
            self.load_data()  # Make sure data is loaded
            weather_data = f"the weather in {self.city} is {self.description} with a temperature of {self.temperature}°C, high of {self.high_temperature}°C, and low of {self.low_temperature}°C."
            message = message.replace('@weather', weather_data)
        return message
