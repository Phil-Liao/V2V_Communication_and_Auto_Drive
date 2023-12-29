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
    def send_to_one(self, client:socket.socket, data:str) -> None: # Send Data to One Client
        data = data.encode(self.FORMAT)
        client.send(data)
    def broadcast(self, data:str, skips:socket.socket=None) -> None: # Sending Data to All Connected Clients
        data = data.encode(self.FORMAT)
        for client in self.clients:
            if client != skips:
                client.send(data)
    def receive(self, client:socket.socket) -> str: # Receiving and Decoding Data from Client
        _data = client.recv(self.HEADER)
        _data = _data.decode(self.FORMAT)
        return _data
    def remove_client(self, client:socket.socket) -> None: # Removing And Closing Clients
        _index = self.clients.index(client)
        self.clients.remove(client)
        client.close()
        _username = self.usernames[_index]
        self.broadcast('{} left!'.format(self._username))
        self.usernames.remove(_username)
    def handle_client(self, client:socket.socket) -> None: # Handling Messages from Clients
        while True:
            try:
                _message = self.receive(client)
                self.broadcast(_message, client)
            except:
                self.remove_client(client)
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
            _thread = threading.Thread(target=(self.handle_client), args=(_client,))
            _thread.start()  
# Lists for Clients and Their Usernames
clients = []
usernames = []
conn = central_server(clients, usernames, HOST, PORT, HEADER, FORMAT, KEYS)
conn.add_client()