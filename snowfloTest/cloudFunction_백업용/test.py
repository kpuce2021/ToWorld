import os
import traceback

import numpy
from pydub import AudioSegment
# from PIL.ImageQt import rgb
# from tensorflow.python.keras.models import load_model
from matplotlib import pyplot as plt
import librosa.display
import librosa
import cv2
from PIL import Image
from skimage.color import rgb2gray

formats_to_convert = ['.m4a']
def m4a2wav():
    for (dirpath, dirnames, filenames) in os.walk("D:/all"): # 경로 변경해야 함.
        for filename in filenames:
            if filename.endswith(tuple(formats_to_convert)):

                filepath = dirpath + '/' + filename
                (path, file_extension) = os.path.splitext(filepath)
                file_extension_final = file_extension.replace('.', '')

                try:
                    track = AudioSegment.from_file(filepath,
                                                   file_extension_final)
                    wav_filename = filename.replace(file_extension_final, 'wav')
                    wav_path = dirpath + '/' + wav_filename
                    print('CONVERTING: ' + str(filepath))
                    file_handle = track.export(wav_path, format='wav')
                    os.remove(filepath)
                except:
                    print(traceback.print_exc())

'''
def wav2sepc():
    FIG_SIZE = (2.56, 1.28)
    plt.figure(figsize=FIG_SIZE)
    audio, sampling_rate = librosa.load('test/g1.wav')
    mel_spectrogram = librosa.feature.melspectrogram(y=audio, sr=sampling_rate, n_mels=256, hop_length=128, fmax=8000)
    mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=numpy.max)
    plt.imshow(mel_spectrogram)
    plt.gca().set_axis_off()
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.savefig('check.png')

def pre_denoise():

    img = cv2.imread('check.png')
    dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    gray = rgb2gray(dst)
    plt.imshow(gray, cmap= plt.get_cmap('gray'), vmin=0, vmax= 1)
    plt.gca().set_axis_off()
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.savefig('grayed.png')
'''
if __name__ == '__main__':
    m4a2wav()
   # wav2sepc()
   # pre_denoise()