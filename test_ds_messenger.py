#Mihir Katyal
#mkatyal@uci.edu
#19099879

from ds_messenger import DirectMessenger, DirectMessage


TEST_SERVER = '168.235.86.101'  
TEST_PORT = 3021                
TEST_USERNAME = 'f21demo'     
TEST_PASSWORD = 'pwd123'     

def test_send():
    print("Testing send functionality...")
    messenger = DirectMessenger(dsuserver="168.235.86.101", username="your_username", password="your_password")
    assert messenger.send(message="Hello, this is a test message from pytest", recipient="recipient_username"), "Failed to send message"
    print("Send functionality passed.")

def test_retrieve_new():
    print("Testing retrieve new messages functionality...")
    messenger = DirectMessenger(dsuserver="168.235.86.101", username="your_username", password="your_password")
    messages = messenger.retrieve_new()
    assert isinstance(messages, list), "Failed to retrieve new messages"
    print("Retrieve new messages functionality passed.")

def test_retrieve_all():
    print("Testing retrieve all messages functionality...")
    messenger = DirectMessenger(dsuserver="168.235.86.101", username="your_username", password="your_password")
    messages = messenger.retrieve_all()
    assert isinstance(messages, list), "Failed to retrieve all messages"
    print("Retrieve all messages functionality passed.")

if __name__ == "__main__":
    test_send()
    test_retrieve_new()
    test_retrieve_all()