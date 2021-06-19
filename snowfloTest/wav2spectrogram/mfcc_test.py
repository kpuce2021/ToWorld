#  mfcc_test : mfcc --> mel spectrum + cepstrul analysis
import traceback

import matplotlib.pyplot as plt
import librosa.display
import librosa
import numpy as np
import os

path = "D:/#2021_CAPSTONE/_DataSet/sound_data_original (wav)"
sample_rate = 44100
formats_to_convert = ['.wav']
# failed to allocate bitmap error 의 원인 --> 조사 필요

# figsize = (1.24,0.8)

dpi = 128
x_inches = 16,384
y_inches = 5,120

for (dirpath, dirnames, filenames) in os.walk(path):  # 상위 폴더
    for filename in filenames:
        # print('dirpath: ', dirpath)
        # print('dirnames : ', dirnames)
        print('filenames: ', filename)

        if filename.endswith(tuple(formats_to_convert)):
            try:
                filepath = os.path.join(dirpath, filename)
                x, sampling_rate = librosa.load(filepath, sample_rate) # x = librosa.load(filepath, sample_rate)[0]

                # melspectrogram
                S = librosa.feature.melspectrogram(x, sr=sample_rate, n_mels=128)  # returns : 128, n_mels = 128 삭제

                plt.figure(figsize=(x_inches/dpi, y_inches/dpi), dpi=dpi, frameon=False)  # 12,4 --> 1.24, 0.8
                # librosa.display.specshow(S)  # 유무 차이, 있으면 --> 색깔 바뀜, 없으면 --> 안 바뀜

                plt.axis('off')
                plt.imshow(S)
                plt.savefig('D:/#2021_CAPSTONE/_DataSet/sound_test_data_pretreatment (spec)/spec_test/mel/' + filename.replace(".wav","") + '.png', bbox_inches='none', pad_inches=0)
                plt.close()  # plt.cla(), plt.clf(), plt.close()

                # log_melspectrogram
                P = librosa.power_to_db(S, ref=np.max)  # log_S = librosa.power_to_db(S, ref=np.max)

                plt.figure(figsize=(x_inches/dpi, y_inches/dpi), dpi=dpi, frameon=False)  # 12,4 --> 1.24, 0.8
                # librosa.display.specshow(P)  # 유무 차이, 있으면 --> 색깔 바뀜, 없으면 --> 안 바뀜

                plt.axis('off')
                plt.imshow(P)
                # bbox_inches = 'tight', padding = 0
                plt.savefig('D:/#2021_CAPSTONE/_DataSet/sound_test_data_pretreatment (spec)/spec_test/power_to_db/' + filename.replace(".wav","") + '.png', bbox_inches='none', pad_inches=0)
                # allocate bitmap error 방지
                plt.close()  # plt.cla(), plt.clf(), plt.close()
                # mfcc
                mfcc = librosa.feature.mfcc(S=P, n_mfcc=20)  # return : 20
                # 전처리 코드 삽입
                # plt.savefig('D:/#2021_CAPSTONE/_DataSet/sound_test_data/spec/mfcc/' + filename.replace(".wav", "") + '.png',bbox_inches='tight', pad_inches=0)

                print(mfcc.shape)

                # delta_mfcc
                delta2_mfcc = librosa.feature.delta(mfcc, order=2)
            except Exception as e:
                print(e)


            # 전처리 코드 삽입
            # plt.savefig('D:/#2021_CAPSTONE/_DataSet/sound_test_data/spec/delta2_mfcc/' + filename.replace(".wav", "") + '.png',bbox_inches='tight', pad_inches=0)

'''
            # 데이터 전처리 공백 없는 plt 파트
            plt.figure(figsize=figsize)  # 12,4 --> 1.24, 0.8
            librosa.display.specshow(P)  # 유무 차이, 있으면 --> 색깔 바뀜, 없으면 --> 안 바뀜

            # plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
            # plt.margins(0, 0)

            plt.axis('off')

            # plt.gca().set_axis_off()
            # plt.gca().xaxis.set_major_locator(plt.NullLocator())
            # plt.gca().yaxis.set_major_locator(plt.NullLocator())
            # plt.tight_layout()

            plt.imshow(P)
            # bbox_inches = 'tight', padding = 0
            plt.savefig('D:/#2021_CAPSTONE/_DataSet/sound_test_data/spec_test/power_to_db/' + filename.replace(".wav","") + '.png', bbox_inches='tight', pad_inches=0)
'''


