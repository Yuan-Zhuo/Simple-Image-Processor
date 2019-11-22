import numpy as np
from PIL import Image
from processing.util import parse_se, parse_image, ImageType, get_value, parse_binary_se
import math


# 二值膨胀-结构元 0-1
def binary_dilation(img, se, center):
    wd_tuple = parse_binary_se(se, center)
    if (wd_tuple == None):
        raise TypeError('invalid se')

    img_arr, img_type = parse_image(img)
    if (img_type == ImageType.INVALID):
        raise TypeError('invalid image')

    img_shape = img_arr.shape
    res_arr = np.zeros(img_shape, dtype=np.uint8)
    for x in range(img_shape[0]):
        for y in range(img_shape[1]):
            if (img_type == ImageType.COLOR):
                val_max_rgb = np.zeros(3, dtype=np.int32)
                for i in range(-wd_tuple[0], wd_tuple[1] + 1):
                    for j in range(-wd_tuple[2], wd_tuple[3] + 1):
                        if (se[i][j]):
                            val_point = get_value(img_arr, img_shape,
                                                  (x + i, y + j))
                            for k in range(3):
                                val_max_rgb[k] = max(val_max_rgb[k],
                                                     val_point[k])
                res_arr[x][y] = val_max_rgb
            else:
                val_max = 0
                for i in range(-wd_tuple[0], wd_tuple[1] + 1):
                    for j in range(-wd_tuple[2], wd_tuple[3] + 1):
                        if (se[i][j]):
                            val_max = max(
                                val_max,
                                get_value(img_arr, img_shape, (x + i, y + j)))
                res_arr[x][y] = val_max
    return Image.fromarray(res_arr)


# 灰度膨胀-结构元 0-255
def grayscale_dilation(img, se, center):
    wd_tuple = parse_se(se, center)
    if (wd_tuple == None):
        raise TypeError('invalid se')

    img_arr, img_type = parse_image(img)
    if (img_type == ImageType.INVALID):
        raise TypeError('invalid image')

    img_shape = img_arr.shape
    res_arr = np.zeros(img_shape, dtype=np.uint8)
    for x in range(img_shape[0]):
        for y in range(img_shape[1]):
            if (img_type == ImageType.COLOR):
                val_max_rgb = np.zeros(3, dtype=np.int32)
                for i in range(-wd_tuple[0], wd_tuple[1] + 1):
                    for j in range(-wd_tuple[2], wd_tuple[3] + 1):
                        val_point = get_value(img_arr, img_shape,
                                              (x + i, y + j))
                        for k in range(3):
                            val_max_rgb[k] = max(val_max_rgb[k],
                                                 val_point[k] + se[i][j])
                for k in range(3):
                    res_arr[x][y][k] = min(val_max_rgb[k], 255)
            else:
                val_max = 0
                for i in range(-wd_tuple[0], wd_tuple[1] + 1):
                    for j in range(-wd_tuple[2], wd_tuple[3] + 1):
                        val_max = max(
                            val_max,
                            get_value(img_arr, img_shape,
                                      (x + i, y + j)) + se[i][j])
                res_arr[x][y] = min(val_max, 255)
    return Image.fromarray(res_arr)


# 二值腐蚀-结构元 0-1
def binary_erosion(img, se, center):
    wd_tuple = parse_binary_se(se, center)
    if (wd_tuple == None):
        raise TypeError('invalid se')

    img_arr, img_type = parse_image(img)
    if (img_type == ImageType.INVALID):
        raise TypeError('invalid image')

    img_shape = img_arr.shape
    res_arr = np.zeros(img_shape, dtype=np.uint8)
    for x in range(img_shape[0]):
        for y in range(img_shape[1]):
            if (img_type == ImageType.COLOR):
                val_max_rgb = np.full(3, 255, dtype=np.int32)
                for i in range(-wd_tuple[0], wd_tuple[1] + 1):
                    for j in range(-wd_tuple[2], wd_tuple[3] + 1):
                        if (se[i][j]):
                            val_point = get_value(img_arr, img_shape,
                                                  (x + i, y + j))
                            for k in range(3):
                                val_max_rgb[k] = min(val_max_rgb[k],
                                                     val_point[k])
                res_arr[x][y] = val_max_rgb
            else:
                val_max = 255
                for i in range(-wd_tuple[0], wd_tuple[1] + 1):
                    for j in range(-wd_tuple[2], wd_tuple[3] + 1):
                        if (se[i][j]):
                            val_max = min(
                                val_max,
                                get_value(img_arr, img_shape, (x + i, y + j)))
                res_arr[x][y] = val_max
    return Image.fromarray(res_arr)


# 灰度腐蚀-结构元 0-255
def grayscale_erosion(img, se, center):
    wd_tuple = parse_se(se, center)
    if (wd_tuple == None):
        raise TypeError('invalid se')

    img_arr, img_type = parse_image(img)
    if (img_type == ImageType.INVALID):
        raise TypeError('invalid image')

    img_shape = img_arr.shape
    res_arr = np.zeros(img_shape, dtype=np.uint8)
    for x in range(img_shape[0]):
        for y in range(img_shape[1]):
            if (img_type == ImageType.COLOR):
                val_max_rgb = np.full(3, 255, dtype=np.int32)
                for i in range(-wd_tuple[0], wd_tuple[1] + 1):
                    for j in range(-wd_tuple[2], wd_tuple[3] + 1):
                        val_point = get_value(img_arr, img_shape,
                                              (x + i, y + j))
                        for k in range(3):
                            val_max_rgb[k] = min(val_max_rgb[k],
                                                 val_point[k] + se[i][j])
                for k in range(3):
                    res_arr[x][y][k] = max(val_max_rgb[k], 0)
            else:
                val_max = 0
                for i in range(-wd_tuple[0], wd_tuple[1] + 1):
                    for j in range(-wd_tuple[2], wd_tuple[3] + 1):
                        val_max = min(
                            val_max,
                            get_value(img_arr, img_shape,
                                      (x + i, y + j)) + se[i][j])
                res_arr[x][y] = max(val_max, 0)
    return Image.fromarray(res_arr)
