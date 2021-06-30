import cv2
from matplotlib import pyplot as plt

file_directory = "D:/#2021_CAPSTONE/_DataSet/temp_pycahrm"
FIG_SIZE = (2.6,2)

import os

# g까지 했음 --> temp_pycahrm 폴더 참조

for (dirpath, dirnames, filenames) in os.walk(file_directory):
    for filename in filenames:
        img = cv2.imread(dirpath + "/" + filename)

        dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

        plt.figure(figsize=FIG_SIZE)
        plt.axis('off'), plt.xticks([]), plt.yticks([])
        plt.tight_layout()
        plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)

        plt.imshow(dst, cmap=plt.cm.rainbow, interpolation='bicubic')
        plt.savefig('D:/#2021_CAPSTONE/_DataSet/removenoise_pycharm/' + 'unnoised' + filename,
                    bbox_inches=None, pad_inches=0)
