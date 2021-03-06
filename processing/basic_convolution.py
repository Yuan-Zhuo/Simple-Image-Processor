from processing.util import parse_kernel, parse_image, get_value, ImageType
import numpy as np
from PIL import Image


def basic_convolution(img, kernel):
    wd = parse_kernel(kernel)
    if (wd == 0):
        raise TypeError('invalid kernel')

    img_arr, img_type = parse_image(img)
    if (img_type == ImageType.INVALID):
        raise TypeError('invalid image')

    img_shape = img_arr.shape
    res_arr = np.zeros(img_shape, dtype=np.uint8)
    for x in range(img_shape[0]):
        for y in range(img_shape[1]):
            if (img_type == ImageType.GRAYSCALE):
                tmp = 0
                for i in range(-wd, wd + 1):
                    for j in range(-wd, wd + 1):
                        tmp += get_value(
                            img_arr, img_shape,
                            (x + i, y + j)) * kernel[wd + i][wd + j]
                res_arr[x][y] = max(min(round(tmp), 255), 0)
            else:
                tmp_rgb = np.zeros(3, dtype=np.float64)
                for i in range(-wd, wd + 1):
                    for j in range(-wd, wd + 1):
                        tmp_rgb += get_value(
                            img_arr, img_shape,
                            (x + i, y + j)) * kernel[wd + i][wd + j]
                for k in range(3):
                    res_arr[x][y][k] = max(min(round(tmp_rgb[k]), 255), 0)
    return Image.fromarray(res_arr)
