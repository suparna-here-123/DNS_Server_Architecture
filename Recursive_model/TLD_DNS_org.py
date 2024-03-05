from socket import *
from Common_to_all import *
import time
import json
import ssl
from dtls import do_patch
do_patch()

# .com TLD port
org_DNS_port = 6002
org_server_socket = ssl.wrap_socket(socket(AF_INET, SOCK_DGRAM))
org_server_socket.bind(('', org_DNS_port))

Auth_IPs = {'wikipedia' : 8000, 'cambridge' : 8001, 'redcross' : 8002}

while True :
    print(".org TLD - ON\n")

    # Receiving message from Root DNS
    root_DNS_message, root_DNS_address = org_server_socket.recvfrom(16384)

    # PROCESSING..........
    root_DNS_message = json.loads(root_DNS_message.decode())        # brought down to dict form
    
    if 'wikipedia' in root_DNS_message["Questions"]["Name"] :
        port = Auth_IPs['wikipedia']
    
    elif 'cambridge' in root_DNS_message["Questions"]["Name"] :
        port = Auth_IPs['cambridge']
    
    elif 'redcross' in root_DNS_message["Questions"]["Name"] :
        port = Auth_IPs['redcross']
    
    else :
        # Reroute to the GoDaddy auth server here
        port = 0

    response = DNS_response_format
    response["Name"] = root_DNS_message["Questions"]["Name"]
    response["Type"] = root_DNS_message["Questions"]["Type"]
    response["Class"] = root_DNS_message["Questions"]["Class"]
    response["Address"] = port

    # Sending response to Root DNS
    time.sleep(3)               # wait before sending response
    org_server_socket.sendto((json.dumps(response)).encode(), root_DNS_address)
    print("-----------------------------------------")