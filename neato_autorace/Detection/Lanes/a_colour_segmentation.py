import cv2
import numpy as np
from .Morph_op import BwareaOpen, Ret_LowestEdgePoints, RetLargestContour_OuterLane


max_value = 255
max_value_H = 360//2
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value
window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'

white_l_hue = 19
white_h_hue = 100
white_l_sat = 0
white_h_sat = 135
white_l_val = 183
white_h_val = 255

yellow_l_hue = 14
yellow_h_hue = 90
yellow_l_sat = 65
yellow_h_sat = 255
yellow_l_val = 0
yellow_h_val = 255

def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv2.setTrackbarPos(low_H_name, window_detection_name, low_H)
def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv2.setTrackbarPos(high_H_name, window_detection_name, high_H)
def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv2.setTrackbarPos(low_S_name, window_detection_name, low_S)
def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv2.setTrackbarPos(high_S_name, window_detection_name, high_S)
def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv2.setTrackbarPos(low_V_name, window_detection_name, low_V)
def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv2.setTrackbarPos(high_V_name, window_detection_name, high_V)

cv2.namedWindow(window_capture_name)
cv2.namedWindow(window_detection_name)
cv2.createTrackbar(low_H_name, window_detection_name , low_H, max_value_H, on_low_H_thresh_trackbar)
cv2.createTrackbar(high_H_name, window_detection_name , high_H, max_value_H, on_high_H_thresh_trackbar)
cv2.createTrackbar(low_S_name, window_detection_name , low_S, max_value, on_low_S_thresh_trackbar)
cv2.createTrackbar(high_S_name, window_detection_name , high_S, max_value, on_high_S_thresh_trackbar)
cv2.createTrackbar(low_V_name, window_detection_name , low_V, max_value, on_low_V_thresh_trackbar)
cv2.createTrackbar(high_V_name, window_detection_name , high_V, max_value, on_high_V_thresh_trackbar)

def get_mask_and_edge_of_large_object(frame, mask, min_area):
    frame_roi = cv2.bitwise_and(frame, frame, mask=mask)
    frame_roi_gray = cv2.cvtColor(frame_roi, cv2.COLOR_BGR2GRAY)
    mask_of_larger_object = BwareaOpen(frame_roi_gray, min_area)
    frame_roi_gray = cv2.bitwise_and(frame_roi_gray, mask_of_larger_object)
    # extract edge of large objects
    frame_roi_smoothed = cv2.GaussianBlur(frame_roi_gray,(11,11),1)
    edge_of_larger_objects = cv2.Canny(frame_roi_smoothed, 50,150,None,3)

    return mask_of_larger_object, edge_of_larger_objects

def OuterLaneROI(frame,mask,minArea):

    Outer_Points_list=[]

    # 5a. Extracted OuterLanes Mask And Edge
    frame_Lane = cv2.bitwise_and(frame,frame,mask=mask)#Extracting only RGB from a specific region
    Lane_gray = cv2.cvtColor(frame_Lane,cv2.COLOR_BGR2GRAY)# Converting to grayscale
    Lane_gray_opened = BwareaOpen(Lane_gray,minArea) # Getting mask of only objects larger then minArea
    Lane_gray = cv2.bitwise_and(Lane_gray,Lane_gray_opened)# Getting the gray of that mask
    Lane_gray_Smoothed = cv2.GaussianBlur(Lane_gray,(11,11),1)# Smoothing out the edges for edge extraction later
    Lane_edge = cv2.Canny(Lane_gray_Smoothed,50,150, None, 3) # Extracting the Edge of Canny

    # 5b. Kept Larger OuterLane
    ROI_mask_Largest,Largest_found = RetLargestContour_OuterLane(Lane_gray_opened,minArea) # Extracting the largest Yellow object in frame

    if(Largest_found):
        # 5c. Kept Larger OuterLane [Edge]
        Outer_edge_Largest = cv2.bitwise_and(Lane_edge,ROI_mask_Largest)
        # 5d. Returned Lowest Edge Points
        Lane_TwoEdges, Outer_Points_list = Ret_LowestEdgePoints(ROI_mask_Largest)
        Lane_edge = Outer_edge_Largest
    else:
        Lane_TwoEdges = np.zeros(Lane_gray.shape,Lane_gray.dtype)

    #cv2.imshow('frame_Lane',frame_Lane)
    #cv2.imshow('Lane_gray',Lane_gray)
    #cv2.imshow('Lane_gray_opened',Lane_gray_opened)
    #cv2.imshow('Lane_gray_Smoothed',Lane_gray_Smoothed)
    #cv2.imshow('Lane_edge_ROI',Lane_edge_ROI)

    #cv2.imshow('ROI_mask_Largest',ROI_mask_Largest)
    #cv2.imshow('Lane_edge',Lane_edge)
    #cv2.imshow('Lane_TwoEdges',Lane_TwoEdges)
    return Lane_edge,Lane_TwoEdges,Outer_Points_list

