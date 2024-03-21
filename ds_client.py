#Mihir Katyal
#mkatyal@uci.edu
#19099879

import socket
import ds_protocol
import time
import json  # Import json for parsing

def send(server:str, port:int, username:str, password:str, message:str=None, bio:str=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((server, port))
        send = client.makefile('w')
        recv = client.makefile('r')

        # Join request
        join_str = ds_protocol.join(username, password)
        send.write(join_str + '\r\n')
        send.flush()

        resp = recv.readline()
        decoded_resp = ds_protocol.extract_msg(resp)

        if decoded_resp.type == "error":
            print(decoded_resp.message)
            return False

        user_token = decoded_resp.token  # Correctly extracting token from response

        # Sending bio if provided
        if bio:
            bio_str = ds_protocol.bio(user_token, bio)
            send.write(bio_str + '\r\n')
            send.flush()
            resp = recv.readline()
            print(resp)  # Print the server response

        # Sending message if provided
        if message:
            post_str = ds_protocol.post(user_token, message)
            send.write(post_str + '\r\n')
            send.flush()
            resp = recv.readline()
            print(resp)  # Print the server response

        return True
