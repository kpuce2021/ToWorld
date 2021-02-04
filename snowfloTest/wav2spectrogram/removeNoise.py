import numpy as np
import cv2
from matplotlib import pyplot as plt

file = "D:/DDataSet/spectrogram/"
folder_src = file+'tpng/fig'
folder_dst = file+'tnoise/ofig'
FIG_SIZE = (0.5,0.5)

for i in range(1,161):
    img = cv2.imread(folder_src+str(i)+'.png')

    dst = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)
    '''
    src
    dst
    h       : 필터 강도 결정, 높을수록 제거가 강함, 10이면 적당?
    hColor  : h와 동일, 칼라 이미지만 적용, 보통 h와 동일
    templateWindowSize  : 홀수값 7권장
    searchWindowSize    : 홀수값 21권장
    '''

    plt.figure(figsize=FIG_SIZE)
    plt.axis('off'), plt.xticks([]), plt.yticks([])
    plt.tight_layout()
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace =0, wspace=0)

    #plt.imshow(img, cmap=plt.cm.rainbow, interpolation='bicubic')
    #plt.savefig(file+"gnoise/noise"+str(i)+".png", dpi = 300, facecolor = 'none')
    plt.imshow(dst, cmap=plt.cm.rainbow, interpolation='bicubic')
    plt.savefig(file+"tnoise/tunnoise"+str(i)+".png", facecolor = 'none')

    print("remove noise "+str(i))

