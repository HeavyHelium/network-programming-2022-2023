import socket
from server import Server



class Client:
    def __init__(self) -> None:
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.connect(Server.ADDR)

    @property
    def client(self) -> socket.socket:
        return self._client

    def send(self, msg: str) -> None:
        message = msg.encode(Server.FORMAT)
        msg_len = len(message)
        send_len = str(msg_len).encode(Server.FORMAT)
        send_len += b' ' * (Server.HEADER - len(send_len))
        self.client.send(send_len)
        self.client.send(message)

    def receive(self) -> str:
        msg_len = int(self.client.recv(Server.HEADER).decode(Server.FORMAT))
        msg = self.client.recv(msg_len).decode(Server.FORMAT)
        return msg

if __name__ == "main":
    client = Client()
    client.send("Hello World!")
    print(client.receive())