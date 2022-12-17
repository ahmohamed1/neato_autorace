import cv2
import numpy as np



# color range
hue_l_l = 0
hue_h_l = 0
lit_l = 255
sat_l = 0

hue_l_h = 0
hue_h_h = 255
lit_h = 255
sat_h = 255
HLS = 0
src = 0

def color_segment(HLS, lower_range, upper_range):

    lower = np.array( [lower_range[0],lower_range[1] ,lower_range[2]] )
    upper = np.array( [upper_range[0]    ,255     ,255])
    mask_in_range = cv2.inRange(HLS,lower_range, upper_range)
    kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    mask_dilated= cv2.morphologyEx(mask_in_range, cv2.MORPH_DILATE, kernal)
    return mask_dilated

def maskextract():
    mask = color_segment(HLS, (hue_l_l, lit_l, sat_l), (hue_l_h,255,255))
    mask_y = color_segment(HLS, (hue_l_h, lit_h, sat_h), (hue_h_h,255,255))

    mask_ = mask != 0
    dst = src * (mask_[:,:,None].astype(src.dtype))

    mask_y = mask != 0
    dst_y = src * (mask_y[:,:,None].astype(src.dtype))

    cv2.imshow("lane_1", dst)
    cv2.imshow("lane_2", dst_y)

def on_hue_low_change(val):
    global hue_l_l
    hue_l_l = val
    maskextract()

def on_hue_high_low_change(val):
    global hue_h_l
    hue_h_l = val
    maskextract()

def on_lit_low_change(val):
    global lit_l
    lit_l = val
    maskextract()

def on_sat_low_chnage(val):
    global sat_l
    sat_l = val
    maskextract()

def on_hue_low_high_change(val):
    global hue_l_h
    hue_l_h = val
    maskextract()

def on_hue_high_change(val):
    global hue_h_h
    hue_h_h = val
    maskextract()

def on_lit_high_change(val):
    global lit_h
    lit_h = val
    maskextract()

def on_sat_high_chnage(val):
    global sat_h
    sat_h = val
    maskextract()


cv2.namedWindow('lane_1')
cv2.namedWindow('lane_2')

cv2.createTrackbar('hue_l_l', 'lane_1', hue_l_l, 255, on_hue_low_change)
cv2.createTrackbar('hue_h_l', 'lane_1', hue_h_l, 255, on_hue_high_low_change)
cv2.createTrackbar('lit_l', 'lane_1', lit_l, 255, on_lit_low_change)
cv2.createTrackbar('sat_l', 'lane_1', sat_l, 255, on_sat_low_chnage)

cv2.createTrackbar('hue_l_h', 'lane_2', hue_l_h, 255, on_hue_low_high_change)
cv2.createTrackbar('hue_h_h', 'lane_2', hue_h_h, 255, on_hue_high_change)
cv2.createTrackbar('lit_h', 'lane_2', lit_h, 255, on_lit_high_change)
cv2.createTrackbar('sat_h', 'lane_2', sat_h, 255, on_sat_high_chnage)



def segment_lanes(frame, min_area):
    # step 1: change color space to HLS
    hls_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)

    # segmentation lane 
    lane_1 = color_segment(hls_image, (hue_l_l,lit_l,sat_l),(255,255,255))
    lane_2 = color_segment(hls_image, (hue_l_l,lit_l,sat_l),(hue_h_h,lit_h,sat_h))
    
    cv2.imshow("lane_1", lane_1)
    cv2.imshow("lane_2", lane_2)

    cv2.waitKey(1)
