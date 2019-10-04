import os 

RESOURCES = {"/css": "static/css", "/images": "static/images", "/js": "static/js"}
PAGE_MAP = {"/index": "index.html", "/": "index.html"}
TYPES = {"/images":"image", "/css": "text", "/js": "text"}

class Handler(object):

    def __init__(self, socket, address):

        self.socket = socket
        self.address = address
        self.pages_dir = "pages"
        self.resources = "static"

        self.run()

    def run(self):

        data = self.socket.recv(1024)
        data = data.decode("utf-8")
        split_data = data.split()
        # self.debug(data)

        # method = split_data[0]
        request = split_data[1]
        element = os.path.split(request)[0]
        r_type = self.check_resource_type(element, request)

        if r_type == "page":

            self.send_page(request)
        
        elif r_type == "resource":

            content_type = self.get_content_type(request)
            self.send_resource(request, content_type)

        elif r_type == "error":

            self.send_page(error=True)

    def check_resource_type(self, element, request):

        if element in RESOURCES:
            return "resource"

        elif element in PAGE_MAP:
            return "page"
        
        else:
            return "error"

        return r_type
    
    def get_content_type(self, request):

        type_ = TYPES[os.path.split(request)[0]]
        ext = os.path.splitext(request)[1]

        if ext == ".png" or ext == ".ico":

            return f"{type_}/png"

        elif ext == ".js":

            return f"{type_}/javascript"
        
        elif ext == ".css":

            return f"{type_}/css"

    def send_page(self, request=None, error=False):

        if error:
            response = "HTTP/1.1 404 Not Found\n"
            page = "error.html"

        else:
            response = "HTTP/1.1 200 OK\n"
            page = PAGE_MAP[request]

        path = os.path.join(self.pages_dir, page)
        with open(path, "r") as f:

            data = f.read()

        c_type = "text/html; charset=utf-8"
        headers = self.build_headers(response, len(data), c_type)

        # print(f"sending headers:\n{headers}")
        send = (headers + data).encode("utf-8")

        self.send_data(send)

    def send_resource(self, request=None, content_type="text/html", error=False):

        if error:
            response = "HTTP/1.1 404 Not Found\n"

        else:
            response = "HTTP/1.1 200 OK\n"

        file_ = os.path.basename(request)
        path = os.path.join(RESOURCES[os.path.split(request)[0]], file_)
        with open(path, "rb") as f:

            data = f.read()

        c_type = content_type
        headers = self.build_headers(response, len(data), c_type)

        # print(f"sending headers:\n{headers}")
        send =  headers.encode("utf-8") + data

        self.send_data(send)

    def build_headers(self, response, content_length, content_type):

        length = f"Content-Length: {content_length}\n"
        c_type = f"Content-Type: {content_type}\n"
        conn = "Connection: close\n\n"

        return response + length + c_type + conn

    def send_data(self, data):

        self.socket.sendall(data)

    def debug(self, data):

        for b in data.split("\n"):
            print(b)