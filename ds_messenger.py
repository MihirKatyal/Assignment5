import time
from ds_protocol import join, directmessage_send, directmessage_request, extract_msg
import pip._vendor.requests 

class DirectMessage:
    def __init__(self, recipient=None, message=None, timestamp=None):
        self.recipient = recipient
        self.message = message
        self.timestamp = timestamp

class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.token = None # the token will be set after you have successfully joined the server

    def authenticate(self):
        # Authenticate with the server
        response = pip._vendor.requests.post(f'http://{self.dsuserver}/join', data=join(self.username, self.password))
        self.token = response.json()['token']