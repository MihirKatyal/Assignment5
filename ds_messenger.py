import time
from ds_protocol import join, directmessage_send, directmessage_request, extract_msg
import requests  # Use the standard requests module
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
        self.token = None

    def authenticate(self):
        try:
            response = requests.post(f'http://{self.dsuserver}:3021/join', json={"username": self.username, "password": self.password})
            if response.status_code == 200:
                response_json = response.json()
                if 'token' in response_json:
                    self.token = response_json['token']
                    return True
                else:
                    print("Authentication failed: 'token' not in response")
            else:
                print(f"Authentication failed with status code {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        except json.JSONDecodeError:
            print(f"Failed to decode JSON from response: {response.text}")
        return False

    def send(self, message: str, recipient: str) -> bool:
        if self.token is None:
            if not self.authenticate():
                return False
        json_message = directmessage_send(self.token, message, recipient)
        response = requests.post(f'http://{self.dsuserver}:3021/send', json=json_message)
        data = extract_msg(response.text)
        return data.type == 'ok'

    def retrieve_new(self) -> list:
        if self.token is None:
            if not self.authenticate():
                return []
        json_request = directmessage_request(self.token, 'new')
        response = requests.post(f'http://{self.dsuserver}:3021/retrieve', json=json_request)
        data = extract_msg(response.text)
        if data.type == 'ok':
            return [DirectMessage(recipient=msg['from'], message=msg['message'], timestamp=msg['timestamp']) for msg in data.messages]
        return []

    def retrieve_all(self) -> list:
        if self.token is None:
            if not self.authenticate():
                return []
        json_request = directmessage_request(self.token, 'all')
        response = requests.post(f'http://{self.dsuserver}:3021/retrieve', json=json_request)
        data = extract_msg(response.text)
        if data.type == 'ok':
            return [DirectMessage(recipient=msg['from'], message=msg['message'], timestamp=msg['timestamp']) for msg in data.messages]
        return []
