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
        
        #Set pipeline and config
        self.pipeline = rs.pipeline()
        cfg = rs.config()
        cfg.enable_stream(rs.stream.color, self.data['color']['height'], self.data['color']['width'], rs.format.bgr8, self.data['color']['fps'])
        cfg.enable_stream(rs.stream.depth, self.data['depth']['height'], self.data['depth']['width'], rs.format.z16, self.data['depth']['fps'])

        # Start streaming
        profile = self.pipeline.start(cfg)

        depth_sensor = profile.get_device().first_depth_sensor()
        self.depth_scale = depth_sensor.get_depth_scale()

        # Create an align object
        # rs.align allows us to perform alignment of depth frames to others frames
        # The "align_to" is the stream type to which we plan to align depth frames.
        align_to = rs.stream.color
        self.align = rs.align(align_to)

    # ----------------------------------------------------------------------------------------------------
    def get_images(self, image_type = 'both'):
        # Wait for a coherent pair of frames: depth and color
        self.frames = self.pipeline.wait_for_frames()

        if image_type == "both":
        # Get frames
            depth_frame = self.frames.get_depth_frame()
            color_frame = self.frames.get_color_frame()        

        # Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

            return [color_image, depth_colormap]

        elif image_type == "color":
        # Get frames
            color_frame = self.frames.get_color_frame()        

        # Convert images to numpy arrays
            color_image = np.asanyarray(color_frame.get_data())

            return color_image

        elif image_type == "depth":
        # Get frames
            depth_frame = self.frames.get_depth_frame()

        # Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

            return depth_colormap
    # ----------------------------------------------------------------------------------------------------
    def get_aligned_images(self, clipping_distance_in_meters = 1):

        self.frames = self.pipeline.wait_for_frames()

        # Align the depth frame to color frame
        aligned_frames = self.align.process(self.frames)

        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
        color_frame = aligned_frames.get_color_frame()

        # Validate that both frames are valid
        if not aligned_depth_frame or not color_frame:
            pass

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Set clipping distance
        clipping_distance = clipping_distance_in_meters / self.depth_scale

        # Remove background - Set pixels further than clipping_distance to grey
        grey_color = 153
        depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #depth image is 1 channel, color is 3 channels
        bg_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), grey_color, color_image)

        # Render images
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        return [bg_removed, depth_colormap]
    # ----------------------------------------------------------------------------------------------------
    def get_depth_point(self, color_point, got_frame = 0):
        if got_frame:
            frames = self.frames
        else:
            frames = self.pipeline.wait_for_frames()

        # Align the depth frame to color frame
        aligned_frames = self.align.process(frames)

        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image

        # Validate that frames are valid
        if not aligned_depth_frame:
            pass

        depth_image = np.asanyarray(aligned_depth_frame.get_data())

        color_point = [int(color_point[0]), int(color_point[1])]

        depth_point = depth_image[color_point[0], color_point[1]]
        # Transform from depth scale to meters
        depth_point_m = depth_point * self.depth_scale

        return depth_point_m

