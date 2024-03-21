import socket
import time
import ds_protocol


class DirectMessage:
    """Direct message object that holds information."""
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None


class DirectMessenger:
    """DirectMessenger class that allows users to communicate with another user through private chat."""
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.port = 3021
        self.server = dsuserver
        self.username = username
        self.password = password
        self.connected = self.join()

    def join(self):
        """Attempts to join the dsuserver. Returns True if connected, else False."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.server, self.port))
                join_str = f'{{"join": {{"username": "{self.username}", "password": "{self.password}", "token": ""}}}}'
                send = client.makefile('w')
                recv = client.makefile('r')
                send.write(join_str + '\r\n')
                send.flush()
                resp = recv.readline()
                decoded_resp = ds_protocol.extract_json(resp)
                if decoded_resp[1] == "error":
                    print(decoded_resp[0])
                    return False
                self.token = decoded_resp[1]
                return True
        except Exception as e:
            print(f"Joining failed: {e}")
            return False

    def send(self, message: str, recipient: str) -> bool:
        """Sends message to another person on the DSUserver. Returns True if sent else False."""
        try:
            if self.token is None:
                if not self.join():
                    return False
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.server, self.port))
                msg_str = f'{{"token": "{self.token}", "directmessage": {{"entry": "{message}", "recipient": "{recipient}", "timestamp": "{time.time()}"}}}}'
                send_msg = client.makefile('w')
                send_msg.write(msg_str + '\r\n')
                send_msg.flush()
                recv = client.makefile('r')
                resp = recv.readline()
                decoded_resp = ds_protocol.extract_json(resp)
                if decoded_resp[1] == "error":
                    print(decoded_resp[0])
                    return False
                return True
        except Exception as e:
            print(f"Sending failed: {e}")
            return False

    def retrieve_new(self) -> list[DirectMessage]:
        """Retrieves new messages. Returns list of DirectMessage objects."""
        messages = []
        try:
            if self.token is None:
                if not self.join():
                    return messages
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.server, self.port))
                msg_str = f'{{"token": "{self.token}", "directmessage": "new"}}'
                send_msg = client.makefile('w')
                send_msg.write(msg_str + '\r\n')
                send_msg.flush()
                recv = client.makefile('r')
                resp = recv.readline()
                decoded_resp = ds_protocol.extract_message(resp)
                if decoded_resp[1] == "error":
                    print(decoded_resp[0])
                    return messages
                for msg_tuple in decoded_resp[0]:
                    dm = DirectMessage()
                    dm.message = msg_tuple[0]
                    dm.recipient = msg_tuple[1]
                    dm.timestamp = msg_tuple[2]
                    messages.append(dm)
                return messages
        except Exception as e:
            print(f"Retrieving new messages failed: {e}")
            return messages

    def retrieve_all(self) -> list:
        """Retrieves all texts. Returns list of DirectMessage objects."""
        messages = []
        try:
            if self.token is None:
                if not self.join():
                    return messages
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.server, self.port))
                msg_str = f'{{"token": "{self.token}", "directmessage": "all"}}'
                send_msg = client.makefile('w')
                send_msg.write(msg_str + '\r\n')
                send_msg.flush()
                recv = client.makefile('r')
                resp = recv.readline()
                decoded_resp = ds_protocol.extract_message(resp)
                if decoded_resp[1] == "error":
                    print(decoded_resp[0])
                    return messages
                for msg_tuple in decoded_resp[0]:
                    dm = DirectMessage()
                    dm.message = msg_tuple[0]
                    dm.recipient = msg_tuple[1]
                    dm.timestamp = msg_tuple[2]
                    messages.append(dm)
        except Exception as e:
            print(f"Retrieving all messages failed: {e}")
        return messages
