#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 18 17:39:26 2021

@author: davide

Create the client using UDP protocol. It is a simulation of wheater station that send a message to gateway.
"""

import socket as sk
import time

class Client:
    
    def __init__(self, socketFamily, socketType, sourceIpAddress, destIpAddress, sourceMacAddress, destMacAddress):
        self.sock = sk.socket(socketFamily, socketType)
        self.sourceIpAddress = sourceIpAddress
        self.destIpAddress = destIpAddress
        self.sourceMacAddress = sourceMacAddress
        self.destMacAddress = destMacAddress
    
    #invia il messaggio
    def sendMessage(self, message, gateway_address):
        #provo ad inviare il messaggio
        try:
                header = self.sourceMacAddress + self.destMacAddress + self.sourceIpAddress + self.destIpAddress
                print('Invio il messaggio: "%s"' % message[0:33])
                time.sleep(2) #attende 2 secondi prima di inviare la richiesta
                self.sock.sendto((header + message + str(time.time())).encode(), gateway_address) #invio il messaggio all'indirizzo specificato
                print('Ho inviato il messaggio, quindi chiudo la connessione con il gateway')
        except Exception as info:
            print("Errore nell'invio del messaggio")
            print(info)
        finally:
            pass