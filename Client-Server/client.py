import socket as s
import threading
import sys
from config import *
import json 
import os

clientSocket = s.socket(s.AF_INET, s.SOCK_STREAM)

def client_receive(clientSocket):
    while True:
        try:
            message = clientSocket.recv(1024).decode()
            if message:
                # Check for file transfer
                try:
                    data = json.loads(message)
                    if data.get("command") == "file_transfer":
                        upload_file(data)
                        continue
                except:
                    pass 
                
                print(message)
            else:
                break
        except: # connection error
            break
        
def upload_file(file_info):
    pathname, sender, receiver = file_info["filename"], file_info["sender"], file_info["receiver"]
    
    if not os.path.exists(pathname):
        print(f"Can't find file: {pathname}")
        return
    
    try:
        fileSocket = s.socket(s.AF_INET, s.SOCK_STREAM)
        fileSocket.connect((SERVER_IP, PORT_FILE))
        
        # Send metadata - file info
        filesize = os.path.getsize(pathname)
        filename = os.path.basename(pathname)
        metadata = {
            "filename" : filename,
            "filesize" : filesize,
            "sender" : sender,
            "receiver" : receiver
        }
        
        fileSocket.send(json.dumps(metadata).encode()) 
        
        # Send contents of file
        with open(pathname, 'rb') as f: # read binary mode
            bytes_sent = 0
            while bytes_sent < filesize:
                chunk = f.read(4096)
                if not chunk: 
                    break # sent completed
                fileSocket.send(chunk)
                bytes_sent += len(chunk)
                
        # Receive confirmation
        response = fileSocket.recv(1024).decode()
        if response == "FTP":
            print(f"{filename} successfully sent.")
        fileSocket.close()
                
    except Exception as e:
        print(f"Error SENDING FILE: {e}")

try: 
    clientSocket.connect((SERVER_IP, PORT))

    receive_thread = threading.Thread(target = client_receive, args = (clientSocket,), daemon=True)
    receive_thread.start()

    # Sending message
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
