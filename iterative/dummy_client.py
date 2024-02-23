from socket import *
from Common_to_all import *
import json
from datetime import datetime
import sys

client_port = 52
client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.bind(('', client_port))

# Client is never always-on, but done here for demo only
while True : 
    client_query = input("Enter query : ")
    start = datetime.now()
    
    client_socket.sendto(client_query.encode(), (All_Servers_IP, 53))
    local_dns_message, local_dns_address = client_socket.recvfrom(16348)
    end = datetime.now()
    
    message_recvd = local_dns_message.decode()
    dict_msg = json.loads(message_recvd)

    if dict_msg['Address'] == 0 :
         print("404 Page Not Found")

    else :   
          print(All_Servers_IP, dict_msg['Address'], dict_msg['Class'])

          if 'CNAME' in client_query :
               print('CNAME')
               
          elif 'MX' in client_query :
               print('MX')
          
          else :
               # printing IP address and port
               print(All_Servers_IP, dict_msg['Type'])
          
          print("\n\n\n")
          print("Query time : ", end - start)
          print("SERVER : ", All_Servers_IP, dict_msg['Address'])
          print("WHEN : ", end = "")

          # Get current date and time
          now = datetime.now()

          # Get date components in words
          date_in_words = now.strftime("%B %d, %Y")  # Full month name, day, year

          # Get time components in numbers
          time_in_numbers = now.strftime("%H:%M:%S")  # Hours:Minutes:Seconds

          # Get day of the week in words
          day_in_words = now.strftime("%A")  # Full weekday name
          print(day_in_words[0:3], date_in_words, time_in_numbers)
          print("MSG SIZE : ", sys.getsizeof(message_recvd))
          print("\n")