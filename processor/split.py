#!/usr/bin/env python

import os
import sys
import cv2


def split(image):
    # Read image as 3 color image
    image = cv2.imread(path, 1)

    green = image[:,:, 1]
    red = image[:,:, 2]

    return (green, red)


def read_file(path):
    # Read image as 3 color image
    return cv2.imread(path, 1)


def main(path):
    (root, ext) = os.path.splitext(path)

    image = read_file(path)

    (green, red) = split(image)

    cv2.imwrite("{}_green{}".format(root, ext), green)
    cv2.imwrite("{}_red{}".format(root, ext), red)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
