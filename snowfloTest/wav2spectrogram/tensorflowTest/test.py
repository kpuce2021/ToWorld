import matplotlib.pyplot as plt
import librosa.display
import librosa
import numpy as np
import os

path = "D:/#2021_CAPSTONE/_DataSet/sound_data_original (wav)/ingb/굿모닝"
sample_rate = 44100
formats_to_convert = ['.wav']

dpi = 128
x_pixels = 512  # 4배 키움 data_prestatement에 비해서
y_pixels = 160

for (dirpath, dirnames, filenames) in os.walk(path):  # 상위 폴더
    for filename in filenames:
        # print('dirpath: ', dirpath)
        # print('dirnames : ', dirnames)
        print('filenames: ', filename)

        if filename.endswith(tuple(formats_to_convert)):
            filepath = os.path.join(dirpath, filename)
            wav, sampling_rate = librosa.load(filepath, sample_rate)
            mel = librosa.feature.melspectrogram(wav, sr=sample_rate, n_mels=128)  # returns : 128 (채널수)
            librosa.display.specshow(mel)

            # plt.figure(figsize=(x_pixels/dpi, y_pixels/dpi),dpi=128)
            # plt.axis('off')  #, plt.xticks([]), plt.yticks([])
            #
            # plt.imshow(mel)
            # plt.savefig('D:/#2021_CAPSTONE/_DataSet/sound_test_data_pretreatment (spec)/spec_test/mel/' + filename.replace(".wav","") + '.png', bbox_inches='tight', pad_inches=0)
            # plt.close()  # plt.cla(), plt.clf(), plt.close()

            log_S = librosa.power_to_db(mel, ref=np.max)  # log_S = librosa.power_to_db(S, ref=np.max)
            librosa.display.specshow(log_S)

            # plt.figure(figsize=(x_pixels/dpi, y_pixels/dpi),dpi=128)
            # plt.axis('off')
            #
            # plt.imshow(log_S)
            # plt.savefig('D:/#2021_CAPSTONE/_DataSet/sound_test_data_pretreatment (spec)/spec_test/power_to_db/' + filename.replace(".wav","") + '.png', bbox_inches='tight', pad_inches=0)
            # plt.close()  # plt.cla(), plt.clf(), plt.close()

            mfcc = librosa.feature.mfcc(S=log_S, n_mfcc=20)  # return : 20
            librosa.display.specshow(mfcc)

            plt.figure(figsize=(x_pixels/dpi, y_pixels/dpi),dpi=128)
            plt.axis('off')

            plt.imshow(mfcc)
            plt.savefig('D:/#2021_CAPSTONE/_DataSet/sound_test_data_pretreatment (spec)/spec_test/test_mfcc/' + filename.replace(".wav", "") + '.png',bbox_inches='tight', pad_inches=0)
            plt.close()  # plt.cla(), plt.clf(), plt.close()

            delta2_mfcc = librosa.feature.delta(mfcc, order=2)
            librosa.display.specshow(delta2_mfcc)

            plt.figure(figsize=(x_pixels/dpi, y_pixels/dpi),dpi=128)
            plt.axis('off')

            plt.imshow(delta2_mfcc)
            plt.savefig('D:/#2021_CAPSTONE/_DataSet/sound_test_data_pretreatment (spec)/spec_test/test_delta2_mfcc/' + filename.replace(".wav", "") + '.png',bbox_inches='tight', pad_inches=0)
            plt.close()  # plt.cla(), plt.clf(), plt.close()
