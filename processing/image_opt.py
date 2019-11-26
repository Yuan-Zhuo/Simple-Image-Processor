import numpy as np
from PIL import Image
from processing.util import parse_image, get_value, ImageType
import math


def image_comp(img_x, img_y):
    try:
        img_x_arr, img_x_type = parse_image(img_x)
        img_y_arr, img_y_type = parse_image(img_y)
        assert ((img_x_type != ImageType.INVALID))
        assert ((img_y_type != ImageType.INVALID))
    except:
        raise TypeError('two images invalid')
    else:
        return img_x_arr, img_x_type, img_y_arr, img_y_type


def image_merge(img_x, img_y):
    img_x_arr, img_x_type, img_y_arr, _ = image_comp(img_x, img_y)

    if ((img_x_arr.shape != img_y_arr.shape)):
        raise TypeError('merge images type error')

    img_shape = img_x_arr.shape
    img_type = img_x_type

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
    img_x_arr, _, img_y_arr, _ = image_comp(img_x, img_y)

    if ((img_x_arr.shape != img_y_arr.shape)):
        raise TypeError('absdiff images type error')

    img_shape = img_x_arr.shape

    res_arr = np.zeros(img_shape, dtype=np.uint8)
    for x in range(img_shape[0]):
        for y in range(img_shape[1]):
            tmp = np.absolute(img_x_arr[x][y] - img_y_arr[x][y])
            res_arr[x][y] = tmp
    return Image.fromarray(res_arr)


def image_divide(img, n):
    img_arr, img_type = parse_image(img)
    if ((img_type == ImageType.INVALID)):
        raise TypeError('image invalid')

    res_arr = np.floor_divide(img_arr, n)
    return Image.fromarray(res_arr.astype(np.uint8))


def image_equal(img_x, img_y):
    img_x_arr, img_x_type, img_y_arr, img_y_type = image_comp(img_x, img_y)

    if ((img_x_type != img_y_type)):
        raise TypeError('compare images type error')

    img_shape = np.minimum(img_x_arr.shape, img_y_arr.shape)
    img_x_arr = img_x_arr[:img_shape[0], :img_shape[1]]
    img_y_arr = img_y_arr[:img_shape[0], :img_shape[1]]
    return np.array_equal(img_x_arr, img_y_arr)


def image_binary(img):
    img_arr, img_type = parse_image(img)
    if ((img_type != ImageType.GRAYSCALE)):
        raise TypeError('image invalid')

    img_shape = img_arr.shape
    res_arr = np.zeros(img_shape, dtype=np.uint8)
    for x in range(img_shape[0]):
        for y in range(img_shape[1]):
            res_arr[x][y] = 0 if img_arr[x][y] < 128 else 1
    return res_arr


def grayscale_image_min(img_x, img_y):
    img_x_arr, img_x_type, img_y_arr, img_y_type = image_comp(img_x, img_y)

    if ((img_x_type != ImageType.GRAYSCALE) |
        (img_y_type != ImageType.GRAYSCALE)):
        raise TypeError('grayscale min images type error')

    img_shape = np.minimum(img_x_arr.shape, img_y_arr.shape)
    img_x_arr = img_x_arr[:img_shape[0], :img_shape[1]]
    img_y_arr = img_y_arr[:img_shape[0], :img_shape[1]]
    res_arr = np.minimum(img_x_arr, img_y_arr)
    return Image.fromarray(res_arr.astype(np.uint8))


def grayscale_image_max(img_x, img_y):
    img_x_arr, img_x_type, img_y_arr, img_y_type = image_comp(img_x, img_y)

    if ((img_x_type != ImageType.GRAYSCALE) |
        (img_y_type != ImageType.GRAYSCALE)):
        raise TypeError('grayscale max images type error')

    img_shape = np.minimum(img_x_arr.shape, img_y_arr.shape)
    img_x_arr = img_x_arr[:img_shape[0], :img_shape[1]]
    img_y_arr = img_y_arr[:img_shape[0], :img_shape[1]]
    res_arr = np.maximum(img_x_arr, img_y_arr)
    return Image.fromarray(res_arr.astype(np.uint8))
