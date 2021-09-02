import numpy as np
import librosa, librosa.display
import matplotlib.pyplot as plt

FIG_SIZE = (0.5,0.5) # FIG_SIZE * DPI # 조절 필요

# melsepctrogram // 과거 파일
file = "E:/##kpu_capstone_voice_data/good_morning_/"
for i in range(1,177):
    sig, sr = librosa.load(file +"g"+str(i)+".wav", sr=22050) # sampling rate 샘플링의 속도 ; 샘플링이란 아날로그 데이터에서 디지털 데이터를 추출하는 것 ; 즉 1초에 얼마나 읽는지 샘플링 레이트

    print(sr)
    print(sig, sig.shape)

    plt.figure(figsize=FIG_SIZE)
    plt.axis('off'), plt.xticks([]), plt.yticks([])
    plt.tight_layout()
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)

    mel = librosa.feature.melspectrogram(sig, sr)
    P = librosa.power_to_db(mel, ref=np.max)
    librosa.display.specshow(P)

    plt.savefig('D:/#2021_CAPSTONE/_DataSet/spec_data/good_morning_u/good_morning_u' + str(i) + '.png', bbox_inches=None, pad_inches=0)
    '''
    librosa.display.waveplot(sig, sr, alpha=0.5)

    hop_length = 512  # 전체 frame 수
    n_fft = 2048  # frame 하나당 sample 수

    # calculate duration hop length and window in seconds
    hop_length_duration = float(hop_length) / sr
    n_fft_duration = float(n_fft) / sr

    # STFT
    stft = librosa.stft(sig, n_fft=n_fft, hop_length=hop_length)

    # 복소공간 값 절댓값 취하기
    magnitude = np.abs(stft)

    # magnitude > Decibels
    log_spectrogram = librosa.amplitude_to_db(magnitude)

    # display spectrogram
    plt.figure(figsize=FIG_SIZE)
    plt.axis('off'), plt.xticks([]), plt.yticks([])
    plt.tight_layout()
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace =0, wspace=0)

    librosa.display.specshow(log_spectrogram, sr=sr, hop_length=hop_length)
    #plt.xlabel("Time")
    #plt.ylabel("Frequency")

    #plt.colorbar(format="%+2.0f dB")
    #plt.title("Spectrogram (dB)")

    plt.savefig("gpng/fig"+str(i)+".png", dpi = 300, facecolor = 'none')
    '''