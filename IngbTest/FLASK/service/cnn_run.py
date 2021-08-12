import librosa, librosa.display
import matplotlib.pyplot as plt
import numpy as np
import cv2
from tensorflow.python.keras.models import load_model
import tensorflow as tf

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)

def wav2spec(filename):
    filename = "operation/"+ filename
    FIG_SIZE = (2.6, 2)
    sig, sr = librosa.load(filename, sr=22050)
    print(sig, sr)
    plt.figure(figsize=FIG_SIZE)
    plt.axis('off'), plt.xticks([]), plt.yticks([])
    plt.tight_layout()
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)
    mel = librosa.feature.melspectrogram(sig, sr)  # mel spectrogram
    P = librosa.power_to_db(mel, ref=np.max)  # log_mel spectrogram
    librosa.display.specshow(P)
    
    plt.savefig(filename + '.png', bbox_inches=None, pad_inches=0)  # /tmp/check1.png로 저장 


def pre_denoise(filename):
    filename = "operation/"+ filename
    print("pre_denoise 함수")
    FIG_SIZE = (2.6, 2)

    img = cv2.imread(filename + '.png')  # 가상환경에 저장한 것 불러옴
    dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

    plt.figure(figsize=FIG_SIZE)
    plt.axis('off'), plt.xticks([]), plt.yticks([])
    plt.tight_layout()
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace =0, wspace=0)   
    plt.imshow(dst, cmap=plt.cm.rainbow, interpolation='bicubic')
    plt.savefig(filename + '.png', bbox_inches=None, pad_inches=0)  # /tmp/denoise.png로 저장

def check_model(filename):
    filename = "operation/"+ filename
    check_model = load_model('model.h5')
    main_img = cv2.imread(filename+'.png') 
    main_img = cv2.cvtColor(main_img, cv2.COLOR_BGR2RGB)
    np.array(main_img, dtype='uint8')
    images = tf.expand_dims(main_img, 0)

    prediction = check_model.predict([images])

    if np.argmax(prediction, axis=1) == [0]:
        return "굿모닝"
    elif np.argmax(prediction, axis=1) == [1]:
        return "출근길 교통 상황 어때"
    else:
        return "내일 날씨 어때"
