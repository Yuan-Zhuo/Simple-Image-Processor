from dhash import DHash
from retouch import Retouch
import os
from PIL import Image
from enum import IntEnum
import cv2


class BottleCapType(IntEnum):
    INVALID = 0
    POS = 1
    NEG = 2
    STANDING = 3


class Identify:
    def __init__(self):
        self.__init_config()
        self.__init_load()

    def __init_config(self):
        # path config
        self.path_list = [
            '../img/standard/positive', '../img/standard/negative',
            '../img/standard/standing'
        ]
        self.standard_img_list = [[], [], []]
        self.switcher = {
            0: BottleCapType.POS,
            1: BottleCapType.NEG,
            2: BottleCapType.STANDING,
            3: BottleCapType.INVALID
        }
        self.threshold = 0.9

    def __init_load(self):
        owd = os.getcwd()
        for idx, path in enumerate(self.path_list):
            filename_list = os.listdir(path)
            os.chdir(path)
            for filename in filename_list:
                # self.standard_img_list[idx].append(Image.open(filename))
                self.standard_img_list[idx].append(cv2.imread(filename))
            os.chdir(owd)

    def __diff(self, img_l, img_r):
        distance = DHash.hamming_distance(img_l, img_r)
        return 1 - distance * 1. / (32 * 32 / 4)

    def __compare(self, img_test, img_list):
        score = 0
        for img in img_list:
            score += self.__diff(img_test, img)
        return score / len(img_list)

    def judge(self, img_test):
        avg_score = [0, 0, 0]
        for i in range(3):
            avg_score[i] = self.__compare(Retouch.retouch(img_test),
                                          self.standard_img_list[i])
            print(avg_score[i])
        max_score = max(avg_score)
        if (max_score > self.threshold):
            idx = avg_score.index(max_score)
        else:
            idx = 3
        return self.switcher[idx]

    def judge_list(self, img_test_list):
        type_list = []
        for img_test in img_test_list:
            type_list.append(self.judge(img_test))
        return type_list


if __name__ == "__main__":
    idt = Identify()
    # img_test_list = []
    # img_test_list.append(Image.open('img/identify/0_neg.jpg'))
    # img_test_list.append(Image.open('img/identify/1_pos.jpg'))
    # img_test_list.append(Image.open('img/identify/2_neg.jpg'))
    # img_test_list.append(Image.open('img/identify/3_standing.jpg'))
    # print(idt.judge_list(img_test_list))
    # print(idt.judge(
    #     Image.open('img/standard/standing/tiny_blue_standing.png')))
    print(idt.judge(cv2.imread('../img/identify/3_standing.jpg')))
