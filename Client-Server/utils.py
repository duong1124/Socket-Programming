from config import clients, admin_requests
from datetime import datetime

def get_time():
    return datetime.now().strftime("%H:%M")    

def username_list() -> list:
    return [client_info["username"] for client_info in clients.values()]

def disconnect_closeSocket(connection):
    if connection in clients:
        username = clients[connection]["username"]
        del clients[connection]
        
        if username in admin_requests:
            del admin_requests[username]
            
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
    formatted_message = f"[{get_time()}] {sender_username}: {message}"
    
    for clientSocket in list(clients.keys()):
        if clientSocket != senderSocket:
            try: 
                clientSocket.send(formatted_message.encode())
            except: # send fail
                disconnect_closeSocket(clientSocket)                                      

def socket_by_name(target_username):
    targetSocket = None
    for clientSocket, client_info in clients.items():
        if client_info["username"] == target_username:
            targetSocket = clientSocket
            break
    return targetSocket 

# ======================================= ADDITIONAL FEATURES FUNCTION =======================================

def send_private_message(message, senderSocket, target_username):    
    targetSocket = socket_by_name(target_username)

    sender_username = clients[senderSocket]["username"] if senderSocket in clients else "?"
    if targetSocket:
        private_message = f"[{get_time()}] [PRIVATE] [{sender_username}]: {message}"
        try:
            targetSocket.send(private_message.encode())
        
        except:
            senderSocket.send(f"[{get_time()}] Can't send private message to {target_username}".encode())
    else:
        senderSocket.send(f"[{get_time()}] {target_username} can't be found!".encode())