import cv2
from matplotlib import pyplot as plt

FIG_SIZE = (2.6, 2)

img = cv2.imread("E:/##kpu_capstone_voice_data/#spec_data/call_sangho/call_sangho (1).png")  # 가상환경에 저장한 것 불러옴

dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

plt.figure(figsize=FIG_SIZE)
plt.axis('off'), plt.xticks([]), plt.yticks([])
plt.tight_layout()
plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)

plt.imshow(dst, cmap=plt.cm.rainbow, interpolation='bicubic')
plt.savefig('E:/##kpu_capstone_voice_data/#spec_data_remove_noise/call_sangho/denoise.png', bbox_inches=None, pad_inches=0)  # /tmp/denoise.png로 저장