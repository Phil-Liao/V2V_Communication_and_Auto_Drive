from collections.abc import Callable, Iterable, Mapping
import socket
import threading
import modified_thread


SERVER = '127.0.0.1'
PORT = 7778
FORMAT = 'ascii'
HEADER = 1024


# Choosing Username
username = input("Choose your username: ")

def start_connection(SERVER=SERVER, PORT=PORT): # Connecting To Server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))   
    return client
def end_connection(client, SERVER, PORT, restart=False):
    print("An error occured!")
    client.close()
    if restart:
        start_connection(SERVER, PORT)

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
                return message
        except:
            end_connection(client, restart=True)
            break


def conn(SERVER:str=SERVER, PORT:int=PORT, FORMAT:str=FORMAT, HEADER:int=HEADER):
    

    # Connecting To Server
    client = start_connection(SERVER, PORT)   

    write_thread = threading.Thread(target=write, args=(client, username, FORMAT))
    write_thread.start()
    
    while True:
        
        # Starting Threads for Listening and Writing
        handle_thread = modified_thread.CustomThread(target=handle, args=(client, username, FORMAT, HEADER))
        
        handle_thread.start()
        handle_thread.join()
        print(handle_thread.join())



conn()
