import time
from ds_messenger import DirectMessenger

# Configuration for testing
DSUSERVER = "168.235.86.101"  # Use the IP address of the server
TEST_USERNAME = "f21demo"
TEST_PASSWORD = "pwd123"
RECIPIENT_USERNAME = "recipient_username"  # Ensure this is a valid username on the server

def test_send_message(messenger):
    print("Testing Sending Message...")
    message = "This is a test message from test_ds_messenger.py."
    recipient = RECIPIENT_USERNAME
    success = messenger.send(message, recipient)
    assert success, "Failed to send message."
    print("Message sent successfully.")

def test_retrieve_new(messenger):
    print("Testing Retrieving New Messages...")
    new_messages = messenger.retrieve_new()
    assert isinstance(new_messages, list), "Failed to retrieve new messages as a list."
    print(f"Retrieved {len(new_messages)} new messages.")

def test_retrieve_all(messenger):
    print("Testing Retrieving All Messages...")
    all_messages = messenger.retrieve_all()
    assert isinstance(all_messages, list), "Failed to retrieve all messages as a list."
    print(f"Retrieved {len(all_messages)} total messages.")

def main():
    print("Initializing Direct Messenger...")
    messenger = DirectMessenger(dsuserver=DSUSERVER, username=TEST_USERNAME, password=TEST_PASSWORD)
    
    print("Authenticating...")
    if messenger.authenticate():
        print("Authenticated successfully.")
        test_send_message(messenger)
        time.sleep(5)  # Waiting for the message to be processed by the server
        test_retrieve_new(messenger)
        test_retrieve_all(messenger)
        print("All tests passed successfully!")
    else:
        print("Authentication failed. Tests aborted.")

if __name__ == "__main__":
    main()
