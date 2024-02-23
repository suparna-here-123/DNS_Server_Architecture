from socket import *
from Common_to_all import *
import time
import json

# Root DNS port
root_DNS_port = 52311
root_serverSocket = socket(AF_INET, SOCK_DGRAM)
root_serverSocket.bind(('', root_DNS_port))

# Each TLD server designated to a unique port
# This PORT NUMBER IS stored in the dictionary
TLD_IPs = {'com' : 6000, 'edu' : 6001, 'org' : 6002}

while True:
    print("Root DNS - ON\n")
    # receiving query from Local DNS
    local_DNS_message, local_DNS_address = root_serverSocket.recvfrom(16384)
    TLD_string = local_DNS_message.decode()
    # print("@Root DNS, received : ", TLD_string)

    # # PROCESSING.....
    TLD_dict = json.loads(TLD_string)
    TLD = TLD_dict["Questions"]["Name"][-3:]
    
    if TLD == 'com' :
        port = TLD_IPs['com']
    
    elif TLD == 'edu' :
        port = TLD_IPs['edu']
    
    elif TLD == 'org':
        port = TLD_IPs['org']

    else :
        port = 0
    
    # Sending message to next DNS server
    if (port == 0) :
        print("Port was zero")
        response = DNS_response_format
        response["Name"] = TLD_string["Questions"]["Name"]
        response["Type"] = TLD_string["Questions"]["Type"]
        response["Class"] = TLD_string["Questions"]["Class"]
        response["Address"] = port
        root_serverSocket.sendto((json.loads(response)).encode(), local_DNS_address)
        continue
    
    else :
        print("Port was NOT zero")
        query = DNS_query_format
        root_serverSocket.sendto(local_DNS_message, (All_Servers_IP, port))

        # Receiving response from TLD server
        print("Root received from TLD")
        TLD_response, TLD_address = root_serverSocket.recvfrom(16384)
        print(TLD_response)
        print("\n")
        
        # Passing on response to Local DNS
        print("Root sending to Local DNS")
        print(TLD_response.decode())

        # Sending back to Local DNS
        time.sleep(3)               # wait before sending response
        root_serverSocket.sendto(TLD_response, local_DNS_address)

    print("-----------------------------------------")