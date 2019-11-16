from PIL import Image
from processing.basic_convolution import basic_convolution
from processing.image_merge import image_merge
import numpy as np


def basic_operator(img, kernel_x, kernel_y):
    img_x = basic_convolution(img, kernel_x)
    img_y = basic_convolution(img, kernel_y)
    return image_merge(img_x, img_y)


def sobel_operator(img):
    kernel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    kernel_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
    return basic_operator(img, kernel_x, kernel_y)


def prewitt_operator(img):
    kernel_x = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
    kernel_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
    return basic_operator(img, kernel_x, kernel_y)


def roberts_operator(img):
    kernel_x = np.array([[0, 0, 0], [0, -1, 0], [0, 0, 1]])
    kernel_y = np.array([[0, 0, 0], [0, 0, 1], [0, -1, 0]])
    return basic_operator(img, kernel_x, kernel_y)
