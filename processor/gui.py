#!/bin/env python

from tkinter import Tk, Frame, Label, Button
from threading import Thread
from PIL import Image
from PIL.ImageTk import PhotoImage
from queue import Queue, Empty

import io

from server import ImageServer


class ImageWidget(Label):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.holder = None
        self.original = None
        self.resized = None

        self.bind("<Configure>", self.on_resize)

    def set_image(self, image):
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
    def __init__(self, master, images):
        super().__init__(master)

        self.images = images

        dimensions = {"relwidth": 0.5, "relheight": 0.5}

        self.original_holder = ImageWidget(self)
        self.original_holder.place(**dimensions)

        self.red_holder = ImageWidget(self, bg="red")
        self.red_holder.place(relx=1, rely=0, anchor="ne", **dimensions)

        self.green_holder = ImageWidget(self, bg="green")
        self.green_holder.place(relx=0, rely=1, anchor="sw", **dimensions)

        self.rotated_holder = ImageWidget(self, bg="teal")
        self.rotated_holder.place(relx=1, rely=1, anchor="se", **dimensions)

        self.after_idle(self.load_image)

    def load_image(self):
        try:
            data = self.images.get_nowait()
            image = Image.open(io.BytesIO(data))

            self.original_holder.set_image(image)
        except Empty:
            pass

        self.after(1000, self.load_image)


def main():
    images = Queue()

    server = ImageServer(images.put_nowait)
    Thread(target=lambda: server.serve_forever()).start()

    root = Tk()

    def cleanup():
        root.destroy()
        server.shutdown()

    root.protocol("WM_DELETE_WINDOW")

    gui = GUI(root, images)
    gui.pack(fill="both", expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()
