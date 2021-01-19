import os
import time
import numpy as np
import cv2
from rscameras.camera_d400 import Camera_D400

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.makedirs(os.path.join(REPO_ROOT, 'bags'), exist_ok = True)

time_name = str(time.localtime().tm_hour)+'_'+str(time.localtime().tm_min)+'_'+str(time.localtime().tm_sec)
dataset_name = os.path.join(REPO_ROOT, 'bags', 'dataset_'+time_name)
os.makedirs(dataset_name, exist_ok = True)

# Get camera
cam = Camera_D400()
fps_list = []

store_index = 1

while True:
    # Stack both images horizontally
    start_time = time.time()

    images = cam.get_images()

    # Show images
    # images_show = np.hstack((images[0],images[1]))

    # cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
    # cv2.imshow('RealSense', images_show)
    
    # FPS
    fps = 1.0 / (time.time() - start_time)
    if len(fps_list) > 120:
        fps_list.pop(0)
    fps_list.append(fps)
    print("FPS: %.2f FPS_avg: %.2f" % (fps, np.mean(fps_list)))

    # Save images
    img_index = '{:06d}'.format(store_index)
    img_color_name = dataset_name + '/color_' + img_index + '.jpeg'
    cv2.imwrite(img_color_name, images[0])

    img_depth_name = dataset_name + '/depth_' + img_index + '.jpeg'
    cv2.imwrite(img_depth_name, images[1])

    store_index += 1

    cv2.waitKey(1)
