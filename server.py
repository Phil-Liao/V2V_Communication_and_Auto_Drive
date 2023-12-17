import socket
import threading

# Connection Data
SERVER = '127.0.0.1'
PORT = 7777
FORMAT = 'ascii'
HEADER = 1024

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

#Recieve Messages From One Connected Client
def receive(sender:socket, HEADER=HEADER, FORMAT=FORMAT) -> str:
    message = sender.recv(HEADER).decode(FORMAT)
    return message

#Sending Messages To One Connected Client
def send_to_one(recipiant:socket, message:str, FORMAT=FORMAT):
    message = message.encode(FORMAT)
    recipiant.send(message)

# Sending Messages To All Connected Clients
def broadcast(clients:list, message:str, FORMAT=FORMAT):
    message = message.encode(FORMAT)
    for client in clients:
        client.send(message)


# Handling Messages From Clients
recipiant_nickname = ''
def handle(client):
    while True:
        try:






            # Recieving and Broadcasting Messages
            message = receive(client)
            if (message[:2] == '@!') and (message[-2:] == '!@'):
                recipiant_nickname = message[2:-2]
                print('recipiant, not actual message')
                message = ''
            elif recipiant_nickname == '#ALL#':
                print(message)
                print(nicknames)
                broadcast(clients, message)
                recipiant_nickname = ''
            elif recipiant_nickname in nicknames:
                print(message)
                recipiant_socket = clients[nicknames.index(recipiant_nickname)]
                send_to_one(recipiant_socket, message)
                recipiant_nickname = ''

            

        
        
        
        
        
        
        except:
            # Removing and Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(clients, '{} left!'.format(nickname))
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def listen():
    while True:
        # Accept Connection
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Request And Store Nickname
        send_to_one(client, 'NICK')
        nickname = receive(client)
        nicknames.append(nickname)
        clients.append(client)

        # Print and Broadcast Nickname
        print(f"Nickname is {nickname}")
        broadcast(clients, f"{nickname} joined!")
        send_to_one(client, 'Connected to server!')

        # Start Handling Thread for Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

listen()