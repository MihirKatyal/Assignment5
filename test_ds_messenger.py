import time
import json
import pip._vendor.requests 
from ds_messenger import DirectMessenger

# Configuartion for testing
DSUSERVER = "168.235.86.101"
TEST_USERNAME = "f21demo"
TEST_PASSWORD = "pwd123"
RECIPIENT_USERNAME = "recipient_username"  # Ensure this is an account you can check

def authenticate(self):
    try:
        response = pip._vendor.requests.post(f'http://{self.dsuserver}/join', json={"username": self.username, "password": self.password})
        # Check if the response is successful and has content
        if response.status_code == 200 and response.text:
            response_json = response.json()
            if 'token' in response_json:
                self.token = response_json['token']
                return True
            else:
                print("Token not found in response:", response_json)
        else:
            print("Failed to authenticate:", response.status_code, response.text)
    except pip._vendor.requests.exceptions.RequestException as e:
        print("Request failed:", e)
    except json.JSONDecodeError as e:
        print("Failed to decode JSON:", e, "Response text:", response.text)
    return False

def test_retrieve_new():
    print("Testing Retrieving New Messages...")
    messenger = DirectMessenger(dsuserver=DSUSERVER, username=TEST_USERNAME, password=TEST_PASSWORD)
    assert messenger.authenticate(), "Pre-Test Authentication failed."
    new_messages = messenger.retrieve_new()
    assert isinstance(new_messages, list), "Failed to retrieve new messages as a list."
    print(f"Retrieved {len(new_messages)} new messages.")

def test_retrieve_all():
    print("Testing Retrieving All Messages...")
    messenger = DirectMessenger(dsuserver=DSUSERVER, username=TEST_USERNAME, password=TEST_PASSWORD)
    assert messenger.authenticate(), "Pre-Test Authentication failed."
    all_messages = messenger.retrieve_all()
    assert isinstance(all_messages, list), "Failed to retrieve all messages as a list."
    print(f"Retrieved {len(all_messages)} total messages.")

def test_send_message():
    print("Testing Sending Message...")
    messenger = DirectMessenger(dsuserver=DSUSERVER, username=TEST_USERNAME, password=TEST_PASSWORD)
    assert messenger.authenticate(), "Pre-Test Authentication failed."
    message = "This is a test message."
    recipient = RECIPIENT_USERNAME
    assert messenger.send_message(message, recipient), "Failed to send message."
    print("Message sent successfully.")

def main():
    authenticate()
    test_send_message()
    # Waiting for the message to be processed by the server and appear in the inbox
    time.sleep(5)  
    test_retrieve_new()
    test_retrieve_all()
    print("All tests passed successfully!")

if __name__ == "__main__":
    main()