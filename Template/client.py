import socket
import threading

SERVER = '127.0.0.1'
PORT = 7779
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
        return _client
    def end_connection(self) -> None: # End Connection to Server
        self.client.close()
    def receive_from_server(self) -> str: # Receive Data from Server
        _data = self.client.recv(self.HEADER)
        _data = _data.decode(self.FORMAT)
        return _data
    def send_to_server(self, data:str) -> None: # Send Data to Server
        data = data.encode(FORMAT)
        self.client.send(data)
    def handle(self): # Listening to Server and Sending Nickname
        while True:
            try:
                message = self.receive_from_server()
                if message == self.KEYS['USERNAME_KEY']:
                    self.send_to_server(self.username)
                else:
                    print(message)
            except:
                # Close Connection When Error
                print("An error occured!")
                self.end_connection()
                break
    def write(self): # Inputting String Data
        while True:
            _message = '{}: {}'.format(username, input(''))
            self.send_to_server(_message)




username = input("Input username: ")

connection = conn(username, SERVER, PORT, HEADER, FORMAT)
# Starting Threads For Listening And Writing
handle_thread = threading.Thread(target=connection.handle, )
handle_thread.start()

write_thread = threading.Thread(target=connection.write, )
write_thread.start()