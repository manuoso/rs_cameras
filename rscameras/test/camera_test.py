import numpy as np
import cv2
import time
from rscameras.camera_d400 import Camera_D400

# Get camera
cam = Camera_D400()
fps_list = []

while True:
    # Stack both images horizontally
    start_time = time.time()

    images = cam.get_images()
    print(cam.get_depth_point([240, 320], got_frame = 1))
    print(cam.get_depth_point([240, 320], got_frame = 1))
    print(cam.get_depth_point([240, 320], got_frame = 1))
    print(cam.get_depth_point([240, 320], got_frame = 1))
    print(cam.get_depth_point([240, 320], got_frame = 1))
    print(cam.get_depth_point([240, 320], got_frame = 1))
    print(cam.get_depth_point([240, 320], got_frame = 1))
    print(cam.get_depth_point([240, 320], got_frame = 1))
    print(cam.get_depth_point([240, 320], got_frame = 1))


    color = images[0]
    color[235:245,315:325,:] = 0
    images[1][235:245,315:325,:] = 0

    color = np.hstack((color,images[1]))
    # Show images
    cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('RealSense', color)
    fps = 1.0 / (time.time() - start_time)
    if len(fps_list) > 120:
        fps_list.pop(0)
    fps_list.append(fps)
    print("FPS: %.2f FPS_avg: %.2f" % (fps, np.mean(fps_list)))
    cv2.waitKey(1)
