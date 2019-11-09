import numpy as np
from PIL import Image
from enum import IntEnum


class ImageType(IntEnum):
    INVALID = 0
    GRAYSCALE = 1
    COLOR = 2


def parse_kernel(kernel):
    try:
        row, col = kernel.shape
        assert ((row == col) & (row % 2 == 1))
    except:
        return 0
    else:
        return row // 2


def parse_image(img):
    try:
        img_arr = np.array(img)
        if (len(img_arr.shape) == 2):
            img_type = ImageType.GRAYSCALE
        elif (len(img_arr.shape) == 3):
            img_type = ImageType.COLOR
        else:
            assert 0
    except:
        return np.zeros(0, dtype="int32"), ImageType.INVALID
    else:
        return img_arr.astype(np.int32), img_type


def get_value(img_arr, img_shape, point):
    if (((point[0] >= 0) & (point[0] < img_shape[0])) &
        ((point[1] >= 0) & (point[1] < img_shape[1]))):
        return np.int32(img_arr[point])
    else:
        return np.zeros(img_arr[0][0].shape, dtype="int32")
