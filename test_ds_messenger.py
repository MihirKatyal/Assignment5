import pytest
from ds_messenger import DirectMessenger, DirectMessage

# Configuration for testing - Replace these with actual testing data
DSUSERVER = "168.235.86.101"  # Use the IP address of the server
TEST_USERNAME = "testuser"  # Replace with actual username for testing
TEST_PASSWORD = "testpass"  # Replace with actual password for testing
RECIPIENT_USERNAME = "recipientuser"  # Make sure this is a valid username on the server

# Setup for pytest to create messenger instances
@pytest.fixture
def setup_messengers():
    sender = DirectMessenger(DSUSERVER, TEST_USERNAME, TEST_PASSWORD)
    receiver = DirectMessenger(DSUSERVER, RECIPIENT_USERNAME, "recipientpass")  # Adjust as needed
    assert sender.token is not None
    assert receiver.token is not None
    return sender, receiver

def test_send_and_receive(setup_messengers):
    sender, receiver = setup_messengers
    message = "This is a test message from pytest."
    
    # Test sending the message
    sent = sender.send(message, RECIPIENT_USERNAME)
    assert sent, "Failed to send message."

    # Assuming there might be a slight delay in message delivery
    import time
    time.sleep(5)  # Wait for the message to be processed

    # Test retrieving the new message
    new_messages = receiver.retrieve_new()
    assert new_messages, "No new messages retrieved."
    assert isinstance(new_messages[0], DirectMessage), "Retrieved object is not a DirectMessage."
    assert new_messages[0].message == message, "The retrieved message text does not match the sent message."
    assert new_messages[0].recipient == TEST_USERNAME, "The retrieved message sender does not match."

def test_retrieve_all(setup_messengers):
    sender, receiver = setup_messengers
    all_messages = receiver.retrieve_all()
    assert isinstance(all_messages, list), "Failed to retrieve all messages as a list."
    assert all_messages, "No messages retrieved with retrieve_all."
