import socket as s
import threading
import sys
from config import *
from utils import client_receive

clientSocket = s.socket(s.AF_INET, s.SOCK_STREAM)

try: 
    clientSocket.connect((SERVER_IP, PORT))

    receive_thread = threading.Thread(target = client_receive, args = (clientSocket,), daemon=True)
    receive_thread.start()

    while True:
        message = input()
        # Delete typed input
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")
        
        print(f"<YOU> : {message}")
        if message == EXIT_MSG:
            break
        elif message:
            clientSocket.send(message.encode())
        else: # no content sent ?
            continue 
        
except Exception as e:
    print(f"Error: {e}")
    
clientSocket.close()
        
    