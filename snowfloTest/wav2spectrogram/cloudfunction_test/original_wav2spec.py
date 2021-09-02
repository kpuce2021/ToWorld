import numpy as np
import librosa, librosa.display
import matplotlib.pyplot as plt

# dpi = 96
# x, y = 288, 192  # inch * dpi = pixel --> inch = pixel / dpi
# print(x , y)

FIG_SIZE = (2.6, 2)

# 저장된 wav 디렉토리, 후에 처리 과정 없으므로 /를 붙여줄 것
file_directory = "E:/##kpu_capstone_voice_data/youtube_dongbinna_u"  # 경로만 변경
formats_to_convert = ['.wav']

import os

# 변환
for (dirpath, dirnames, filenames) in os.walk(file_directory):  # 상위 폴더
    # https://codechacha.com/ko/python-walk-files/
    # os.walk : for 로 어떤 경로의 모든 하위 폴더와 파일을 탐색
    for filename in filenames:
        if filename.endswith(tuple(formats_to_convert)):  # tuple -> ('.wav')
            # .wav로 끝나면
            sig, sr = librosa.load(dirpath + "/" + filename, sr=22050)

            plt.figure(figsize=FIG_SIZE)  # 크기 조정
            plt.axis('off'), plt.xticks([]), plt.yticks([])  # 축끄기, 눈금끄기
            plt.tight_layout()
            plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)

            mel = librosa.feature.melspectrogram(sig, sr)  # mel spectrogram
            P = librosa.power_to_db(mel, ref=np.max)  # log_mel spectrogram
            librosa.display.specshow(P)

            filename = filename.split('.')

            plt.savefig('E:/##kpu_capstone_voice_data/#spec_data/youtube_dongbinna_u/' + filename[0] + '.png', bbox_inches=None,
                        pad_inches=0)