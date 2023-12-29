import socket
import threading

# Connection Data
HOST = '127.0.0.1'
PORT = 7777
HEADER = 1024
FORMAT = 'ascii'




KEYS = {'USERNAME_KEY':'USERNAME'}

class central_server:
    def __init__(self, clients:list[socket.socket], usernames:list[str], HOST:str=HOST, PORT:int=PORT, HEADER:int=HEADER, FORMAT:str=FORMAT, KEYS:dict[str, str]=KEYS) -> None:
        self.clients = clients
        self.usernames = usernames
        self.HOST = HOST
        self.PORT = PORT
        self.HEADER = HEADER
        self.FORMAT = FORMAT
        self.KEYS = KEYS
        self.server = self.start_server()
    def start_server(self) -> None: # Start the Server
        _server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _server.bind((self.HOST, self.PORT))
        _server.listen()
        return _server
    def end_server(self) -> None: #End the Server
        self.server.close()
    def send_to_one(self, _client:socket.socket, _data:str) -> None: # Send Data to One Client
        _data = _data.encode(self.FORMAT)
        _client.send(_data)
    def broadcast(self, _data:str) -> None: # Sending Data to All Connected Clients
        _data = _data.encode(self.FORMAT)
        for client in self.clients:
            client.send(_data)
    def receive(self, client:socket.socket) -> str: # Receiving and Decoding Data from Client
        _data = client.recv(self.HEADER)
        _data = _data.decode(self.FORMAT)
        return _data
    def remove_client(self, _client:socket.socket) -> None: # Removing And Closing Clients
        _index = self.clients.index(_client)
        self.clients.remove(_client)
        _client.close()
        _username = self.usernames[_index]
        self.broadcast('{} left!'.format(self._username))
        self.usernames.remove(_username)
    def handle_client(self, _client:socket.socket) -> None: # Handling Messages from Clients
        while True:
            try:
                _message = self.receive(_client)
                self.broadcast(_message)
            except:
                self.remove_client(_client)
                break
    def add_client(self) -> None: # Listening Function
        while True:
            # Accept Connection
            _client, _address = self.server.accept()
            print("Connected with {}".format(str(_address)))

            # Request And Store Nickname

            self.send_to_one(_client, self.KEYS['USERNAME_KEY'])
            _username = self.receive(_client)
            self.usernames.append(_username)
            self.clients.append(_client)

            # Print And Broadcast Username
            print("Username is {}".format(_username))
            self.broadcast(f'{_username} joined!')
            self.send_to_one(_client, 'Connected to server!')

            # Start Handling Thread For Client
            thread = threading.Thread(target=(self.handle_client), args=(_client,))
            thread.start()  
# Lists for Clients and Their Usernames
clients = []
usernames = []
conn = central_server(clients, usernames)
conn.add_client()