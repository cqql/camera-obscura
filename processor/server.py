#!/bin/env python

from flask import Flask, request
from queue import Queue

app = Flask(__name__)
images = Queue()

@app.route("/upload", methods=["POST"])
def save_image():
    images.put(request.get_data())

    return ""

if __name__ == "__main__":
    app.run(host="0.0.0.0")
