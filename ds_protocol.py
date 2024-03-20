#Mihir Katyal
#mkatyal@uci.edu
#19099879


import json
from collections import namedtuple
import time

# Definitions for response data structures
DataTuple = namedtuple('DataTuple', ['type', 'message', 'token', 'messages'])
MessageTuple = namedtuple('MessageTuple', ['message', 'from_user', 'timestamp'])

def join(username, password):
    return json.dumps({
        "join": {
            "username": username,
            "password": password,
            "token": "" 
        }
    })

def post(token, message, timestamp=time.time()):
    return json.dumps({
        "token": token,
        "post": {
            "entry": message,
            "timestamp": str(timestamp)  
        }
    })

def bio(token, bio, timestamp=time.time()):
    return json.dumps({
        "token": token,
        "bio": {
            "entry": bio,
            "timestamp": str(timestamp) 
        }
    })

def directmessage_send(token, message, recipient, timestamp=time.time()):
    return json.dumps({
        "token": token,
        "directmessage": {
            "entry": message,
            "recipient": recipient,
            "timestamp": str(timestamp)
        }
    })

def directmessage_request(token, request_type="new"):
    return json.dumps({
        "token": token,
        "directmessage": request_type
    })

def extract_msg(json_msg: str) -> DataTuple:
    try:
        json_obj = json.loads(json_msg)
        if 'response' in json_obj:
            response = json_obj['response']
            if 'messages' in response:  # Handle direct messages response
                messages = [MessageTuple(msg['message'], msg['from'], msg['timestamp']) for msg in response['messages']]
                return DataTuple(response.get('type', ''), response.get('message', ''), response.get('token', ''), messages)
            else:  # Handle other types of responses
                return DataTuple(response.get('type', ''), response.get('message', ''), response.get('token', ''), [])
        else:
            return DataTuple('error', 'Invalid response format', None, [])
    except json.JSONDecodeError:
        return DataTuple('error', 'JSON cannot be decoded', None, [])
