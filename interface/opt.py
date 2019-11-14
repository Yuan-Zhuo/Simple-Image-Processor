# -*- coding: utf-8 -*-

from enum import IntEnum


class OptType(IntEnum):
    INVALID = 0
    MEAN_FILTER = 1
    MEDIAN_FILTER = 2
    GAUSSIAN_FILTER = 3
    SOBEL_OPERATOR = 4
    PREWITT_OPERATOR = 5
    ROBERTS_OPERATOR = 6
    CUSTOMIZE_OPERATOR = 7
