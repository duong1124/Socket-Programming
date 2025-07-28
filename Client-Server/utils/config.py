# Config 
PORT = 3107
PORT_FILE = 3108
MAX_USERS = 20
SERVER_IP = "192.168.56.1" # for client-side

ADMIN_PASSWORD = "admin123"

# Alias
OPTION_MSG = "/option"
EXIT_MSG = "/EXIT"
GET_LIST_MSG = "/list"
PRIVATE_MSG = "/pm"
GET_INFO = "/whoami"
SEND_FILE_MESSAGE = "/file"

# Commands
COMMANDS = {
    OPTION_MSG : "Show available commands.",
    EXIT_MSG : "Exit chat.",
    GET_LIST_MSG : "List of online users.",
    PRIVATE_MSG : "<username> <message> for private message.",
    GET_INFO : "Get your (local) address and port num.",
    SEND_FILE_MESSAGE : "/file <path> [username] for public/private sending."
}

ADMIN_COMMANDS = {}

clients = {} # socket: {username, addr, is_admin, is_muted}
admin_requests = {}