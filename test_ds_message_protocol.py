#Mihir Katyal
#mkatyal@uci.edu
#19099879

import ds_protocol
import time

def test_directmessage_send():
    token = "test_token"
    message = "Hello, world!"
    recipient = "test_user"
    timestamp = time.time()
    json_message = ds_protocol.directmessage_send(token, message, recipient, timestamp)

    print("Testing directmessage_send...")
    print("Output:", json_message)
    print()

def test_directmessage_request():
    token = "test_token"
    print("Testing directmessage_request for 'new' messages...")
    json_request_new = ds_protocol.directmessage_request(token, "new")
    print("Output for 'new':", json_request_new)
    
    print("Testing directmessage_request for 'all' messages...")
    json_request_all = ds_protocol.directmessage_request(token, "all")
    print("Output for 'all':", json_request_all)
    print()

def test_extract_msg():
    print("Testing extract_msg...")
    sample_response = '{"response": {"type": "ok", "messages": [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167690.3928561"}]}}'
    extracted = ds_protocol.extract_msg(sample_response)
    print("Extracted Messages:")
    for msg in extracted.messages:
        print(f'Message: {msg.message}, From: {msg.from_user}, Timestamp: {msg.timestamp}')
    print()

# Run the tests
test_directmessage_send()
test_directmessage_request()
test_extract_msg()
