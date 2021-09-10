import librosa, librosa.display
import matplotlib.pyplot as plt
import numpy as np
import cv2
from tensorflow.python.keras.models import load_model
import tensorflow as tf
import os
from distutils.dir_util import copy_tree
import random


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


def wav2spec(filename, email):
    filename = "operation/"+ email + "/" + filename
    FIG_SIZE = (2.6, 2)
    sig, sr = librosa.load(filename, sr=22050)
    plt.figure(figsize=FIG_SIZE)
    plt.axis('off'), plt.xticks([]), plt.yticks([])
    plt.tight_layout()
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)
    mel = librosa.feature.melspectrogram(sig, sr)  # mel spectrogram
    P = librosa.power_to_db(mel, ref=np.max)  # log_mel spectrogram
    librosa.display.specshow(P)
    
    plt.savefig(filename + '.png', bbox_inches=None, pad_inches=0)  # /tmp/check1.png로 저장 


def pre_denoise(filename, email):
    filename = "operation/" + email + "/" + filename
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


# 학습모드
def cnn_pre_denoise(filename, isThere, email, answer):
    filename = "operation/" + email + "/"+ filename
    FIG_SIZE = (2.6, 2)

    img = cv2.imread(filename + '.png')  # 가상환경에 저장한 것 불러옴
    dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

    plt.figure(figsize=FIG_SIZE)
    plt.axis('off'), plt.xticks([]), plt.yticks([])
    plt.tight_layout()
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace =0, wspace=0)   
    plt.imshow(dst, cmap=plt.cm.rainbow, interpolation='bicubic')

    if(isThere > 0):                # 이미 존재
        path = "temp/" + email + "/" + answer

        if(isThere % 5 == 0):
          print("___데이터베이스 내의 파일의 개수가 몇의 배수이면 Convolution을 수행합니다___")
          # convolution() 
    else:                           # 기존에 존재하지 않음 == 0
        print("___문장이 없을 경우 새로운 파일이 생성됩니다___")
        path = "temp/" + email + "/" + answer
        os.makedirs(path)       # 폴더 여러개 생성

    pre_aug_png = answer + str(isThere+1) + ".png"
    final_path = path + "/" + pre_aug_png
   
    plt.savefig(final_path, bbox_inches=None, pad_inches=0)  # /tmp/denoise.png로 저장

    spec_aug(final_path)
    

def check_model(filename, email):
    filename = "operation/"+ email + "/" + filename
    check_model = load_model('model/model.h5')
    main_img = cv2.imread(filename+'.png') 
    main_img = cv2.cvtColor(main_img, cv2.COLOR_BGR2RGB)
    np.array(main_img, dtype='uint8')
    images = tf.expand_dims(main_img, 0)

    prediction = check_model.predict([images])

    if np.argmax(prediction, axis=1) == [0]:
        return "상호한테 전화해줘"
    elif np.argmax(prediction, axis=1) == [1]:
        return "굿모닝"
    elif np.argmax(prediction, axis=1) == [2]:
        return "출근길 교통상황 어때"    
    elif np.argmax(prediction, axis=1) == [3]:
        return "음악 추천해줘"
    elif np.argmax(prediction, axis=1) == [4]:
        return "오늘 날씨 어때"
    elif np.argmax(prediction, axis=1) == [5]:
        return "내일 날씨 어때"    
    else:
        return "유트브에서 동빈나 틀어줘"

def spec_aug(final_path):

      for i in range(5):

        cv_path = np.fromfile(final_path, np.uint8)
        img = cv2.imdecode(cv_path, cv2.IMREAD_COLOR)
        
        aug_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        col = random.randrange(0, 200)  # 0 ~ 200
        row = random.randrange(0, 260)  # 0 ~ 260

        col_r = random.randrange(0, 50)
        row_r = random.randrange(0, 50)

        cp_img = aug_img[0:200, row:row + row_r]
        cp_img.fill(255)

        cp_img = aug_img[col:col + col_r, 0:260]
        cp_img.fill(255)

        plt.figure(figsize=(2.6, 2))
        plt.axis('off'), plt.xticks([]), plt.yticks([])
        plt.tight_layout()
        plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)

        plt.imshow(aug_img, cmap=plt.cm.rainbow, interpolation='bicubic')
        plt.savefig(final_path + str(i) + '_augment.png', bbox_inches=None, pad_inches=0)