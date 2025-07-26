from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(('', serverPort))
serverSocket.listen(1) # listen(backlog) - number of connection is waited for accept at a time, if larger -> queue
print('The server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept()
    
    sentence = connectionSocket.recv(1024).decode()
    modified_sentence = sentence.upper()
    
    connectionSocket.send(modified_sentence.encode())
    
    connectionSocket.close()
    
    