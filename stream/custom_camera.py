from imutils.video import VideoStream
from stream.base_camera import BaseCamera
from time import sleep
import imutils
import cv2
import os


class Camera(BaseCamera):

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    def frames():
        camera = VideoStream(src=1).start()
        sleep(0.8)

        while True:

            frame = camera.read()
            frame = imutils.resize(frame, width=480)

            yield cv2.imencode('.jpg', frame)[1].tobytes()
