from PIL import Image
from processing.basic_morphological import grayscale_dilation, grayscale_erosion
from processing.image_opt import image_absdiff, gray_image_max, gray_image_min, image_equal
from processing.util import MorphReconstructOptType, MorphGradientOptType
import numpy as np


def morph_grayscale_edge_detection(img):
    se = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    center = (1, 1)
    img_d = grayscale_dilation(img, se, center)
    img_e = grayscale_erosion(img, se, center)
    return image_absdiff(img_d, img_e)


# img_marker 标记图像 -- img_mask 模板图像
def morph_reconstruct(img_marker, img_mask, se, center, opt_type):
    if (opt_type == MorphReconstructOptType.INVALID):
        raise TypeError('invalid reconstruct opt')

    img_res = None
    switcher = {
        MorphReconstructOptType.DILATION: (grayscale_dilation, gray_image_min),
        MorphReconstructOptType.EROSION: (grayscale_erosion, gray_image_max)
    }

    func = switcher.get(opt_type)
    img_tmp = img_marker
    while True:
        img_res = img_tmp
        img_tmp = (func[1])((func[0])(img_tmp, se, center), img_mask)
        if image_equal(img_tmp, img_res):
            break
    return img_res


def morph_gradient(img, se, center, opt_type):
    if (opt_type == MorphGradientOptType.INVALID):
        raise TypeError('invalid gradient opt')

    if (opt_type == MorphGradientOptType.INTERNAL):
        img_l = img
    else:
        img_l = grayscale_dilation(img, se, center)

    if (opt_type == MorphGradientOptType.EXTERNAL):
        img_r = img
    else:
        img_r = grayscale_erosion(img, se, center)

    return image_absdiff(img_l, img_r)
