#!/bin/env python

from tkinter import Tk, Frame, Label, Button
from threading import Thread
from PIL import Image
from PIL.ImageTk import PhotoImage

import queue
import io
import cv2
import numpy as np

from server import ImageServer, save_to_file
from split import split


class ImageWidget(Label):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.holder = None
        self.original = None
        self.resized = None

        self.bind("<Configure>", self.on_resize)

    def set_image(self, data):
        image = Image.open(io.BytesIO(data))

        self.original = image
        self.resize_image()
        self.draw_image()

    def on_resize(self, event):
        if self.original:
            self.resize_image()
            self.draw_image()

    def draw_image(self):
        # We have to keep this reference, so that the image holder is not GCed
        self.holder = PhotoImage(self.resized)

        self.configure(image=self.holder)

    def resize_image(self):
        size = (self.winfo_width(), self.winfo_height())
        self.resized = self.original.resize(size)


class GUI(Frame):
    def __init__(self, master):
        super().__init__(master)

        dimensions = {"relwidth": 0.5, "relheight": 0.5}

        self.original_holder = ImageWidget(self)
        self.original_holder.place(**dimensions)

        self.red_holder = ImageWidget(self, bg="red")
        self.red_holder.place(relx=1, rely=0, anchor="ne", **dimensions)

        self.green_holder = ImageWidget(self, bg="green")
        self.green_holder.place(relx=0, rely=1, anchor="sw", **dimensions)

        self.rotated_holder = ImageWidget(self, bg="teal")
        self.rotated_holder.place(relx=1, rely=1, anchor="se", **dimensions)

    def set_image(self, data_bytes):
        data = np.frombuffer(data_bytes, dtype="uint8")
        cv2im = cv2.imdecode(data, 1)
        (cv2green, cv2red) = split(cv2im)
        _, green = cv2.imencode(".jpeg", cv2green)
        _, red = cv2.imencode(".jpeg", cv2red)

        self.original_holder.set_image(data)
        self.green_holder.set_image(green)
        self.red_holder.set_image(red)


def main():
    images = queue.Queue(maxsize=1)

    def queue_image(image):
        print("Received image")

        save_to_file(image)

        try:
            images.put_nowait(image)
        except queue.Full:
            print("Dropped image, because queue is full")

    server = ImageServer(queue_image)
    Thread(target=lambda: server.serve_forever()).start()

    root = Tk()

    def cleanup():
        root.destroy()
        server.shutdown()

    root.protocol("WM_DELETE_WINDOW")

    gui = GUI(root)
    gui.pack(fill="both", expand=True)

    def pop_image():
        try:
            data = images.get_nowait()

            gui.set_image(data)
        except queue.Empty:
            pass

        gui.after(1000, pop_image)

    gui.after_idle(pop_image)

    root.mainloop()


if __name__ == "__main__":
    main()
