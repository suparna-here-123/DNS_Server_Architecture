from socket import *
import random
from Common_to_all import *
import json
import time

root_DNS_port = 52311
root_serverSocket = socket(AF_INET, SOCK_DGRAM)
root_serverSocket.bind(('', root_DNS_port))

# Each TLD server designated to a unique port
# This PORT NUMBER IS stored in the dictionary
TLD_IPs = {'com' : 6000, 'edu' : 6001, 'org' : 6002}

while True:
    #receiving from the local DNS
    local_DNS_message, local_DNS_address = root_serverSocket.recvfrom(16384)

    # # PROCESSING.....
    root_string = json.loads(local_DNS_message)
    TLD = root_string["Questions"]["Name"][-3:]
    print("TLD extracted = ", TLD)

    if TLD == 'com' :
        port = TLD_IPs['com']

    elif TLD == 'edu' :
        port = TLD_IPs['edu']

    elif TLD == 'org' :
        port = TLD_IPs['org']

    else:
        port=0
    

    # sending the ip address of the respective TLD server back to the local DNS server

    response = DNS_response_format
    response["Name"] = root_string["Questions"]["Name"]
    response["Type"] = root_string["Questions"]["Type"]
    response["Class"] = root_string["Questions"]["Class"]
    response["Address"] = port

    print("Sending message to Local DNS : ", response)
    time.sleep(3) 
    root_serverSocket.sendto((json.dumps(response)).encode(), (local_DNS_address))


