from config import clients, GET_LIST_MSG, EXIT_MSG
from datetime import datetime

def get_time():
    return datetime.now().strftime("%H:%M")    

def username_list() -> list:
    return [client_info["username"] for client_info in clients.values()]

def disconnect_closeSocket(connection):
    if connection in clients:
        username = clients[connection]["username"]
        
        del clients[connection]
        broadcast_all(f"{username} left the chat.")
        
    connection.close()

def broadcast_all(message):
    admin_message = f"[{get_time()}] [ADMIN] {message}"
    
    for clientSocket in list(clients.keys()):
        try:
            clientSocket.send(admin_message.encode())
        except:
            disconnect_closeSocket(clientSocket)
            
def broadcast_clients(message, senderSocket):
    sender_username = clients[senderSocket]["username"] if senderSocket in clients else "?"
    formatted_message = f"[{get_time()} {sender_username}: {message}]"
    
    for clientSocket in list(clients.keys()):
        if clientSocket != senderSocket:
            try: 
                clientSocket.send(formatted_message.encode())
            except: # send fail
                disconnect_closeSocket(clientSocket)
                
def client_receive(clientSocket):
    while True:
        try:
            message = clientSocket.recv(1024).decode()
            if message:
                print(message)
            else:
                break
        except: # connection error
            break
        