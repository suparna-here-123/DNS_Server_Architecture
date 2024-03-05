from socket import *
from Common_to_all import *
import time
import json
import ssl
from dtls import do_patch
do_patch()

# .com TLD port
goDaddy_auth_port = 7003
goDaddy_server_socket = ssl.wrap_socket(socket(AF_INET, SOCK_DGRAM))
goDaddy_server_socket.bind(('', goDaddy_auth_port))


Services_IP = {"cats4you" : 9000, "darshini4you" : 9001, "cafe4you" : 9002}

while True :
    print("GoDaddy Auth DNS - ON\n")

    com_TLD_message, com_TLD_address = goDaddy_server_socket.recvfrom(16384)
    message = com_TLD_message.decode()
    message = json.loads(message)
    print(message)
    
    if ("cats4you" in message["Questions"]["Name"]):
        port= Services_IP["cats4you"]
    
    elif ("darshini4you" in message["Questions"]["Name"]) :
        port= Services_IP["darshini4you"]
    
    elif ("cafe4you" in message["Questions"]["Name"]) :
        port= Services_IP["cafe4you"]

    else :
        # Domain name not registered
        port = 0
    
    if (port == 0) :
        print("Port was zero")
        response = DNS_response_format
        response["Name"] = message["Questions"]["Name"]
        response["Type"] = message["Questions"]["Type"]
        response["Class"] = message["Questions"]["Class"]
        response["Address"] = port
        goDaddy_server_socket.sendto((json.dumps(response)).encode(), com_TLD_address)
        continue
    
    else :
        # Sending response back to the TLD
        response = DNS_response_format
        response["Name"] = message["Questions"]["Name"]
        response["Type"] = message["Questions"]["Type"]
        response["Class"] = message["Questions"]["Class"]
        response["Address"] = port

        # Auth received from TLD
        print("GoDaddy Auth received from TLD")
        print(com_TLD_message.decode())
        print("\n")

        # Auth Sending to TLD
        print("Auth sending to TLD")
        print((json.dumps(response)))
        time.sleep(3)               # wait before sending response
        goDaddy_server_socket.sendto((json.dumps(response)).encode(), com_TLD_address)
        print("-----------------------------------------")
