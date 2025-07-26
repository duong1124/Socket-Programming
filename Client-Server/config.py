# Config 
PORT = 3107
MAX_USERS = 10
SERVER_IP = "192.168.56.1" # for client-side

# Alias
OPTION_MSG = "/option"
EXIT_MSG = "/EXIT"
GET_LIST_MSG = "/list"

# Commands
COMMANDS = {
    OPTION_MSG : "Show available commands.",
    EXIT_MSG : "Exit chat.",
    GET_LIST_MSG : "List of online users"
}

clients = {}
