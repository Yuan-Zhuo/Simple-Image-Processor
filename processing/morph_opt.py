from PIL import Image
from processing.basic_morphological import grayscale_dilation, grayscale_erosion
from processing.image_opt import image_absdiff, gray_image_max, gray_image_min, image_equal
from processing.util import MorphOptType
import numpy as np


def morph_grayscale_edge_detection(img):
    se = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    center = (1, 1)
    img_d = grayscale_dilation(img, se, center)
    img_e = grayscale_erosion(img, se, center)
    return image_absdiff(img_d, img_e)


def morph_reconstruction(img, img_ref, se, center, opt_type):
    img_res = None
    switcher = {
        MorphOptType.DILATION: (grayscale_dilation, gray_image_min),
        MorphOptType.EROSION: (grayscale_erosion, gray_image_max)
    }

    func = switcher.get(opt_type)
    img_tmp = img_ref
    while True:
        img_res = img_tmp
        img_tmp = (func[1])((func[0])(img_tmp, se, center), img)
        if image_equal(img_tmp, img_res):
            break
    return img_res
