"""
Created on Tue May 18 17:45:09 2021

@author: davide

easy module that start clients simultaneously
"""


import socket
import client

#MAIN
clients = []
clientsAddresses = {"192.168.1.10": "5C:D4:85:A3:5D:AE", 
          "192.168.1.14": "02:79:6F:E5:91:24",
          "192.168.1.15": "3D:0E:25:E3:CD:85", 
          "192.168.1.16": "27:39:F9:D9:01:07"}


destIpAddress = "192.168.1.20" #ip della porta udp del gateway
destMacAddress = "33:A1:8D:55:42:5E" #mac del gateway
gateway_address = ('localhost', 8400)

for ip in clientsAddresses.keys():
    cl = client.Client(socket.AF_INET, socket.SOCK_DGRAM, ip, destIpAddress, clientsAddresses.get(ip), destMacAddress)
    clients.append(cl)


message = '192.168.1.10 – 08.00 – 09°C - 27%' #message to send    
clients[0].sendMessage(message[0:58], gateway_address)
message = '192.168.1.14 – 12.00 – 09°C - 65%' 
clients[1].sendMessage(message[0:58], gateway_address)
message = '192.168.1.15 – 16.00 – 22°C - 55%'
clients[2].sendMessage(message[0:58], gateway_address)
message = '192.168.1.16 – 20.00 – 40°C - 40%'
clients[3].sendMessage(message[0:58], gateway_address)
