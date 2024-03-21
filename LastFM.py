#Mihir Katyal
#mkatyal@uci.edu
#19099879

import urllib.request
import urllib.error
import json
from WebAPI import WebAPI

class LastFM(WebAPI):
    def __init__(self, user: str):
        super().__init__()
        self.user = user
        # Initialize attributes to store top tracks data
        self.top_tracks = []

    def load_data(self):
        if not self.api_key:
            raise ValueError("API key is not set.")

        url = f"http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&user={self.user}&api_key={self.api_key}&format=json&limit=5"
        try:
            data = self._download_url(url)
            # Processing and storing top tracks data
            self.top_tracks = [(track['name'], track['playcount']) for track in data['toptracks']['track']]
        except urllib.error.URLError as e:
            raise ConnectionError("There was an error connecting to the internet or the API URL was incorrect.")
        except urllib.error.HTTPError as e:
            raise ConnectionError(f"HTTP error encountered: {e.code}")
        except json.JSONDecodeError:
            raise ValueError("Error processing JSON data from API.")
        except KeyError:
            raise ValueError("Incomplete or incorrect data received from API.")
        
    def transclude(self, message: str) -> str:
        if '@lastfm' in message:
            self.load_data()  # Ensure data is loaded
            if self.top_tracks:
                top_tracks_str = ', '.join([f"'{name}' (Playcount: {playcount})" for name, playcount in self.top_tracks])
                message = message.replace('@lastfm', f"Top LastFM tracks: {top_tracks_str}")
            else:
                message = message.replace('@lastfm', "No top LastFM tracks available.")
        return message
