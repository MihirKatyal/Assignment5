#Mihir Katyal
#mkatyal@uci.edu
#19099879

import socket
import json
import time
from ds_protocol import directmessage_send, directmessage_request, join, extract_msg

class DirectMessage:
    def __init__(self, message=None, recipient=None, timestamp=None):
        self.recipient = recipient
        self.message = message
        self.timestamp = timestamp

class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.token = None
        self._authenticate()

    def _authenticate(self):
        # Construct join message using ds_protocol
        auth_msg = join(self.username, self.password)
        try:
            # Send join request to server to retrieve token
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.dsuserver, 3021))  
                s.sendall(auth_msg.encode('utf-8'))
                response = s.recv(4096).decode('utf-8')
                data = json.loads(response)
                if 'response' in data and data['response']['type'] == 'ok':
                    self.token = data['response']['token']
        except Exception as e:
            print(f"Failed to authenticate: {e}")

    def send(self, message: str, recipient: str) -> bool:
        if not self.token:
            print("No authentication token available.")
            return False

        dm_json = directmessage_send(self.token, message, recipient)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.dsuserver, 3021))
                s.sendall(dm_json.encode('utf-8'))
                response = s.recv(4096).decode('utf-8')
                
                # Check response to see if message was successfully sent
                if '"type": "ok"' in response:
                    return True
        except Exception as e:
            print(f"Failed to send message: {e}")
        return False

    def _retrieve_messages(self, type: str) -> list:
        if not self.token:
            return []
        dm_request = directmessage_request(self.token, type)
        messages = []
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.dsuserver, 3021))
                s.sendall(dm_request.encode('utf-8'))
                response = s.recv(4096).decode('utf-8')
                data = extract_msg(response)
                if data.type == 'ok':
                    for msg in data.messages:
                        messages.append(DirectMessage(msg.message, msg.from_user, msg.timestamp))
        except Exception as e:
            print(f"Failed to retrieve messages: {e}")
        return messages

    def retrieve_new(self) -> list:
        return self._retrieve_messages("new")

    def retrieve_all(self) -> list:
        return self._retrieve_messages("all")
