from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)

serverSocket.bind(('', serverPort)) # Bind to all interfaces (all IP addresses) on the specified port
print('The server is ready to receive')

while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    
    modified_message = message.decode().upper()
    
    # clientAddress ~ (clientIP, clientPort)    
    serverSocket.sendto(modified_message, clientAddress)