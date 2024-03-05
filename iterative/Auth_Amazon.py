from socket import *
from Common_to_all import *
import json
import time
import ssl
from dtls import do_patch
do_patch()

# .com TLD port
amazon_auth_port = 7001
amazon_server_socket = ssl.wrap_socket(socket(AF_INET, SOCK_DGRAM))
amazon_server_socket.bind(('', amazon_auth_port))

Services_IP = {"prime" : 8003, "fresh" : 8004, "pay" : 8005}

while True:
    #receiving the response from the localDNS
    local_DNS_message, local_DNS_address = amazon_server_socket.recvfrom(16384)
    message = local_DNS_message.decode()
    message = json.loads(message)

    if ("prime" in message["Questions"]["Name"].split('.')):
        port= Services_IP["prime"]

    elif ("fresh" in message["Questions"]["Name"].split('.')) :
        port= Services_IP["fresh"]

    elif ("pay" in message["Questions"]["Name"].split('.')) :
        port= Services_IP["pay"]

    else :
        port=0
        ################# HANDLE OTHER SERVICES #######################

    # Sending response back to the local DNS server

    response = DNS_response_format
    response["Name"] = message["Questions"]["Name"]
    response["Type"] = message["Questions"]["Type"]
    response["Class"] = message["Questions"]["Class"]
    response["Address"] = port
    print("Sending message to Local DNS : ", response)

    time.sleep(3) 
    amazon_server_socket.sendto((json.dumps(response)).encode(), (local_DNS_address))
