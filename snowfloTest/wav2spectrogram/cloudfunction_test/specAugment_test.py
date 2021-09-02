import random
import cv2
from matplotlib import pyplot as plt


# https://jvvp.tistory.com/1018
# 결과 저장 폴더 생성
def random_image(path, pfilename):
    for i in range(NUM_SAMPLES):
        # 랜덤 이미지를 생성합니다.
        img1 = cv2.imread(
            path + "/" + pfilename)
        img2 = cv2.imread("E:/##kpu_capstone_voice_data/#spec_data_augment/call_sangho/test0.png")

## 영역 지정
        # 좌표
        col = random.randrange(0, 200)      # 0 ~ 200
        row = random.randrange(0, 260)      # 0 ~ 260

        # 넓이
        col_r = random.randrange(0, 50)
        row_r = random.randrange(0, 50)

        # 체크
        print("row: {} col: {} row_r: {} col_r: {}".format(row, col, row_r, col_r))

        #
        cp_img = img1[0:200,row:row + row_r]
        cp_img.fill(255)

        cp_img = img1[col:col+col_r,0:260]
        cp_img.fill(255)

        plt.figure(figsize=FIG_SIZE)
        plt.axis('off'), plt.xticks([]), plt.yticks([])
        plt.tight_layout()
        plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)

        plt.imshow(img1, cmap=plt.cm.rainbow, interpolation='bicubic')
        plt.savefig('E:/##kpu_capstone_voice_data/#spec_data_augment/call_sangho/'+pfilename+str(i)+".png",
                    bbox_inches=None, pad_inches=0)

import os

if __name__ == '__main__':
    NUM_SAMPLES = 10            ## 이미지 파일 개수를 정의
    FIG_SIZE = (2.6, 2)

    # 랜덤
    random.seed()

    file_directory = "E:/##kpu_capstone_voice_data/#spec_data_remove_noise/call_sangho/"     ## 폴더명 변경

    for (dirpath, dirnames, filenames) in os.walk(file_directory):
        for filename in filenames:
            random_image(file_directory, filename)