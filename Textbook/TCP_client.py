from socket import *

serverName = 'serverName'
serverPort = 12000 
clientSocket = socket(AF_INET, SOCK_STREAM) # TCP connection as TCP bytestream

clientSocket.connect((serverName, serverPort))

sentence = input('Input lowercase sentence: ')
clientSocket.send(sentence.encode())

modified_sentence = clientSocket.recv(1024) 
# no need to sendto, recvfrom via the connection
print(f"From server: {modified_sentence.decode()}")

clientSocket.close()