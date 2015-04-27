#!/bin/env python

from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import os


class UploadHandler(BaseHTTPRequestHandler):
    def __init__(self, req, client_addr, server, handler):
        self.handler = handler

        # The super constructor calls do_POST directly, so we need to set
        # self.handler beforehand
        super().__init__(req, client_addr, server)

    def do_POST(self):
        self.handler(self.rfile.read())


class ImageServer(HTTPServer):
    def __init__(self, handler):
        def proxy(req, client_addr, server):
            return UploadHandler(req, client_addr, server, handler)

        super().__init__(("0.0.0.0", 5000), proxy)


def save_to_file(image):
    os.makedirs("images", exist_ok=True)

    filename = "images/{:d}.jpg".format(int(time.time()))

    print("Saving image to {}".format(filename))

    with open(filename, "wb") as file:
        file.write(image)


def main():
    server = ImageServer(save_to_file)
    server.serve_forever()


if __name__ == "__main__":
    main()
