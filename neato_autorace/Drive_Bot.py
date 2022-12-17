import cv2
from .Detection.Lanes.lane_detection import detect_lane
from numpy import interp

class Control():

    def __init__(self):
        self.angle = 0.0
        self.velocity = 0.1
        self.speed = 80

    def follow_lane(self, max_sane_dist, dist, curv):
        self.speed = 80
        max_turn_angle = 90
        max_turn_angle_negative = -90
        req_turn_angle = 0

        if dist > max_sane_dist and dist < (-1*max_sane_dist):
            if dist > max_sane_dist:
                req_turn_angle = max_turn_angle + curv
            else:
                req_turn_angle = max_turn_angle_negative + curv
        else:
            car_offsite = interp(dist, [-max_sane_dist, max_sane_dist], [-max_turn_angle, max_turn_angle])
            req_turn_angle = car_offsite + curv

        # handle overflow
        if req_turn_angle > max_turn_angle or req_turn_angle < max_turn_angle_negative:
            if req_turn_angle > max_turn_angle:
                req_turn_angle = max_turn_angle 
            else:
                req_turn_angle = max_turn_angle_negative

        # Handle max car turn ability
        self.angle = interp(req_turn_angle, [-max_turn_angle, max_turn_angle], [-30,30])


    def drive(self, current_state):
        [dist, curv, img] = current_state

        if dist!= 1000 and curv!= 1000:
            self.follow_lane(img.shape[1]/4, dist, curv)

        else:
            self.speed = 0.0 
            self.angle = 0.0
        
        # interplating the angle and speed from realworld to motorworls
        self.angle = interp(self.angle, [-30,30], [0.5,-0.5])
        self.speed = interp(self.speed, [30,90], [0.1,0.15])


class Car():
    def __init__(self):
        self.Control = Control()
    def display_state(self,frame_disp,angle_of_car,current_speed):

        # Translate [ ROS Car Control Range ===> Real World angle and speed  ]
        angle_of_car  = interp(angle_of_car,[-0.5,0.5],[45,-45])
        if (current_speed !=0.0):
            current_speed = interp(current_speed  ,[1  ,   2],[30 ,90])

        ###################################################  Displaying CONTROL STATE ####################################

        if (angle_of_car <-10):
            direction_string="[ Left ]"
            color_direction=(120,0,255)
        elif (angle_of_car >10):
            direction_string="[ Right ]"
            color_direction=(120,0,255)
        else:
            direction_string="[ Straight ]"
            color_direction=(0,255,0)

        if(current_speed>0):
            direction_string = "Moving --> "+ direction_string
        else:
            color_direction=(0,0,255)


        cv2.putText(frame_disp,str(direction_string),(20,40),cv2.FONT_HERSHEY_DUPLEX,0.4,color_direction,1)

        angle_speed_str = "[ Angle ,Speed ] = [ " + str(int(angle_of_car)) + "deg ," + str(int(current_speed)) + "mph ]"
        cv2.putText(frame_disp,str(angle_speed_str),(20,20),cv2.FONT_HERSHEY_DUPLEX,0.4,(0,0,255),1)
        
                
    def drive_car(self, frame):
        img = frame[100:480, 0:640]
        img = cv2.resize(img, (320,240))

        distance, curvature = detect_lane(img)

        current_state = [distance, curvature, img]
        self.Control.drive(current_state)

        self.display_state(img,self.Control.angle, self.Control.speed)

        return self.Control.angle, self.Control.speed, img
         

