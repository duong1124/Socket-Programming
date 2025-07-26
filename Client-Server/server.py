import socket as s
import threading
from config import *
from utils import *
import json 
import os

serverIP = s.gethostbyname(s.gethostname())

serverSocket = s.socket(s.AF_INET, s.SOCK_STREAM) # TCP
serverSocket.bind((serverIP, PORT))
serverSocket.listen(MAX_USERS)

fileSocket = s.socket(s.AF_INET, s.SOCK_STREAM)
fileSocket.bind((serverIP, PORT_FILE))
fileSocket.listen(MAX_USERS)

def handle_admin():
    pass 

def handle_file_loop():
    while True:
        try:
            fileConnection, file_addr = fileSocket.accept()
            thread = threading.Thread(target=handle_file, args = (fileConnection, file_addr), daemon=True)
            thread.start()
        except:
            break
        
def handle_file(fileConnection, file_addr):
    """For receiving file on PORT_FILE"""
    try:
        metadata_file = fileConnection.recv(1024).decode()
        data = json.loads(metadata_file)
        
        filename, filesize, sender, receiver = data["filename"], data["filesize"], data["sender"], data.get("receiver", "ALL")
        
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        
        filepath = os.path.join('uploads', f"{sender}_{filename}")
        with open(filepath, 'wb') as f:
            bytes_received = 0
            while bytes_received < filesize:
                chunk = fileConnection.recv(4096)
                if not chunk:
                    break
                f.write(chunk) # Server write to create real file on disk
                bytes_received += len(chunk)
        
        # Announce that file has been sent
        if receiver == "ALL":
            broadcast_all(f"{sender} sent a file: {filename} - {filesize} bytes")
        else: # Private file sent
            targetSocket = socket_by_name(receiver)
            targetSocket.send(f"[{get_time()}] [PRIVATE] {sender} sent you a file: {filename}.".encode())

        fileConnection.send("FTP")
        
    except Exception as e:
        print(f"Error: {e}")
        
    fileConnection.close()

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
        welcome_message += "\nType /option for options."
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
                elif message == GET_LIST_MSG:
                    online_users = username_list()
                    list_message = f"{len(online_users)} online clients: {', '.join(online_users)}"
                    connectionSocket.send(f"[{get_time()}] {list_message}".encode())
                
                # 3. Option message
                elif message == OPTION_MSG:
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
                
                # 6. Receive 
                elif message.startswith(SEND_FILE_MESSAGE):
                    file_receiver = message[6:].split(' ')
                    filename = file_receiver[0]
                    receiver = file_receiver[1] if len(file_receiver) > 1 else "ALL"
                    
                    file_info = {
                        "command": "file_transfer",
                        "filename": filename,
                        "sender": username,
                        "receiver": receiver,
                    }
                    connectionSocket.send(json.dumps(file_info).encode())
                
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

# Initialize thread for file transfer server
file_thread = threading.Thread(target=handle_file_loop, daemon=True)
file_thread.start()
                                        
print(f"Chat Server is running on {serverIP}:{PORT}")
print(f"File Server is running on {serverIP}:{PORT_FILE}")

while True:
    try:
        connectionSocket, addr = serverSocket.accept() # !BLOCKING
        
        # Create one thread to handle that client
        thread = threading.Thread(target=handle_client, args=(connectionSocket, addr), daemon=True)
        thread.start()
        
    except KeyboardInterrupt:
        serverSocket.close()
        fileSocket.close()
        break
