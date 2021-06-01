#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 18 17:45:09 2021

@author: davide
Server's class
"""


import socket
import time
import sys

class Server:
    
    def __init__(self, socketFamily, socketType, serverAddress, gatewayDestMac, gatewayDestIp):
        self.serverSocket = self.createSocket(socketFamily, socketType)
        self.serverAddress = serverAddress
        self.serverIp = "10.10.10.1"
        self.serverMac = "49:9D:D0:93:EB:B2"
        self.gatewayDestMac = gatewayDestMac
        self.gatewayDestIp = gatewayDestIp
        self.receivedMessages = []
        
        try:
            self.serverSocket.bind(serverAddress)
            self.serverSocket.listen(1)
            print("Web SERVER online sulla porta: ", 8080)
        except:
            sys.exit(1)
            
    def createSocket(self, socketFamily, socketType):
        return socket.socket(socketFamily, socketType)
            
    def waitToReceive(self):
        while True:
            print ("Sono in attesa di ricevere il messaggio...")
            connectionSocket, address = self.serverSocket.accept()
            if (connectionSocket != None):
                print(connectionSocket, address)
            try:
                message = connectionSocket.recv(4096)
                print("\nHo ricevuto il messaggio:\n", message.decode()[54:189])
                self.receivedMessages.append(message.decode()[54:189])
                elapsed_time = time.time() - float(message.decode()[189::])
                print("tempo per la ricezione: %f ms" % elapsed_time)
                header = self.serverMac + self.gatewayDestMac + self.gatewayDestIp + self.serverIp 
                connectionSocket.send((str(header) + "MESSAGES STORED ON SERVER").encode())
            except IOError:
                print("errore")
#MAIN
gatewayDestMac = "33:A1:8D:55:42:5E"
gatewayDestIp = "10.10.10.5"
server = Server(socket.AF_INET, socket.SOCK_STREAM, ('localhost',8080), gatewayDestMac, gatewayDestIp)
server.waitToReceive()


