import socket
import threading

SERVER = '127.0.0.1'
PORT = 7777
FORMAT = 'ascii'
HEADER = 1024

# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

# Recieving Messages from Server
def receive(sender:socket, HEADER=HEADER, FORMAT=FORMAT) -> str:
    message = sender.recv(HEADER).decode(FORMAT)
    return message

# Send String Data to Server
def send_to_server(client:socket, message:str, recipiant=None, FORMAT=FORMAT):
    recipiant = ('@!' + recipiant + '!@').encode(FORMAT)
    client.send(recipiant)
    print(message)
    message = message.encode(FORMAT)
    client.send(message)


# Handle input info
def write():
    while True:
        recipiant = input('Type in your recipitant nickname: (Leave blank for all.)')
        if recipiant == '':
            recipiant = '#ALL#'
        message = input('Type in your message: ')
        message = f'{nickname}: {message}'
        send_to_server(client, message, recipiant)

# Listening to Server and Sending Nickname
def handle():
    while True:
        try:
            # Receive Message from Server
            # If 'NICK' Send Nickname
            message = receive(client)
            if message == 'NICK':
                client.send(nickname.encode(FORMAT))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break



# Starting Threads for Listening and Writing
handle_thread = threading.Thread(target=handle)
handle_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()