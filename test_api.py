#Mihir Katyal
#mkatyal@uci.edu
#19099879

from OpenWeather import OpenWeather
from LastFM import LastFM
from WebAPI import WebAPI

def test_api(message: str, apikey: str, webapi: WebAPI):
    webapi.set_apikey(apikey)
    webapi.load_data()
    result = webapi.transclude(message)
    print(result)

if __name__ == "__main__":
    open_weather_api_key = '6aff17baf0c23f582c0d2028522c3d03'
    lastfm_api_key = '43effd57c3bbcfc8d88897c50b1cb0cf'
    
    open_weather = OpenWeather()  # Utilizes default parameters
    lastfm = LastFM("default_user")  
    
    # Testing OpenWeather
    test_api("Testing the weather: @weather", open_weather_api_key, open_weather)
    
    # Testing LastFM
    test_api("Testing lastFM: @lastfm", lastfm_api_key, lastfm)
