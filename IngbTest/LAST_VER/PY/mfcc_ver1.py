import librosa
import librosa.display
import os
import numpy as np
import matplotlib.pyplot as plt

sample_rate= 44100

def mfcc(path):
    for root, subdirs, files in os.walk('C:/Users/zzzma/PycharmProjects/PyAloha/final_audio/'+ path):
        i = 0
        for fname in files:
            full_fname = os.path.join(root, fname)
            print(full_fname)
            audio = librosa.load(full_fname, sample_rate)[0]

            S = librosa.feature.melspectrogram(audio, sr = sample_rate, n_mels = 128) # sample_rate: 이산적(離散的)인 신호를 만들기 위해 연속적 신호에서 얻어진 단위시간(주로 초)당 샘플링 횟수를 정의
                                                                                      # n_mels: mel filter의 개수
            log_S = librosa.power_to_db(S, ref=np.max)
            mfcc = librosa.feature.mfcc(S=log_S, n_mfcc=20)

            delta2_mfcc = librosa.feature.delta(mfcc, order=2)

            # print(delta2_mfcc.shape)
            plt.figure(figsize=(12, 4))
            librosa.display.specshow(delta2_mfcc)
            plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
            plt.margins(0, 0)
            plt.gca().set_axis_off()
            plt.gca().xaxis.set_major_locator(plt.NullLocator())
            plt.gca().yaxis.set_major_locator(plt.NullLocator())
            plt.tight_layout()
            plt.imshow(delta2_mfcc)
            # plt.savefig('C:/Users/zzzma/PycharmProjects/PyAloha/mfcc/mfcc_test/mfcc/good/good'+ str(i)+'.png', bbox_inches='tight', pad_inches=0)

            plt.savefig('C:/Users/zzzma/PycharmProjects/PyAloha/mfcc/mfcc_test/mfcc/good/' +  fname.replace(".wav","") + '.png',
                        bbox_inches='tight', pad_inches=0)
            i += 1
            # print(log_S)

if __name__ == '__main__':
    mfcc('test')