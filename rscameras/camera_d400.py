import numpy as np
import pyrealsense2 as rs
import cv2

from rscameras.camera_base import Camera_Base, TypeExcept

####################################################################################################
class Camera_D400(Camera_Base):
    def __init__(self, config = None):
        Camera_Base.__init__(self, config)

        if(self.data['camera_name'] != "d400"):
            raise TypeExcept("Camera name is not d400")   

        self.pipeline = rs.pipeline()
        cfg = rs.config()
        cfg.enable_stream(rs.stream.color, self.data['color']['height'], self.data['color']['width'], rs.format.bgr8, self.data['color']['fps'])
        cfg.enable_stream(rs.stream.depth, self.data['depth']['height'], self.data['depth']['width'], rs.format.z16, self.data['depth']['fps'])

        # Start streaming
        self.pipeline.start(cfg)

    # ----------------------------------------------------------------------------------------------------
    def image(self):
        # Wait for a coherent pair of frames: depth and color
        frames = self.pipeline.wait_for_frames()

        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        if not depth_frame or not color_frame:
            pass

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        return color_image, depth_colormap
