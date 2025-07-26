import socket as s
import threading
from config import *
from utils import *

serverIP = s.gethostbyname(s.gethostname())

serverSocket = s.socket(s.AF_INET, s.SOCK_STREAM) # TCP
serverSocket.bind((serverIP, PORT))
serverSocket.listen(MAX_USERS)

def handle_client(connectionSocket, addr):
    try:
        # Enter username until valid
        connectionSocket.send("Enter your username: ".encode())
        username = connectionSocket.recv(1024).decode().strip()
        
        while username in username_list() or not username: 
            connectionSocket.send("Your username already existed or invalid!".encode())
            username = connectionSocket.recv(1024).decode().strip()
        
        # Save client
        clients[connectionSocket] = {"username" : username , "addr" : addr}
        
        # Welcome message
        welcome_message = f"Welcome {username} to the chat."
        welcome_message += "Type /option for options."
        connectionSocket.send(welcome_message.encode()) # send to new client
        broadcast_clients(f"{username} has joined the chat.", connectionSocket) # send to the other clients
        
        while True:
            try:
                message = connectionSocket.recv(1024).decode().strip() 
                
                # 1. Exit message
                if message == EXIT_MSG:
                    disconnect_closeSocket(connectionSocket)
                    break
                
                # 2. Get list message    
                elif message.startswith(GET_LIST_MSG):
                    online_users = username_list()
                    list_message = f"{len(online_users)} online clients: {', '.join(online_users)}"
                    connectionSocket.send(f"[{get_time()}] {list_message}".encode())
                
                # 3. Option message
                elif message.startswith(OPTION_MSG):
                    command_list = "\n".join([f"- {command} : {description}" for command, description in COMMANDS.items()])
                    command_message = f"Available options:\n{command_list}"
                    connectionSocket.send(command_message.encode())
                
                # 4. Private message
                elif message.startswith(PRIVATE_MSG):
                    name_msg = message[4:].split(' ', 1)
                    if len(name_msg) >= 2: 
                        target_username, message = name_msg
                        send_private_message(message, connectionSocket, target_username)
                    else:
                        connectionSocket.send("Wrong format. Must be /pm <username> <message>".encode())
                
                # 5. Get infor message
                elif message == GET_INFO:
                    clientSocket = clients[connectionSocket]
                    client_username = clientSocket["username"]
                    clientIP, clientPORT = clientSocket["addr"]
                    
                    infor_message = f"Username: {client_username}\nAddress: {clientIP}:{clientPORT}"
                    connectionSocket.send(infor_message.encode())
                    
                # 0. Normal message                        
                elif message:
                    current_username = clients[connectionSocket]["username"]
                    print(f"[{get_time()}] {current_username}: {message}") # for client
                    broadcast_clients(message, connectionSocket)
                
                # . No content message    
                else:
                    # continue
                    disconnect_closeSocket(connectionSocket)
                    break
            
            except:
                disconnect_closeSocket(connectionSocket)
                break
        
    except: # Error while connecting ?
        disconnect_closeSocket(connectionSocket)
                                        
print(f"Server is running on {serverIP}")
while True:
    try:
        connectionSocket, addr = serverSocket.accept()
        
        thread = threading.Thread(target=handle_client, args=(connectionSocket, addr), daemon=True)
        thread.start()
        
    except KeyboardInterrupt:
        serverSocket.close()
        break
