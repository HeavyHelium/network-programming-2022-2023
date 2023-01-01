import socket
import threading

from data_handler import DataHandler

HEADER = 64
FORMAT = "utf-8"

class Status: 
    def __init__(self, label: str, msg: str) -> None: 
        self._label = label
        self._msg = msg

    def __str__(self) -> str: 
        return f"[{self._label}]: {self._msg}"
    
    def __repr__(self) -> str: 
        return self._label, self._msg

class Server: 
    GREET_MSG = "\nWelcome to the parallel quicksort server!\n"
    DISCONNECT_MSG = "GOTTAGO"
    FORMAT = "<number of processes>, <list of numbers>"
    
    INSTRUCTIONS = f"Please enter data in the following format: \
    { FORMAT }\nTo disconnect, enter { DISCONNECT_MSG }"

    ON_DISCONNECT_MSG = "Goodbye!"

    def __init__(self, 
                 serv_ip=socket.gethostbyname(socket.gethostname()), 
                 port=5050) -> None:
        port = port
        self._addr = serv_ip, port

        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.bind(self.addr)

    @property
    def addr(self) -> tuple[str, int]:
        return self._addr

    @property
    def serv_ip(self) -> str:
        """
            Returns the server's IP address
        """
        return self.addr[0]
    
    @property
    def port(self) -> int:
        return self.addr[1] 

    def __str__(self) -> str: 
        return f"Server { self.serv_ip } on port { self.port }" 

    def __repr__(self) -> str: 
        return self.addr

    @property
    def active_connections(self) -> int:
        # the main thread is always running, 
        # hence the -1
        return threading.active_count() - 1
    
    @property
    def server(self) -> socket.socket:
        """
            Returns the server socket
        """
        return self._server

    # the start thread is always running
    def start(self) -> None: 
        print(Status("STARTING", "Server us is starting"))
        self.server.listen()
        print(Status("LISTENING", str(self)))

        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print()
            print(Status("ACTIVE CONNECTIONS", 
                  str(self.active_connections)))

    def handle_client(self, conn: socket.socket, addr: tuple[str, int]) -> None: 
        print(Status("NEW CONNECTION", 
                     f"{addr} connected."))
        self.send(Server.GREET_MSG + Server.INSTRUCTIONS, conn, process_msg=False)
        connected = True

        while connected: 
            msg = self.receive(conn)
            if msg:
                print(Status("RECEIVED", f"From { addr } got: { msg }"))
                if msg == Server.DISCONNECT_MSG:
                    connected = False
                    self.send(Server.ON_DISCONNECT_MSG, conn, process_msg=False)
                else:
                    self.send(msg, conn)
        conn.close()
        print(Status("DISCONNECTED", f"{ addr } disconnected."))
        # I am printing the number of active connections
        # at the very end of the thread, so it is still active
        # hence the -1
        print()
        print(Status("ACTIVE CONNECTIONS", 
              f"{ self.active_connections - 1 }"))
    
    def receive(self, conn: socket.socket) -> str: 
        msg_len = conn.recv(HEADER).decode(FORMAT)
        # in order to make sure that we're getting a valid mesaage
        # before we try and convert to an int, i.e. 
        # it is not simply None
        # when we connect initially, we receive the empty message 
        msg = ""
        if msg_len:
            msg_len = int(msg_len)
            msg = conn.recv(msg_len).decode(FORMAT)
        return msg     

    def send(self, msg: str, conn: socket.socket, process_msg=True) -> None:
        if process_msg: 
            try: 
                msg = "The sorted list is: " + DataHandler(msg)()
            except Exception as e: 
                msg = str(Status("ERROR", f"Something went wrong with processing your data: { e }"))
            
        message = msg.encode(FORMAT)
        msg_len = len(message)
        send_len = str(msg_len).encode(FORMAT)
        send_len += b' ' * (HEADER - len(send_len))
        conn.send(send_len)
        conn.send(message)

if __name__ == "__main__":
    server = Server()
    server.start()