import socket

class Connection:

    def __init__(self, client_id, client_ip):
        self.client_id = client_id
        self.client_ip = client_ip
    
    def verify(self):
        # TODO: Verify to prevent ip and identity spoofing. Auth will be important
        pass

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.client_ip, 80)) # Add config later for choosing port

    def send(self, action):
        #TODO: Make conversational protocol for sending data over sockets
        pass

    def receive(self, callback):
        #TODO: Make conversational protocol for sending data over sockets
        pass

    # We may need a watchdog thread or something to detect disconnects and update
    # other players in real time