import cv2

from .a_colour_segmentation import segment_lanes
from .b_midlane_estimation import estimate_mid_lane
from ...config import config

from .c_cleaning import get_yellow_inner_Edge, extande_short_lane
from .d_data_extraction import fetch_info_and_dispaly



def detect_lane(img):
    img_cropped = img[config.CropHeight_resized:,:]

    # white_lane_mask, white_lane_edge, yellow_lane_mask, yellow_lane_edge, OuterLane_Points = segment_lanes(img, config.minArea_resized)
    Mid_edge_ROI,Mid_ROI_mask,Outer_edge_ROI,OuterLane_TwoSide,OuterLane_Points = segment_lanes(img_cropped,config.minArea_resized)
    estimated_midlane = estimate_mid_lane (Mid_edge_ROI, config.MaxDist_resized)

    outer_lane_on_side, outer_cnts_on_side, mid_cnts, offset_correction = get_yellow_inner_Edge (OuterLane_TwoSide, estimated_midlane, OuterLane_Points)
    extended_mid_lane, extended_outer_lane = extande_short_lane(estimated_midlane,mid_cnts,outer_cnts_on_side,outer_lane_on_side.copy())

    distance, curvature = fetch_info_and_dispaly(Mid_ROI_mask, extended_mid_lane, extended_outer_lane, img_cropped, offset_correction)

    cv2.imshow('Mid_edge_ROI', Mid_edge_ROI)
    cv2.imshow('Mid_ROI_mask', Mid_ROI_mask)
    cv2.imshow('Outer_edge_ROI', Outer_edge_ROI)
    cv2.imshow('OuterLane_TwoSide', OuterLane_TwoSide)
    cv2.imshow('estimated_midlane', estimated_midlane)
    cv2.imshow('extended_outer_lane', extended_outer_lane)
    cv2.imshow('outer_lane_on_side', outer_lane_on_side)
    cv2.imshow('extended_mid_lane', extended_mid_lane)
    cv2.waitKey(1)