#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 18 17:45:14 2021

@author: davide

Class of a gateway inbound udp and tcp protocol in outbound
"""

import socket 
import time
import sys

class Gateway:
    
    def __init__(self, address, socketFamily, socketType, gatewayMac, gatewayTCPip, gatewayUDPip):
        self.socketFamily = socketFamily
        self.address = address
        self.socketType = socketType
        self.clients =[] #client connessi
        self.arpTableMac={"192.168.1.10": "5C:D4:85:A3:5D:AE", 
                          "192.168.1.14": "02:79:6F:E5:91:24",
                          "192.168.1.15": "3D:0E:25:E3:CD:85", 
                          "192.168.1.16": "27:39:F9:D9:01:07"} #arp table clients mac
        self.messageToSend="" #messaggio da inviare al server
        #caratteristiche del gateway
        self.gatewayMac= gatewayMac
        self.gatewayUDPip = gatewayUDPip #interfaccia UDP
        self.gatewayTCPip = gatewayTCPip #interfaccia TCP
        
        #il server rimane uguale per tutta l'esecuzione del programma e quindi e definito solamente all'interno del gateway
        self.serverIp = "10.10.10.1"
        self.serverMac = "49:9D:D0:93:EB:B2"
        
    def connectServer(self, server): #connetto il server utilizzando il protocollo TCP
        self.gateway = self.createSocket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.gateway.connect(server)
        except Exception as ex:
            print (Exception,":",ex)
            print("Errore nella connessione al server, chiudo l'applicazione!")
            sys.exit(0)
        #SONO RIUSCITO A CONNETTERMI AL SERVER, QUINDI INVIO I MESSAGGI
        print("\n-----HO RICEVUTO TUTTI I MESSAGGI QUINDI MI CONNETTO AL SERVER E LI INVIO----")
        self.sendMessage(self.messageToSend)   
        
    def createSocket(self, socketFamily, socketType):
        return socket.socket(socketFamily, socketType)
        
    def sendMessage(self, message):
        header = self.gatewayMac + self.serverMac + self.gatewayTCPip + self.serverIp 
        print("\nINVIO AL SERVER IL MESSAGGIO:\n" + self.messageToSend)
        self.gateway.send((header+message+ str(time.time())).encode('utf-8'))
        self.messageToSend = "" #resetto il messaggio da inviare
        self.clients = [] #resetto i clients collegati
        self.waitForMessage() 
       
       
        
    def messageReceive(self, message):
        received_message = message.decode("utf-8")
        source_mac = received_message[0:17]
        print("--------RICEVO UN MESSAGGIO DA MAC: ", source_mac)
        if (source_mac != self.serverMac):
            print("\nSOURCE MAC: ", source_mac)
            destination_mac = received_message[17:34]
            print("\nDESTINATION MAC: ", destination_mac)
            source_ip = received_message[34:46]
            print("\nSOURCE IP: ", source_ip)
            destination_ip = received_message[46:58]
            print("\nDESTINATION IP: ", destination_ip)
            message = received_message[58::]
            print("\nMESSAGGIO RICEVUTO: ", message[0:33])
            print("\nDIMENSIONE MESSAGGIO: %d bytes" % len(message))
            elapsed_time = time.time() - float(message[33::])
            print("\nTIME ELAPSED: %f ms" % elapsed_time)
            
            if source_ip in self.arpTableMac.keys():
                if self.arpTableMac.get(source_ip) == source_mac and (source_ip, source_mac) not in self.clients:
                    self.clients.append((source_ip, source_mac))
                    self.messageToSend += message[0:33] + "\n"
                else:
                    print("Non posso aggiungere questo messaggio poichè è già stato ricevuto un messaggio da questo client")
        else:
            print(received_message[54::])
            
            
    def waitForMessage(self):
        self.gateway = self.createSocket(self.socketFamily, self.socketType)
        self.gateway.bind(self.address)
        print ('\n\r Gateway ''%s'' sulla porta %s' % self.address)
        
        while True:
            print("\n\nGateway: sono in attesa di ricevere messaggi") 
            message, address = self.gateway.recvfrom(4096)
     
            if message:
                self.messageReceive(message)
             #verifico che siano arrivati 4 messaggi
        #una volta ricevuti tutti i messaggi, qui devo far connettere il gateway al server per inviare tutti i messaggi ricevuti
       
            if len(self.clients) == 4: #invio il messagggio al server solo quando hanno inviato il messaggio tutti e 4
                self.gateway.close()
                self.connectServer(('localhost', 8080)) #connetto al server sulla porta 8080
                break
#MAIN
gatewayMac= "33:A1:8D:55:42:5E"
gatewayUDPip = "192.168.1.20" #interfaccia UDP
gatewayTCPip = "10.10.10.5" #interfaccia TCP
        
gate = Gateway(('localhost', 8400), socket.AF_INET, socket.SOCK_DGRAM, gatewayMac, gatewayTCPip , gatewayUDPip)
gate.waitForMessage()
            
            
