from socket import *
from Common_to_all import *
import json

# .com TLD port
google_auth_port = 7000
google_server_socket = socket(AF_INET, SOCK_DGRAM)
google_server_socket.bind(('', google_auth_port))


Services_IP = {"drive" : 8000, "youtube" : 8001, "classroom" : 8002}

while True:
    #receiving the response from the localDNS
    local_DNS_message, local_DNS_address = google_server_socket.recvfrom(16384)
    message = local_DNS_message.decode()
    message = json.loads(message)

    if ("drive" in local_DNS_message.decode()):
        port= Services_IP["drive"]

    elif ("youtube" in local_DNS_message.decode()) :
        port= Services_IP["youtube"]

    elif ("classroom" in local_DNS_message.decode()) :
        port= Services_IP["classroom"]

    else :
        pass
        ################# HANDLE OTHER SERVICES #######################

    # Sending response back to the local DNS server
    print("Sending message to Local DNS : ", port)

    response = DNS_response_format
    response["Name"] = message["Questions"]["Name"]
    response["Type"] = message["Questions"]["Type"]
    response["Class"] = message["Questions"]["Class"]
    response["Address"] = port

    google_server_socket.sendto((json.dumps(response)).encode(), (local_DNS_address))
