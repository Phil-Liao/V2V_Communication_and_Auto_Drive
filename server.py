import socket
import threading

# Connection Data
SERVER = '127.0.0.1'
PORT = 7778
FORMAT = 'ascii'
HEADER = 1024

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
usernames = []

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
recipiant_username = ''
def handle(client):
    while True:
        try:
            # Recieving and Broadcasting Messages
            message = receive(client)
            if (message[:2] == '@!') and (message[-2:] == '!@'):
                recipiant_username = message[2:-2]
                #print('recipiant, not actual message')
                message = ''
            elif recipiant_username == '#ALL#':
                print(message)
                print(usernames)
                broadcast(clients, message)
                recipiant_username = ''
            elif recipiant_username in usernames:
                print(message)
                recipiant_socket = clients[usernames.index(recipiant_username)]
                send_to_one(recipiant_socket, message)
                recipiant_username = ''
        except:
            # Removing and Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(clients, '{} left!'.format(username))
            usernames.remove(username)
            break

# Receiving / Listening Function
def listen():
    while True:
        # Accept Connection
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Request And Store Username
        send_to_one(client, 'USERNAME')
        username = receive(client)
        usernames.append(username)
        clients.append(client)

        # Print and Broadcast Nickname
        print(f"Username is {username}")
        broadcast(clients, f"{username} joined!")
        send_to_one(client, 'Connected to server!')


        # Start Handling Thread for Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        print(f'Handle thread for nickname: {username} started.')

listen()