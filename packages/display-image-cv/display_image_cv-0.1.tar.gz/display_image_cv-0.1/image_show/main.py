import os
import numpy as np
import cv2 as cv

def display_image(image_path):
    image = cv.imread(image_path)
    cv.namedWindow("image",cv.WINDOW_NORMAL)
    cv.imshow("image",image)
    cv.waitKey(0)
    cv.destroyAllWindows()

display_image("C:\\Users\\saura\\Desktop\\images\\image2.jpg")