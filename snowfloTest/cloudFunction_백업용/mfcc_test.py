#  mfcc_test : mfcc --> mel spectrum + cepstrul analysis

import matplotlib.pyplot as plt
import librosa.display
import librosa
import numpy as np
import os

path = "D:/#2021_CAPSTONE/_DataSet/sound_test_data"
sample_rate = 44100
formats_to_convert = ['.wav']

for (dirpath, dirnames, filenames) in os.walk(path):  # 상위 폴더
    for filename in filenames:
        print('dirpath: ', dirpath)
        print('dirnames : ', dirnames)
        print('filenames: ', filename)

        if filename.endswith(tuple(formats_to_convert)):
            filepath = os.path.join(dirpath, filename)
            # x = librosa.load(filepath, sample_rate)[0]
            x, sampling_rate = librosa.load(filepath, sample_rate)
            S = librosa.feature.melspectrogram(x, sr=sample_rate, n_mels=128)  # returns : 128

            # plt.title('melspectrogram')
            # plt.imshow(S)
            # plt.savefig('D:/#2021_CAPSTONE/_DataSet/sound_test_data/spec/mel/' + filename.replace(".wav","") + '.png', bbox_inches=None, pad_inches=0)

            P = librosa.power_to_db(S, ref=np.max)  # log_S = librosa.power_to_db(S, ref=np.max)
            # mel
            # plt.figure(figsize=(12, 4))
            # plt.axis('off'), plt.xticks([]), plt.yticks([])
            # plt.tight_layout()
            # plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)
            # librosa.display.specshow(P)

            # plt.title('power_to_db')
            # plt.imshow(P)
            # plt.savefig('D:/#2021_CAPSTONE/_DataSet/sound_test_data/spec/power_to_db/' + filename.replace(".wav","") + '.png', bbox_inches=None, pad_inches=0)

            print(S.shape)  # 모양이 계속 다르게 나옴

            mfcc = librosa.feature.mfcc(S=P, n_mfcc=20)  # return : 20

            # plt.title('mfcc')
            # figsize
            # plt.figure(figsize=(12, 4))
            # # tight
            # plt.tight_layout()
            # plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)
            # plt.margins(0, 0)
            # # gca() --> ???
            # plt.gca().set_axis_off()
            # plt.gca().xaxis.set_major_locator(plt.NullLocator())
            # plt.gca().yaxis.set_major_locator(plt.NullLocator())
            # plt.imshow(mfcc)
            # plt.savefig('D:/#2021_CAPSTONE/_DataSet/sound_test_data/spec/mfcc/' + filename.replace(".wav", "") + '.png',bbox_inches='tight', pad_inches=0)

            print(mfcc.shape)
            delta2_mfcc = librosa.feature.delta(mfcc, order=2)

            # plt.title('delta2_mfcc')
            plt.figure(figsize=(12, 4))
            librosa.display.specshow(delta2_mfcc)  # 유무 차이, 있으면 --> 색깔 바뀜, 없으면 --> 안 바뀜
            plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
            plt.margins(0, 0)
            plt.gca().set_axis_off()
            plt.gca().xaxis.set_major_locator(plt.NullLocator())
            plt.gca().yaxis.set_major_locator(plt.NullLocator())
            plt.tight_layout()
            plt.imshow(delta2_mfcc)
            plt.savefig('D:/#2021_CAPSTONE/_DataSet/sound_test_data/spec/delta2_mfcc/' + filename.replace(".wav", "") + '.png',bbox_inches='tight', pad_inches=0)

            # plt.imshow(log_S)  # imshow : 원하는 배열 넣고
            # plt.show()  # show :


