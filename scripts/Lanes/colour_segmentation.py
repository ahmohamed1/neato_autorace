import cv2


def color_segment(hls_img, lower_range, higherrange):
    

def segment_lanes(frame, min_area):
    # step 1: change color space to HLS
    hll_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
