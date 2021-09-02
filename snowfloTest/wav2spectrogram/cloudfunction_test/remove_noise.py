import cv2
from matplotlib import pyplot as plt

file_directory = "E:/##kpu_capstone_voice_data/#spec_data/youtube_dongbinna_u"
FIG_SIZE = (2.6,2)

import os

for (dirpath, dirnames, filenames) in os.walk(file_directory):
    for filename in filenames:
        print("dp: ", dirpath)
        print("fn: ", filename)
        print("pt: ", dirpath + "/" + filename)

        img = cv2.imread(dirpath + "/" + filename)

        dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

        plt.figure(figsize=FIG_SIZE)
        plt.axis('off'), plt.xticks([]), plt.yticks([])
        plt.tight_layout()
        plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)

        plt.imshow(dst, cmap=plt.cm.rainbow, interpolation='bicubic')
        # plt.savefig('E:/##kpu_capstone_voice_data/#spec_data_remove_noise/call_sangho/' + 'unnoised' + filename,
        #             bbox_inches=None, pad_inches=0)
        plt.savefig('E:/##kpu_capstone_voice_data/#spec_data_remove_noise/youtube_dongbinna_u/' + 'unnoised' + filename,
                    bbox_inches=None, pad_inches=0)