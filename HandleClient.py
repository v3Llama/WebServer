import time
import threading

MAPPINGS = {"/index": "index.html", "/": "index.html"}

class Handler(object):

    def __init__(self, socket, address):

        self.socket = socket
        self.address = address

        self.run()

    def run(self):

        alive = True

        while alive:

            data = self.socket.recv(1024)
            alive = bool(data)

            resource = self.get_resource(data)
            page = self.get_page(resource)
            self.send_page(page)

            if not alive:
                print(f"{self.address[0]} is dead")
                break
            
            time.sleep(0.5)
            break

    def get_resource(self, data):

        headers = data.decode("utf-8").split()
        print(headers[1])
        path = headers[1]

        return path

    def get_page(self, resource):

        try:

            header = "HTTP/1.1 200 OK\n\n"
            page = MAPPINGS[resource]

        except KeyError:

            header = "HTTP/1.1 404 Not Found\n\n"
            page = "error.html"

        with open(page, "r") as f:
            
            data = f.read()

        return bytes(header + data, "utf-8")

    def send_page(self, page):

        self.socket.sendall(page)