import time
import socket
import requests
import threading

from Config import Config
from HandleClient import Handler

class Server(object):

    def __init__(self):

        super().__init__()

    def run(self):

        c = Config()
        c.load_config()

        host = c.get_param("host")
        port = c.get_param("port")

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Listening on {host}:{port}")

        while True:

            print("Waiting")
            (client_socket, address) = server_socket.accept()

            t = threading.Thread(target=Handler, args=[client_socket, address])
            t.start()
            t.join()

if __name__ == "__main__":
    
    s = Server()
    s.run()