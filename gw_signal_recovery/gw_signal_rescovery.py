from os.path import isfile, join
from os import listdir
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from PIL import ImageFilter

import cv2   # if not found,try pip install opencv-python
import os

print("Change the current working directory to path:", os.path.dirname(__file__))
os.chdir(os.path.dirname(__file__))

onlyfiles = [f for f in listdir("./input") if isfile(join("./input", f))]

print(onlyfiles)
'''
3YljKfLQ.png
4B2Dcn2o.png
8dJosPug.png
8uS7qspI.png
buY6cs6U.png
Clqh9OD0.png
DH1QeME4.png
jyicdNJM.png
KsJUDLN0.png
m-GNRpbw.png
TO5-rs9o.png
u4J8dZ7o.png
VvCGeC4o.png
'''

# 將波形以外的背景填成白色


def floodfill_image(image, power):
    copyImage = image.copy()  # 複製原圖像
    h, w = image.shape[:2]  # 讀取圖像的寬和高
    mask = np.zeros([h+2, w+2], np.uint8)  # 新建圖像矩陣 +2是官方函數要求

    cv2.floodFill(copyImage, mask, (517, 260), (255, 255, 255), (power,
                                                                 power, power), (power, power, power), cv2.FLOODFILL_FIXED_RANGE)
    #cv.imshow("floodFill", copyImage)
    return copyImage

# 將canny最後結果填上白色


def result_image(image):
    copyImage = image.copy()
    rows, cols = copyImage.shape
    tmp_top = 0
    tmp_down = 0
    tmp_col = 0
    # 圖片大小
    # print(str(rows),",",str(cols))
    wait_draw = False
    for i in range(cols):
        top = 0
        down = rows
        for j in range(rows):
            k = copyImage[j, i]
            if(k > 100):
                if (j > top):
                    top = j
                if (j < down):
                    down = j
        if(down - top > rows/2):
            wait_draw = True
            #cv2.line(copyImage, (i, tmp_top),(i, tmp_down), (255, 255, 255), 1)
            #print("top =" + str(tmp_top) +",down ="+str(tmp_down))

        else:
            if(wait_draw):
                wait_draw = False
                '''
                cv2.line(copyImage, (tmp_col,tmp_down ),
                     (i, down), (255, 255, 255), 1)
                cv2.line(copyImage, (tmp_col,tmp_top ),
                     (i, top), (255, 255, 255), 1)
                '''
                cv2.line(copyImage, (tmp_col, int((tmp_down + tmp_top)/2)),
                         (i, int((top + down)/2)), (255, 255, 255), 1)

            cv2.line(copyImage, (i, top), (i, down), (255, 255, 255), 1)
            tmp_top = top
            tmp_down = down
            tmp_col = i

    return copyImage


def cv2_show_img(title, img, is_save):
    cv2.imshow(title, img)
    if(is_save):
        cv2.imwrite("output\\" + title, img)


index = 0
# === main ===
for file in onlyfiles:
    src = cv2.imread("input\\" + file)
    H, W, channels = src.shape

    # 裁切區域的 x 與 y 座標（左上角）
    x = 10
    y = 90

    # （右下角）
    x1 = W-30
    y1 = 545
    crop_img = src[y:y1, x:x1]
    cv2_show_img(str(index) + "_1_original_" + file, src, True)

    #cv2.imshow("crop_img", crop_img)

    # flood fill 邊緣偵測
    ff_img = floodfill_image(crop_img, 35)
    #cv2.imshow("floodfill", ff_img)

    # blur 模糊
    blur = cv2.blur(ff_img, (5, 5))  # 中型圖片
    #cv2.imshow("blur", blur)

    # kernel 銳化
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)
    kernel_img = cv2.filter2D(blur, -1, kernel=kernel)
    #cv2.imshow("kernel", kernel_img)

    # canny 邊緣偵測
    canny = cv2.Canny(kernel_img, 100, 200)
    cv2_show_img(str(index) + "_2_canny_" + file, canny, True)

    # sobel 邊緣偵測(未使用)
    '''
    Gx = cv2.Sobel(blur,cv2cv.CV_16S,1,0)
    Gy = cv2.Sobel(blur,cv2.CV_16S,0,1)

    absX = cv2.convertScaleAbs(Gx)
    absY = cv2.convertScaleAbs(Gy)
    
    dst = cv2.addWeighted(absX,0.5,absY,0.5,0)
    
    cv2.imshow("absX", absX)
    cv2.imshow("absY", absY)
    cv2.imshow("sobel", dst)
    '''

    result_img = result_image(canny)
    cv2_show_img(str(index) + "_3_result_" + file, result_img, True)

    # 按任一鍵繼續下一張
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    index += 1
