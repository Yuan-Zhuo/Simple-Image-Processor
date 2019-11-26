# -*- coding: utf-8 -*-

from enum import IntEnum


class ConvolutionOptType(IntEnum):
    INVALID = 0
    MEAN_FILTER = 1
    MEDIAN_FILTER = 2
    GAUSSIAN_FILTER = 3
    SOBEL_OPERATOR = 4
    PREWITT_OPERATOR = 5
    ROBERTS_OPERATOR = 6
    CUSTOMIZE_OPERATOR = 7


class MorphEdgeDetectionOptType(IntEnum):
    INVALID = 0
    STANDRARD = 1
    INTERNAL = 2
    EXTERNAL = 3


class MorphBinaryReconstructOptType(IntEnum):
    INVALID = 0
    CONDITIONAL_DILATION = 1
    CONDITIONAL_EROSION = 2


class MorphGrayscaleReconstructOptType(IntEnum):
    INVALID = 0
    GEODESIC_DILATION = 1
    GEODESIC_EROSION = 2
    OPEN = 3
    CLOSE = 4


class MorphGradientOptType(IntEnum):
    INVALID = 0
    STANDRARD = 1
    INTERNAL = 2
    EXTERNAL = 3
