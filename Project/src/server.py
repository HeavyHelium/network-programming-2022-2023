import socket 
from threading import Thread, activeCount


class Server:
    # I am using my local IP address for the server
    # a (server, port) tuple
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = SERVER, 5050
    # The size of the header, 
    # which is the first message sent by the client
    # its meaning is the length of the message to be received in bytes
    HEADER = 64
    FORMAT = "utf-8"
    DISCONNECT_MESSAGE = "!GOTTAGO"

    def __init__(self) -> None:
        """
            Creates a new server and binds it to the specified address
        """
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to this sepcific address
        self._server.bind(Server.ADDR)

    def handle_client(self, conn, addr) -> None: 
        """
            Handle a single client connection to the server
            :param conn: the socket object representing the connection
            :param addr: the address of the client
        """
        print(f"[NEW CONNECTION] { addr } connected.")

        connected = True

        while connected:
            msg = self.receive(conn)
            if not msg is None:
                    
                if msg == Server.DISCONNECT_MESSAGE:
                    connected = False

                print(f"[{ addr }] { msg }")
                self.send(conn, f"Msg {msg} received")
        
        # Client has disconnected
        conn.close()

    def send(self, conn, msg: str) -> None:
        """
            Sends a message to the client
            :param conn: the socket object representing the connection
            :param msg: the message to be sent
        """
        message = msg.encode(Server.FORMAT)
        msg_len = len(message)
        send_len = str(msg_len).encode(Server.FORMAT)
        send_len += b' ' * (Server.HEADER - len(send_len))
        conn.send(send_len)
        conn.send(message)
    
    def receive(self, conn) -> str:
        """
            Receives a message from the client
            :param conn: the socket object representing the connection
        """
        msg_len = int(conn.recv(Server.HEADER).decode(Server.FORMAT))
        msg = conn.recv(msg_len).decode(Server.FORMAT)
        return msg

    @property
    def server(self) -> socket.socket:
        return self._server

    def start(self) -> None:
        """
            Starts the server and listen for connections
            Handles each connection in a new thread
        """
        self.server.listen()
        print(f"[LISTENING] Server is listening on { Server.SERVER }")
        while True:
            # con is a socket object, representing the connection
            conn, addr  = self.server.accept() # wait for a new connection to the server
            thread = Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] { activeCount() - 1 }") # -1 because the main thread is also running


if __name__ == "__main__":
    server = Server()
    server.start()