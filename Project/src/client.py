import socket


HEADER = 64
PORT = 5050

FORMAT = "utf-8"
DISCONNECT_MESSAGE = "GOTTAGO"

#SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "192.168.0.105"
ADDR = (SERVER, PORT)

class Client: 
    def __init__(self) -> None:
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.connect(ADDR)
        msg = self.receive() # initial message    
        print(msg)

    @property
    def client(self):
        return self._client

    def send(self, msg):
        message = msg.encode(FORMAT)
        send_len = str(len(message)).encode(FORMAT)
        send_len += b' ' * (HEADER - len(send_len))
        self.client.send(send_len) 
        self.client.send(message)
        print(self.receive()) 

    def receive(self) -> str:
        msg_len = self.client.recv(HEADER).decode(FORMAT)
        msg_len = int(msg_len)
        msg = self.client.recv(msg_len).decode(FORMAT)
        return msg
    
    def communiation_loop(self) -> None:
        msg = "42" # initial value doesn't matter
        while True:
            print("$ ", end="")
            msg = input().strip()
            if not msg: 
                continue

            if msg == DISCONNECT_MESSAGE:
                self.send(msg)
                break
            self.send(msg) 



if __name__ == "__main__":
    c = Client()
    c.communiation_loop()

