#!/usr/bin/env python

import os
import sys
import cv2
import numpy as np

from matplotlib import pyplot as plt


def stereo(left, right):
    bm = cv2.StereoSGBM_create(blockSize=5,
                               numDisparities=16,
                               preFilterCap=4,
                               minDisparity=-64,
                               uniquenessRatio=1,
                               speckleWindowSize=150,
                               speckleRange=2,
                               disp12MaxDiff=10,
                               P1=200,
                               P2=800)

    disp = bm.compute(left, right)

    x = cv2.normalize(disp, np.array([]), 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    import ipdb
    ipdb.set_trace()
    return x


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
