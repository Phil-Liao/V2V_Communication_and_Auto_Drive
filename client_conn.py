import socket
import threading
import modified_thread

SERVER = '127.0.0.1'
PORT = 7777
HEADER = 1024
FORMAT = 'ascii'



KEYS = {'USERNAME_KEY':'USERNAME'}
class conn:
    def __init__(self, username:str, SERVER:str=SERVER, PORT:int=PORT, HEADER:int=HEADER, FORMAT:str=FORMAT, KEYS:dict[str, str]=KEYS) -> None:
        self.username = username
        self.SERVER = SERVER
        self.PORT = PORT
        self.HEADER = HEADER
        self.FORMAT = FORMAT
        self.KEYS = KEYS
        self.client = self.start_connection()
    def start_connection(self) -> socket.socket: # Start Connection to Server
        _client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _client.connect((self.SERVER, self.PORT))
        print(f'[CONNECTED] Connection to SERVER:{self.SERVER} successful.')
        return _client
    def end_connection(self) -> None: # End Connection to Server
        self.client.close()
        print(f'[DISCONNECTED] Connection to SERVER:{self.SERVER} ended.')
    def receive_from_server(self) -> str: # Receive Data from Server
        _data = self.client.recv(self.HEADER)
        _data = _data.decode(self.FORMAT)
        return _data
    def send_to_server(self, data:str) -> None: # Send Data to Server
        data = data.encode(FORMAT)
        self.client.send(data)
        print(f'[SENT] Message successfully sent to SERVER:{self.SERVER}.')
    def handle(self) -> str or bool: # Listening to Server and Sending Nickname
        while True:
            try:
                message = self.receive_from_server()
                if message == self.KEYS['USERNAME_KEY']:
                    self.send_to_server(self.username)
                else:
                    #print(message)
                    return message
            except:
                print("An error occured!")
                return False
    def test_write(self) -> None: # Inputting String Data
        while True:
            _message = '{}: {}'.format(username, input(''))
            self.send_to_server(_message)




username = input("Input username: ")

connection = conn(username, SERVER, PORT, HEADER, FORMAT)

test_write_thread = threading.Thread(target=connection.test_write, )
test_write_thread.start()


# Starting Threads For Listening And Writing
#handle_thread = threading.Thread(target=connection.handle, )
#handle_thread.start()
while True:
    handle_thread = modified_thread.CustomThread(target=connection.handle, )
    handle_thread.start()
    handle_thread.join()
    if type(handle_thread.join()) == str:
        print(handle_thread.join())
    if handle_thread.join() == False:
        connection.end_connection()
        connection.start_connection()
