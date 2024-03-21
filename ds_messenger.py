import time
from ds_protocol import join, directmessage_send, directmessage_request, extract_msg
import pip._vendor.requests  # Changed from pip._vendor.requests to requests for standard usage
import json

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
        self.token = None  # the token will be set after you have successfully joined the server

    def authenticate(self):
        try:
            response = pip._vendor.requests.post(f'https://{self.dsuserver}/join', json={"username": self.username, "password": self.password})
            if response.status_code == 200:
                response_json = response.json()
                if 'token' in response_json:
                    self.token = response_json['token']
                    return True
                else:
                    print("Authentication failed: 'token' not in response")
            else:
                print(f"Authentication failed with status code {response.status_code}: {response.text}")
        except pip._vendor.requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        except json.JSONDecodeError:
            print(f"Failed to decode JSON from response: {response.text}")
        return False

    def send(self, message: str, recipient: str) -> bool:
        # Send a message
        if self.token is None:
            if not self.authenticate():
                return False
        json_message = directmessage_send(self.token, message, recipient)
        response = pip._vendor.requests.post(f'https://{self.dsuserver}/send', data=json_message)
        data = extract_msg(response.text)
        return data.type == 'ok'

    def retrieve_new(self) -> list:
        # Retrieve new messages
        return self._retrieve_messages('new')

    def retrieve_all(self) -> list:
        # Retrieve all messages
        return self._retrieve_messages('all')

    def _retrieve_messages(self, msg_type: str) -> list:
        # Retrieve messages helper function
        if self.token is None:
            if not self.authenticate():
                return []
        json_request = directmessage_request(self.token, msg_type)
        response = pip._vendor.requests.post(f'https://{self.dsuserver}/retrieve', data=json_request)
        data = extract_msg(response.text)
        if data.type == 'ok':
            return [DirectMessage(msg['from_user'], msg['message'], msg['timestamp']) for msg in data.messages]
        return []