def LaneROI(frame,mask,minArea):
    
    # 4a. Keeping only Midlane ROI of frame
    frame_Lane = cv2.bitwise_and(frame,frame,mask=mask)#Extracting only RGB from a specific region
    # 4b. Converting frame to grayscale
    Lane_gray = cv2.cvtColor(frame_Lane,cv2.COLOR_BGR2GRAY) # Converting to grayscale
    # 4c. Keep Only larger objects
    Lane_gray_opened = BwareaOpen(Lane_gray,minArea) # Getting mask of only objects larger then minArea
    
    Lane_gray = cv2.bitwise_and(Lane_gray,Lane_gray_opened)# Getting the gray of that mask
    Lane_gray_Smoothed = cv2.GaussianBlur(Lane_gray,(11,11),1) # Smoothing out the edges for edge extraction later

    # 4d. Keeping only Edges of Segmented ROI    
    Lane_edge = cv2.Canny(Lane_gray_Smoothed,50,150, None, 3) # Extracting the Edge of Canny

    #cv2.imshow('ROI_mask',mask)
    #cv2.imshow('frame_Lane',frame_Lane)
    #cv2.imshow('Lane_gray',Lane_gray)
    #cv2.imshow('Lane_gray_opened',Lane_gray_opened)
    #cv2.imshow('Lane_gray_Smoothed',Lane_gray_Smoothed)
    #cv2.imshow('Lane_edge',Lane_edge)

    return Lane_edge,Lane_gray_opened
    
def segment_white_lane(frame, white_regions, min_area):
    white_lane_mask, white_lane_edge = get_mask_and_edge_of_large_object(frame, white_regions, min_area)
    return white_lane_mask, white_lane_edge

def segment_yellow_lane(frame, yellow_regions, min_area):
    outter_points_list = []
    mask, edge = get_mask_and_edge_of_large_object(frame, yellow_regions, min_area)
    return mask, edge


def segment_lanes(frame, min_area):

    frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame_threshold = cv2.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))

    white_mask = cv2.inRange(frame_HSV, (white_l_hue, white_l_sat, white_l_val), (white_h_hue, white_h_sat, white_h_val))
    yellow_mask = cv2.inRange(frame_HSV, (yellow_l_hue, yellow_l_sat, yellow_l_val), (yellow_h_hue, yellow_h_sat, yellow_h_val))
    
    Outer_edge_ROI,OuterLane_SidesSeperated,Outer_Points_list = OuterLaneROI(frame,yellow_mask,min_area+500)#27msec
    Mid_edge_ROI,Mid_ROI_mask = LaneROI(frame,white_mask,min_area)
    cv2.imshow(window_capture_name, frame)
    cv2.imshow(window_detection_name, frame_threshold)
    # cv2.imshow("white lane", white_mask)
    # cv2.imshow("yellow lane", yellow_mask)
    cv2.waitKey(1)
    return Mid_edge_ROI,Mid_ROI_mask,Outer_edge_ROI,OuterLane_SidesSeperated,Outer_Points_list

    # white_lane_mask, white_lane_edge = segment_white_lane(frame, white_mask, min_area)
    # yellow_lane_mask, yellow_lane_edge = segment_yellow_lane(frame, yellow_mask, min_area)

    # return white_lane_mask, white_lane_edge, yellow_lane_mask, yellow_lane_edge, Outer_Points_list

    # return white_lane_mask, white_lane_edge