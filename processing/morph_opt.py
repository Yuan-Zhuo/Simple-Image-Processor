from PIL import Image
from processing.basic_morphological import geodesic_dilation, geodesic_erosion, binary_dilation, binary_erosion, grayscale_dilation, grayscale_erosion, binary_geodesic_dilation, binary_geodesic_erosion
from processing.image_opt import image_absdiff, grayscale_image_max, grayscale_image_min, image_equal, image_divide
from interface.opt_type import MorphBinaryReconstructOptType, MorphEdgeDetectionOptType, MorphGradientOptType, MorphGrayscaleReconstructOptType
import numpy as np


# Types: standard, internal, external
def morph_edge_detection(se, center, opt_type, img):
    if (opt_type == MorphGradientOptType.INVALID):
        raise TypeError('invalid edge detection opt')

    if (opt_type == MorphGradientOptType.INTERNAL):
        img_l = img
    else:
        img_l = binary_dilation(img, se, center)

    if (opt_type == MorphGradientOptType.EXTERNAL):
        img_r = img
    else:
        img_r = binary_erosion(img, se, center)

    return image_absdiff(img_l, img_r)


# Types: conditional dilation, conditioanl erosion
def morph_binary_reconstruct(se, center, opt_type, img_f, img_g):
    if (opt_type == MorphBinaryReconstructOptType.INVALID):
        raise TypeError('invalid reconstruct opt')

    img_res = None
    reconstruct_switcher = {
        MorphBinaryReconstructOptType.CONDITIONAL_DILATION:
        binary_geodesic_dilation,
        MorphBinaryReconstructOptType.CONDITIONAL_EROSION:
        binary_geodesic_erosion
    }

    func = reconstruct_switcher.get(opt_type)
    img_res = None
    img_tmp = img_f
    while True:
        img_tmp = func(img_tmp, img_g, se, center)
        if image_equal(img_tmp, img_res):
            break
        img_res = img_tmp
    return img_res


# Types: geodesic dilation, geodesic erosion, open, close
def morph_grayscale_reconstruct(se, center, opt_type, img_f, img_g=None):
    if (opt_type == MorphGrayscaleReconstructOptType.INVALID):
        raise TypeError('invalid reconstruct opt')

    if (img_g == None):
        if (opt_type == MorphGrayscaleReconstructOptType.OPEN):
            img_g = grayscale_erosion(img_f, se, center)
            opt_type = MorphGrayscaleReconstructOptType.GEODESIC_DILATION
        elif (opt_type == MorphGrayscaleReconstructOptType.CLOSE):
            img_g = grayscale_dilation(img_f, se, center)
            opt_type = MorphGrayscaleReconstructOptType.GEODESIC_EROSION
        else:
            raise TypeError('invalid arguments for reconstruct')

    img_res = None
    reconstruct_switcher = {
        MorphGrayscaleReconstructOptType.GEODESIC_DILATION: geodesic_dilation,
        MorphGrayscaleReconstructOptType.GEODESIC_EROSION: geodesic_erosion
    }

    func = reconstruct_switcher.get(opt_type)
    img_res = None
    img_tmp = img_f
    while True:
        img_tmp = func(img_tmp, img_g, se, center)
        if image_equal(img_tmp, img_res):
            break
        img_res = img_tmp
    return img_res


# Types: standard, internal, external
def morph_gradient(se, center, opt_type, img):
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

    return image_divide(image_absdiff(img_l, img_r), 2)
