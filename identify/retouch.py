import cv2
import numpy as np


class Retouch:
    @staticmethod
    def remove_bg(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        th, threshed = cv2.threshold(gray, 127, 255,
                                     cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

        _cnts = cv2.findContours(threshed, cv2.RETR_TREE,
                                 cv2.CHAIN_APPROX_SIMPLE)[-2]
        cnts = sorted(_cnts, key=cv2.contourArea)
        for cnt in cnts:
            if cv2.contourArea(cnt) > 1000:
                break

        mask = np.zeros(img.shape[:2], np.uint8)
        cv2.drawContours(mask, [cnt], -1, 255, -1)
        return cv2.bitwise_and(img, img, mask=mask)

    @staticmethod
    def crop_edge(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)
        cnt = contours[0]
        x, y, w, h = cv2.boundingRect(cnt)

        return img[y:y + h, x:x + w]

    @staticmethod
    def clear_bg(img):
        arr = np.array(img)
        x, y, z = arr.shape
        for ix in range(x):
            for iy in range(y):
                if np.array_equal(arr[ix, iy], [0, 0, 0]):
                    arr[ix, iy] = [255, 255, 255]
        return arr

    @staticmethod
    def retouch(img):
        img_after = Retouch.remove_bg(img)
        cv2.imwrite('retouch.png', img_after)
        img_after = Retouch.crop_edge(img_after)
        img_after = Retouch.clear_bg(img_after)

        return img_after
