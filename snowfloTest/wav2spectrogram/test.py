# any test

import matplotlib.pyplot as plt
import librosa.display
import librosa
import numpy as np

path = "D:/#2021_CAPSTONE/_DataSet/sound_data/snowflo/how_working_path/how_working_path (1).wav"
sample_rate = 44100

x, sampling_rate = librosa.load(path, sample_rate)
S = librosa.feature.melspectrogram(x, sr=sample_rate, n_mels=128)  # returns : 128
P = librosa.power_to_db(S, ref=np.max)  # log_S = librosa.power_to_db(S, ref=np.max)
mfcc = librosa.feature.mfcc(S=P, n_mfcc=20)  # return : 20
delta2_mfcc = librosa.feature.delta(mfcc, order=2)

plt.figure(figsize=(12, 4))
librosa.display.specshow(delta2_mfcc)  # 유무 차이, 있으면 --> 색깔 바뀜, 없으면 --> 안 바뀜
plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
plt.margins(0, 0)
plt.gca().set_axis_off()
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())
plt.tight_layout()
plt.imshow(delta2_mfcc)
plt.savefig('D:/#2021_CAPSTONE/_DataSet/sound_test_data/spec/delta2_mfcc/' + "test" + '.png',
            bbox_inches='tight', pad_inches=0)

import cv2
img = cv2.imread('D:/#2021_CAPSTONE/_DataSet/sound_test_data/spec/delta2_mfcc/test.png')

print(img)