from socket import *
from Common_to_all import *
import time
import json

# .com TLD port
com_DNS_port = 6000
com_server_socket = socket(AF_INET, SOCK_DGRAM)
com_server_socket.bind(('', com_DNS_port))

Auth_IPs = {'google' : 7000, 'amazon' : 7001, 'flipkart' : 7002, 'goDaddy' : 7003}

while True :
    print(".com TLD - ON\n")

    # Receiving message from Root DNS
    root_DNS_message, root_DNS_address = com_server_socket.recvfrom(16384)

    # # PROCESSING..........
    root_DNS_message = json.loads(root_DNS_message.decode())        # brought down to dict form
    
    if 'google' in root_DNS_message["Questions"]["Name"] :
        port = Auth_IPs['google']
    
    elif 'amazon' in root_DNS_message["Questions"]["Name"] :
        port = Auth_IPs['amazon']
    
    elif 'flipkart' in root_DNS_message["Questions"]["Name"] :
        port = Auth_IPs['flipkart']
    
    else :
        port = 0
    #     # DO SOMETHING HEREE!!!!!!!!!!!!

    if (port == 0) :
        print("Port was zero")
        response = DNS_response_format
        response["Name"] = root_DNS_message["Questions"]["Name"]
        response["Type"] = root_DNS_message["Questions"]["Type"]
        response["Class"] = root_DNS_message["Questions"]["Class"]
        response["Address"] = port
        com_server_socket.sendto((json.dumps(response)).encode(), root_DNS_address)
        continue

    else :
        # Sending request to Auth
        query = DNS_query_format
        com_server_socket.sendto(json.dumps(root_DNS_message).encode(), (All_Servers_IP, port))

        # Response received here...........
        print("TLD received from Auth")
        auth_response, authAddress = com_server_socket.recvfrom(16384)
        print(auth_response)
        print("\n")

        #Sending response to Root server here..
        print("TLD to Root")
        print(auth_response.decode())
        print("\n")

        # Sending response to Root DNS
        time.sleep(3)               # wait before sending response
        com_server_socket.sendto(auth_response, root_DNS_address)
        print("-----------------------------------------")