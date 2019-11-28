import numpy as np
from PIL import Image
from enum import IntEnum


class ImageType(IntEnum):
    INVALID = 0
    GRAYSCALE = 1
    COLOR = 2


def parse_se(se, center):
    try:
        row, col = se.shape
        assert ((row > 0) & (col > 0))
        assert ((center[0] < row) & (center[0] >= 0))
        assert ((center[1] < col) & (center[1] >= 0))
    except:
        return None
    else:
        return (center[0], row - center[0] - 1, center[1], col - center[1] - 1)


def parse_binary_se(se, center):
    try:
        row, col = se.shape
        assert ((row > 0) & (col > 0))
        assert ((center[0] < row) & (center[0] >= 0))
        assert ((center[1] < col) & (center[1] >= 0))
        for a in np.nditer(se):
            assert ((a in (0, 1)))
    except:
        return None
    else:
        return (center[0], row - center[0] - 1, center[1], col - center[1] - 1)


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
        return None, ImageType.INVALID
    else:
        return img_arr.astype(np.uint8), img_type


def parse_binary_image(img):
    try:
        img_arr = np.array(img)
        assert ((len(img_arr.shape) == 2))
        img_type = ImageType.GRAYSCALE
        for a in np.nditer(img_arr):
            assert ((a in (0, 255)))
    except:
        return None, ImageType.INVALID
    else:
        return img_arr.astype(np.uint8), img_type


def get_value(img_arr, img_shape, point):
    if (((point[0] >= 0) & (point[0] < img_shape[0])) &
        ((point[1] >= 0) & (point[1] < img_shape[1]))):
        return np.int32(img_arr[point])
    else:
        return np.zeros(img_arr[0][0].shape, dtype=np.int32)


# Gaussian function
def gau(x, y, sigma):
    return 1 / (2 * np.pi * (sigma)**2) * np.exp(-(x**2 + y**2) / (2 *
                                                                   (sigma)**2))


def gaussian_kernel(size, sigma):
    wd = size // 2
    M = np.zeros((size, size), dtype=np.float64)
    s = 0
    for i in range(-wd, wd + 1):
        for j in range(-wd, wd + 1):
            M[i + wd, j + wd] = gau(i, j, sigma)
            s = s + M[i + wd, j + wd]

    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            M[i, j] /= s
    return M.astype(np.float64)
