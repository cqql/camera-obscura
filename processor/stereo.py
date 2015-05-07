#!/usr/bin/env python

import os
import sys
import cv2
import numpy as np

from matplotlib import pyplot as plt


def stereo(left, right):
    bm = cv2.StereoBM_create(numDisparities=16, blockSize=15)
    bm.setUniquenessRatio(1)

    disp = bm.compute(left, right)

    return cv2.normalize(disp, np.array([]), 0, 255, cv2.NORM_MINMAX,
                         cv2.CV_8U)


def main(left_path, right_path):
    left = cv2.imread(left_path, 0)
    right = cv2.imread(right_path, 0)

    result = stereo(left, right)

    (root, ext) = os.path.splitext(left_path)
    prefix = os.path.commonprefix([left_path, right_path])[:-1]
    cv2.imwrite("{}_stereo{}".format(prefix, ext), result)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        main(*sys.argv[1:3])
