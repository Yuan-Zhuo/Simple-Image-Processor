from PIL import Image
from processing.basic_convolution import basic_convolution
from processing.image_merge import image_merge
from processing.util import parse_kernel, parse_image, get_value, ImageType, gaussian_kernel
import numpy as np


def mean_filter(img, size=3):
    kernel = np.full((size, size), 1 / (size * size), dtype=np.float64)
    return basic_convolution(img, kernel)


def median_filter(img, size=3):
    img_arr, img_type = parse_image(img)
    if (img_type == ImageType.INVALID):
        raise TypeError('invalid image')

    wd = size // 2
    img_shape = img_arr.shape
    res_arr = np.zeros(img_shape, dtype=np.uint8)
    for x in range(img_shape[0]):
        for y in range(img_shape[1]):
            tmp = []
            for i in range(-wd, wd + 1):
                for j in range(-wd, wd + 1):
                    tmp.append(get_value(img_arr, img_shape, (x + i, y + j)))
            if (img_type == ImageType.GRAYSCALE):
                res_arr[x][y] = max(min(round(np.median(tmp)), 255), 0)
            else:
                for k in range(3):
                    res_arr[x][y][k] = max(
                        min(round(np.median(np.array(tmp)[:, k])), 255), 0)
    return Image.fromarray(res_arr)


def gaussian_filter(img, size=3, sigma=1):
    kernel = gaussian_kernel(size, sigma)
    return basic_convolution(img, kernel)
