import socket
import threading
import time
from typing import Callable

from data_handler import DataHandler

HEADER = 64

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())

ADDR = (SERVER, PORT)
FORMAT = "utf-8"


class Server: 
    GREET_MSG = "\nWelcome to the parallel quicksort server!\n"
    DISCONNECT_MESSAGE = "GOTTAGO"
    FORMAT = "<number of processes>, <list of numbers>"
    INSTRUCTIONS = f"Please enter data in the following format: {FORMAT}\nTo disconnect, enter {DISCONNECT_MESSAGE}"
    
    def __init__(self) -> None:
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.bind(ADDR)
    
    @property
    def server(self):
        return self._server

    # the start thread is always running
    def start(self): 
        print("[STARTING] Server is starting")
        self.server.listen()
        print(f"[LISTENING] Server is listening on { SERVER }")
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] { threading.active_count() - 1 }")

    def handle_client(self, conn, addr): 
        print(f"[NEW CONNECTION] { addr } connected.")
        self.send(Server.GREET_MSG + Server.INSTRUCTIONS, conn, process_msg=False)
        connected = True

        while connected: 
            msg = self.receive(conn)
            if msg:
                print(f"From { addr } got: { msg }")
                if msg == Server.DISCONNECT_MESSAGE: 
                    connected = False
                    self.send("Goodbye!", conn, process_msg=False)
                else: 
                    self.send(msg, conn)
        conn.close()
    
    def receive(self, conn) -> str: 
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

    def send(self, msg: str, conn, process_msg=True):
        if process_msg: 
            try: 
                msg = "The sorted list is: " + DataHandler(msg)()
            except Exception as e: 
                msg = f"Something went wrong with processing your data: {e}"
            
        message = msg.encode(FORMAT)
        msg_len = len(message)
        send_len = str(msg_len).encode(FORMAT)
        send_len += b' ' * (HEADER - len(send_len))
        conn.send(send_len)
        conn.send(message)

if __name__ == "__main__":
    server = Server()
    server.start()