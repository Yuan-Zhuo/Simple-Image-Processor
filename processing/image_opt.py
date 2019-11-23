import numpy as np
from PIL import Image
from processing.util import parse_image, get_value, ImageType
import math


def image_merge(img_x, img_y):
    img_x_arr, img_x_type = parse_image(img_x)
    img_y_arr, img_y_type = parse_image(img_y)
    if ((img_x_type == ImageType.INVALID) | (img_y_type == ImageType.INVALID)):
        raise TypeError('invalid image')

    img_shape = img_x_arr.shape
    img_type = img_x_type
    if ((img_shape != img_y_arr.shape) | (img_type != img_y_type)):
        raise TypeError('not equal image')

    res_arr = np.zeros(img_shape, dtype=np.uint8)
    for x in range(img_shape[0]):
        for y in range(img_shape[1]):
            tmp = img_x_arr[x][y] + img_y_arr[x][y]
            if (img_type == ImageType.GRAYSCALE):
                res_arr[x][y] = max(min(round(tmp), 255), 0)
            else:
                for k in range(3):
                    res_arr[x][y][k] = max(min(round(tmp[k]), 255), 0)
    return Image.fromarray(res_arr)


def image_absdiff(img_x, img_y):
    img_x_arr, img_x_type = parse_image(img_x)
    img_y_arr, img_y_type = parse_image(img_y)
    if ((img_x_type == ImageType.INVALID) | (img_y_type == ImageType.INVALID)):
        raise TypeError('invalid image')

    img_shape = img_x_arr.shape
    img_type = img_x_type
    if ((img_shape != img_y_arr.shape) | (img_type != img_y_type)):
        raise TypeError('not equal image')

    res_arr = np.zeros(img_shape, dtype=np.uint8)
    for x in range(img_shape[0]):
        for y in range(img_shape[1]):
            tmp = np.absolute(img_x_arr[x][y] - img_y_arr[x][y])
            res_arr[x][y] = tmp
    return Image.fromarray(res_arr)


def image_equal(img_x, img_y):
    img_x_arr, img_x_type = parse_image(img_x)
    img_y_arr, img_y_type = parse_image(img_y)
    if ((img_x_type == ImageType.INVALID) | (img_y_type == ImageType.INVALID)):
        raise TypeError('invalid image')

    img_type = img_x_type
    if ((img_type != img_y_type)):
        raise TypeError('different type image')

    img_shape = np.minimum(img_x_arr.shape, img_y_arr.shape)
    img_x_arr = img_x_arr[:img_shape[0], :img_shape[1]]
    img_y_arr = img_y_arr[:img_shape[0], :img_shape[1]]
    return np.array_equal(img_x_arr, img_y_arr)


def gray_image_min(img_x, img_y):
    img_x_arr, img_x_type = parse_image(img_x)
    img_y_arr, img_y_type = parse_image(img_y)
    if ((img_x_type != ImageType.GRAYSCALE) |
        (img_y_type != ImageType.GRAYSCALE)):
        raise TypeError('invalid image')

    img_type = img_x_type
    if ((img_type != img_y_type)):
        raise TypeError('different type image')

    img_shape = np.minimum(img_x_arr.shape, img_y_arr.shape)
    img_x_arr = img_x_arr[:img_shape[0], :img_shape[1]]
    img_y_arr = img_y_arr[:img_shape[0], :img_shape[1]]
    res_arr = np.minimum(img_x_arr, img_y_arr)
    return Image.fromarray(res_arr.astype(np.uint8))


def gray_image_max(img_x, img_y):
    img_x_arr, img_x_type = parse_image(img_x)
    img_y_arr, img_y_type = parse_image(img_y)
    if ((img_x_type != ImageType.GRAYSCALE) |
        (img_y_type != ImageType.GRAYSCALE)):
        raise TypeError('grayscale image expected')

    img_type = img_x_type
    if ((img_type != img_y_type)):
        raise TypeError('different type image')

    img_shape = np.minimum(img_x_arr.shape, img_y_arr.shape)
    img_x_arr = img_x_arr[:img_shape[0], :img_shape[1]]
    img_y_arr = img_y_arr[:img_shape[0], :img_shape[1]]
    res_arr = np.maximum(img_x_arr, img_y_arr)
    return Image.fromarray(res_arr.astype(np.uint8))
