import cv2
from .Detections.Lanes.lane_detection import detect_lane




class Car():

    def drive_neato(self, frame):
        img = frame[0:640, 238:1042]
        img = cv2.resize(img, (320,240))

        detect_lane(img)
