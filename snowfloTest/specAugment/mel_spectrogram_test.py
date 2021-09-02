import librosa
import librosa.display
import tensorflow as tf
import os
import numpy as np
import matplotlib.pyplot as plt
from specAugment import spec_augment_tensorflow
import cv2
from PIL import Image

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

FIG_SIZE = (2.6, 2)

def specAug_run(img_path):
    for root, subdirs, files in os.walk(img_path):
        for fname in files:
            print(fname)
            full_fname = os.path.join(root, fname)
            audio, sampling_rate = librosa.load(full_fname, sr=22050)

            # plt.figure(figsize=FIG_SIZE)  # 크기 조정
            plt.axis('off'), plt.xticks([]), plt.yticks([])  # 축끄기, 눈금끄기
            plt.tight_layout()
            plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)

            mel_spectrogram = librosa.feature.melspectrogram(audio, sampling_rate)
            mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)
            print(mel_spectrogram.shape)

            plt.imshow(mel_spectrogram)

            for i in range(0,3):
                warped_masked_spectrogram = spec_augment_tensorflow.spec_augment(mel_spectrogram=mel_spectrogram) # 한 데이터에대해서 random으로 들어오니까 여러번 반복해주면 될듯                plt.imshow(warped_masked_spectrogram)
                print(warped_masked_spectrogram)
                #plt.savefig('spec_aug/traindata/augment_t/'+ fname +'_' + str(i) + '.png', bbox_inches='tight', pad_inches=0)
                plt.savefig('E:/##kpu_capstone_voice_data/#spec_data_augment/call_sangho/' + fname + str(i) + '_aug.png', bbox_inches='tight', pad_inches=0)

FIG_SIZE = (2.6, 2)

if __name__ == "__main__":
     audio_path = "E:/##kpu_capstone_voice_data/call_sangho"
     specAug_run(audio_path)        # directory name

