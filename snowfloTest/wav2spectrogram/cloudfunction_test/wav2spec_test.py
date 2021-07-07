import numpy as np
import librosa, librosa.display
import matplotlib.pyplot as plt

#file_directory
filepath = 'D:/#2021_CAPSTONE/_DataSet/sound_data_original (m4a)/test_m4a2wav/'
filename = 'my_audio_file.wav'

# wav2spec
def wav2spec(filepath):
    print("wav2spec 함수")

    FIG_SIZE = (2.6, 2)

    sig, sr = librosa.load(filepath, sr=22050)

    plt.figure(figsize=FIG_SIZE)
    plt.axis('off'), plt.xticks([]), plt.yticks([])
    plt.tight_layout()
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)

    mel = librosa.feature.melspectrogram(sig, sr)  # mel spectrogram
    P = librosa.power_to_db(mel, ref=np.max)  # log_mel spectrogram
    librosa.display.specshow(P)

    plt.savefig('android_file (1).png', bbox_inches=None, pad_inches=0)  # /tmp/check1.png로 저장
    # upload_blob('kpu2021mk3-220df.appspot.com', '/tmp/check1.png', 'check_wav2spec_file.png')

wav2spec(filepath+filename)