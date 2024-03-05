from socket import *
from Common_to_all import *
import time
import json
import ssl
from dtls import do_patch
do_patch()

# .com TLD port
google_auth_port = 7000
google_server_socket = ssl.wrap_socket(socket(AF_INET, SOCK_DGRAM))
google_server_socket.bind(('', google_auth_port))


Services_IP = {"drive" : 8000, "youtube" : 8001, "classroom" : 8002}

while True :
    print("Google Auth DNS - ON\n")

    com_TLD_message, com_TLD_address = google_server_socket.recvfrom(16384)
    message = com_TLD_message.decode()
    message = json.loads(message)
    
    if ("drive" in com_TLD_message.decode().split('.')):
        port= Services_IP["drive"]
    
    elif ("youtube" in com_TLD_message.decode().split('.')) :
        port= Services_IP["youtube"]
    
    elif ("classroom" in com_TLD_message.decode().split('.')) :
        port= Services_IP["classroom"]

    else :
        port = 0
    
    if (port == 0) :
        print("Port was zero")
        response = DNS_response_format
        response["Name"] = message["Questions"]["Name"]
        response["Type"] = message["Questions"]["Type"]
        response["Class"] = message["Questions"]["Class"]
        response["Address"] = port
        google_server_socket.sendto((json.loads(response)).encode(), com_TLD_address)
        continue
    
    else :
        # Sending response back to the TLD
        response = DNS_response_format
        response["Name"] = message["Questions"]["Name"]
        response["Type"] = message["Questions"]["Type"]
        response["Class"] = message["Questions"]["Class"]
        response["Address"] = port

        # Auth received from TLD
        print("Auth received from TLD")
        print(com_TLD_message.decode())
        print("\n")

        # Auth Sending to TLD
        print("Auth sending to TLD")
        print((json.dumps(response)))
        time.sleep(3)               # wait before sending response
        google_server_socket.sendto((json.dumps(response)).encode(), com_TLD_address)
        print("-----------------------------------------")
