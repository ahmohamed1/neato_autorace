import cv2
from .Detection.Lanes.lane_detection import detect_lane




class Car():

    def drive_car(self, frame):
        img = frame[100:480, 0:640]
        img = cv2.resize(img, (320,240))

        detect_lane(img)
