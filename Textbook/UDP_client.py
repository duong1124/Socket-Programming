from socket import *

serverName = 'hostname'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM) # IPv4 socket, AF_INET6 for IPv6 socket

message = input('Input lowercase sentence: ')
clientSocket.sendto(message.encode(), (serverName, serverPort)) # serverName -> serverIP is done here

# Receive modified message (and senderIP) from server and display 
modifiedMessage, serverAddress = clientSocket.recvfrom(2048) # read maximum 2048 bytes
print('From Server:', modifiedMessage.decode()) #

clientSocket.close() 