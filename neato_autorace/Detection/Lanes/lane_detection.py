from.colour_segmentation import segment_lanes
from ...config import config





def detect_lane(img):
    img_cropped = img[config.CropHeight_resizes:,:]

    segment_lanes = segment_lanes(img_cropped, config.minArea_resizes)
