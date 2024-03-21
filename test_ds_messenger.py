import time
from ds_messenger import DirectMessenger

# Configuration for testing
DSUSERVER = "168.235.86.101"
TEST_USERNAME = "f21demo"
TEST_PASSWORD = "pwd123"
RECIPIENT_USERNAME = "recipient_username"  

def test_send_message(messenger):
    print("Testing Sending Message...")
    message = "This is a test message from the test script."
    success = messenger.send(message, RECIPIENT_USERNAME)  # Ensure your DirectMessenger has a send method
    assert success, "Failed to send message."

def test_retrieve_new(messenger):
    print("Testing Retrieving New Messages...")
    new_messages = messenger.retrieve_new()  # Ensure your DirectMessenger has a retrieve_new method
    assert isinstance(new_messages, list), "Failed to retrieve new messages as a list."
    print(f"Retrieved {len(new_messages)} new messages.")

def test_retrieve_all(messenger):
    print("Testing Retrieving All Messages...")
    all_messages = messenger.retrieve_all()  # Ensure your DirectMessenger has a retrieve_all method
    assert isinstance(all_messages, list), "Failed to retrieve all messages as a list."
    print(f"Retrieved {len(all_messages)} total messages.")

def main():
    print("Starting tests...")
    messenger = DirectMessenger(dsuserver=DSUSERVER, username=TEST_USERNAME, password=TEST_PASSWORD)
    if not messenger.authenticate():
        print("Failed to authenticate with the server.")
        return
    print("Authenticated successfully.")

    test_send_message(messenger)
    time.sleep(5)  # Wait a bit for the message to be processed by the server
    test_retrieve_new(messenger)
    test_retrieve_all(messenger)
    print("All tests passed successfully!")

if __name__ == "__main__":
    main()
