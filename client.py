import socket
import threading

SERVER = '127.0.0.1'
PORT = 7777
FORMAT = 'ascii'
HEADER = 1024


# Choosing Username
username = input("Choose your username: ")



# Recieving Messages from Server
def receive(sender:socket, HEADER:int=HEADER, FORMAT:str=FORMAT) -> str:
    message = sender.recv(HEADER).decode(FORMAT)
    return message

# Send String Data to Server
def send_to_server(client:socket, message:str, recipiant:str=None, FORMAT:int=FORMAT):
    recipiant = ('@!' + recipiant + '!@').encode(FORMAT)
    client.send(recipiant)
    print(message)
    message = message.encode(FORMAT)
    client.send(message)
    print(f'Client side sent message: {message}')


# Handle input info
def write(client:socket, username:str=username, FORMAT:str=FORMAT):
    while True:
        recipiant = input('Type in your recipitant nickname: (Leave blank for all.)')
        if recipiant == '':
            recipiant = '#ALL#'
        message = input('Type in your message: ')
        message = f'{username}: {message}'
        send_to_server(client, message, recipiant, FORMAT)

# Listening to Server and Sending Nickname
def handle(client:socket, username:str=username, FORMAT:str=FORMAT, HEADER:int=HEADER):
    while True:
        try:
            # Receive Message from Server
            message = receive(client, HEADER, FORMAT)
            # If 'USERNAME' Send Username
            if message == 'USERNAME':
                client.send(username.encode(FORMAT))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break


def start_connection(SERVER:str=SERVER, PORT:int=PORT, FORMAT:str=FORMAT, HEADER:int=HEADER):
    

    # Connecting To Server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))    

    # Starting Threads for Listening and Writing
    handle_thread = threading.Thread(target=handle, args=(client, username, FORMAT, HEADER))
    handle_thread.start()

    write_thread = threading.Thread(target=write, args=(client, username, FORMAT))
    write_thread.start()



start_connection()