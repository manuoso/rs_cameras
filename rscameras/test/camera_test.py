import numpy as np
import cv2

from rscameras.camera_d400 import Camera_D400

# Get camera
cam = Camera_D400()

while True:
    # Stack both images horizontally
    images = np.hstack(cam.image())

    # Show images
    cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('RealSense', images)
    cv2.waitKey(1)
