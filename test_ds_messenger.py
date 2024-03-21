import time
from ds_messenger import DirectMessenger

# Configuartion for testing
DSUSERVER = "168.235.86.101"
TEST_USERNAME = "f21demo"
TEST_PASSWORD = "pwd123"
RECIPIENT_USERNAME = "recipient_username"  # Ensure this is an account you can check

def test_authentication():
    print("Testing authentication...")
    messenger = DirectMessenger(dsuserver=DSUSERVER, username=TEST_USERNAME, password=TEST_PASSWORD)
    assert messenger.authenticate(), "Failed to authenticate"