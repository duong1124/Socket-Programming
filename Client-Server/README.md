# Python Socket Chatroom

A simple multi-client Client-Server chatroom application using Python sockets and threading.

## Features

- Username authentication (unique)
- Private messaging between users (`/pm <username> <message>`)
- List all online users (`/list`)
- Show available commands (`/option`)
- Get your own info (`/whoami`)
- File transfer TCP
- SSL Socket connection

## SSL/TSL Handshale

1. Generate a root CA with `ca.key` and `ca.crt` for signing server certificates.  

```
openssl genrsa -out ca.key 2048 
openssl req -x509 -new -nodes -key ca.key -sha256 -days 365 -out ca.crt
```

2. Create a private key `server.key` and a CSR `server.csr` for the server.  

```
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr
```

3. Use the CA to sign the CSR and generate `server.crt` for TLS authentication.

```
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365 -sha256
```

## Future

- Folder transfer TCP
- Chat room requests (Accept/Deny by Admin/Server?)
- Admin system (admin password, admin requests)
- Admin command (/kick, /mute, /all bs?)

This project is for educational purposes and demonstrates basic socket programming and multi-threaded server/client design in Python.
