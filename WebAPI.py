#Mihir Katyal
#mkatyal@uci.edu
#19099879

import urllib.request
import urllib.error
import json
from abc import ABC, abstractmethod

class WebAPI(ABC):
    def __init__(self, api_key=None):
        self.api_key = api_key

    def _download_url(self, url: str) -> dict:
        if not self.api_key:
            raise ValueError("API key is not set.")
        try:
            response = urllib.request.urlopen(url)
            data = json.loads(response.read())
            return data
        except urllib.error.URLError as e:
            raise ConnectionError("There was an error connecting to the internet or the API URL was incorrect.")
        except urllib.error.HTTPError as e:
            raise ConnectionError(f"HTTP error encountered: {e.code}")
        except json.JSONDecodeError:
            raise ValueError("Error processing JSON data from API.")

    def set_apikey(self, apikey: str) -> None:
        self.api_key = apikey

    @abstractmethod
    def load_data(self):
        pass

    @abstractmethod
    def transclude(self, message: str) -> str:
        pass
