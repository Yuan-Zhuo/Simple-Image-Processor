from PIL import Image
from processing.basic_convolution import basic_convolution
from processing.image_merge import image_merge


def sobel_operator(img):
    sobel_horizontal_kernel = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    sobel_vertical_kernel = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
    img_x = basic_convolution(img, sobel_horizontal_kernel)
    img_y = basic_convolution(img, sobel_vertical_kernel)
    return image_merge(img_x, img_y)
