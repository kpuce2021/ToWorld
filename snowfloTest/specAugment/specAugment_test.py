import librosa
import librosa.display
import tensorflow as tf
import os
import numpy as np
import matplotlib.pyplot as plt
from specAugment import spec_augment_tensorflow
import cv2
from PIL import Image
plt.rcParams.update({'figure.max_open_warning': 0})

from tensorflow.python.client import device_lib
print(device_lib.list_local_devices())

tf.compat.v1.disable_v2_behavior()
sess = tf.compat.v1.Session()

# gpu = tf.config.experimental.list_physical_devices ('GPU')
# tf.config.experimental.set_memory_growth (gpu [0], True)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def sparse_warp(mel_spectrogram, time_warping_para=80):

    fbank_size = tf.shape(mel_spectrogram)
    n, v = fbank_size[1], fbank_size[2]

    pt = tf.random.uniform([], time_warping_para, n-time_warping_para, tf.int32) # radnom point along the time axis
    src_ctr_pt_freq = tf.range(v // 2)  # control points on freq-axis
    src_ctr_pt_time = tf.ones_like(src_ctr_pt_freq) * pt  # control points on time-axis
    src_ctr_pts = tf.stack((src_ctr_pt_time, src_ctr_pt_freq), -1)
    src_ctr_pts = tf.cast(src_ctr_pts, dtype=tf.float32)

    # Destination
    w = tf.random.uniform([], -time_warping_para, time_warping_para, tf.int32)  # distance
    dest_ctr_pt_freq = src_ctr_pt_freq
    dest_ctr_pt_time = src_ctr_pt_time + w
    dest_ctr_pts = tf.stack((dest_ctr_pt_time, dest_ctr_pt_freq), -1)
    dest_ctr_pts = tf.cast(dest_ctr_pts, dtype=tf.float32)

    # warp
    source_control_point_locations = tf.expand_dims(src_ctr_pts, 0)  # (1, v//2, 2)
    dest_control_point_locations = tf.expand_dims(dest_ctr_pts, 0)  # (1, v//2, 2)

    warped_image, _ = tf.contrib.image.sparse_image_warp(mel_spectrogram, source_control_point_locations, dest_control_point_locations)
    return warped_image


def frequency_masking(mel_spectrogram, v, frequency_masking_para=27, frequency_mask_num=2):

    fbank_size = tf.shape(mel_spectrogram)
    n, v = fbank_size[1], fbank_size[2]

    for i in range(frequency_mask_num):
        f = tf.random.uniform([], minval=0, maxval=frequency_masking_para, dtype=tf.int32)
        v = tf.cast(v, dtype=tf.int32)
        f0 = tf.random.uniform([], minval=0, maxval=v-f, dtype=tf.int32)

        # warped_mel_spectrogram[f0:f0 + f, :] = 0
        mask = tf.concat((tf.ones(shape=(1, n, v - f0 - f, 1)),
                          tf.zeros(shape=(1, n, f, 1)),
                          tf.ones(shape=(1, n, f0, 1)),
                          ), 2)
        mel_spectrogram = mel_spectrogram * mask
    return tf.cast(mel_spectrogram, dtype=tf.float32)


def time_masking(mel_spectrogram, tau, time_masking_para=100, time_mask_num=2):

    fbank_size = tf.shape(mel_spectrogram)
    n, v = fbank_size[1], fbank_size[2]

    # Step 3 : Time masking
    for i in range(time_mask_num):
        t = tf.random.uniform([], minval=0, maxval=time_masking_para, dtype=tf.int32)
        t0 = tf.random.uniform([], minval=0, maxval=tau-t, dtype=tf.int32)

        mask = tf.concat((tf.ones(shape=(1, n-t0-t, v, 1)),
                          tf.zeros(shape=(1, t, v, 1)),
                          tf.ones(shape=(1, t0, v, 1)),
                          ), 1)
        mel_spectrogram = mel_spectrogram * mask
    return tf.cast(mel_spectrogram, dtype=tf.float32)


def spec_augment(mel_spectrogram):
    v = mel_spectrogram.shape[0]
    tau = mel_spectrogram.shape[1]
    warped_mel_spectrogram = sparse_warp(mel_spectrogram)
    warped_frequency_spectrogram = frequency_masking(warped_mel_spectrogram, v=v)
    warped_frequency_time_sepctrogram = time_masking(warped_frequency_spectrogram, tau=tau)
    return warped_frequency_time_sepctrogram


def visualization_spectrogram(mel_spectrogram, title):
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(librosa.power_to_db(mel_spectrogram[0, :, :, 0], ref=np.max), y_axis='mel', fmax=8000, x_axis='time')
    plt.title(title)
    plt.tight_layout()
    plt.show()


def visualization_tensor_spectrogram(mel_spectrogram, title):
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(librosa.power_to_db(mel_spectrogram[0, :, :, 0], ref=np.max), y_axis='mel', fmax=8000, x_axis='time')
    plt.title(title)
    plt.tight_layout()
    plt.show()


FIG_SIZE = (2.6, 2)

def specAug_run(img_path):
    for root, subdirs, files in os.walk(img_path):
        for fname in files:
            print(fname)
            full_fname = os.path.join(root, fname)
            audio, sampling_rate = librosa.load(full_fname)

            plt.figure(figsize=FIG_SIZE)  # 크기 조정
            plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
            plt.margins(0, 0)
            plt.gca().set_axis_off()
            plt.gca().xaxis.set_major_locator(plt.NullLocator())
            plt.gca().yaxis.set_major_locator(plt.NullLocator())

            mel_spectrogram = librosa.feature.melspectrogram(y=audio, sr=sampling_rate,n_mels=256, hop_length=128,fmax=8000)
            mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)
            print(mel_spectrogram.shape)
            # plt.figure(figsize=FIG_SIZE)  # 크기 조정
            # plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
            # plt.margins(0, 0)
            # plt.gca().set_axis_off()
            # plt.gca().xaxis.set_major_locator(plt.NullLocator())
            # plt.gca().yaxis.set_major_locator(plt.NullLocator())
            # plt.imshow(mel_spectrogram)
            # plt.savefig('warehouse2/dd/' + fname + '_vs2.png', bbox_inches='tight', pad_inches=0)
            # plt.show()

            plt.imshow(mel_spectrogram)

            for i in range(0,3):
                warped_masked_spectrogram = spec_augment_tensorflow.spec_augment(mel_spectrogram=mel_spectrogram) # 한 데이터에대해서 random으로 들어오니까 여러번 반복해주면 될듯                plt.imshow(warped_masked_spectrogram)
                # plt.show()
                print(warped_masked_spectrogram)
                #plt.savefig('spec_aug/traindata/augment_t/'+ fname +'_' + str(i) + '.png', bbox_inches='tight', pad_inches=0)
                plt.savefig('E:/##kpu_capstone_voice_data/#spec_data_augment/call_sangho/' + fname + str(i) + '_aug.png', bbox_inches='tight', pad_inches=0)

def denoise_run():
    for root, subdirs, files in os.walk('C:/Users/zzzma/PycharmProjects/specAugment/ingb/spec/weather_spec'):
        for fname in files:
            plt.figure(figsize=(2.60, 2))
            full_fname = os.path.join(root, fname)
            img = cv2.imread(full_fname)
            dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
            # gray = rgb2gray(dst)
            plt.gca().set_axis_off()
            '''
            src
            dst
            h       : 필터 강도 결정, 높을수록 제거가 강함, 10이면 적당?
            hColor  : h와 동일, 칼라 이미지만 적용, 보통 h와 동일
            templateWindowSize  : 홀수값 7권장
            searchWindowSize    : 홀수값 21권장
            '''
            plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
            plt.gca().xaxis.set_major_locator(plt.NullLocator())
            plt.gca().yaxis.set_major_locator(plt.NullLocator())
            plt.imshow(dst)
            # plt.imshow(gray, cmap=plt.get_cmap('gray'), vmin=0, vmax=1)
            plt.savefig(full_fname)

FIG_SIZE = (2.6, 2)

def wav2sepc():
    for i in range(1, 4):
        plt.figure(figsize=FIG_SIZE)
        audio, sampling_rate = librosa.load("prediction/g/g"+ str(i) +".wav")
        mel_spectrogram = librosa.feature.melspectrogram(y=audio, sr=sampling_rate, n_mels=256, hop_length=128, fmax=8000)
        mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)
        plt.gca().set_axis_off()
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.imshow(mel_spectrogram)
        plt.savefig('g'+str(i)+'.png')


def resize_and_crop(img_path, modified_path, size, crop_type='middle'):
    files = os.listdir(img_path)
    for file in files:
        name = str(file)
        os.chdir(img_path)
        img = Image.open(file)
        img_ratio = img.size[0] / float(img.size[1])
        ratio = size[0] / float(size[1])

        if ratio > img_ratio:
            img = img.resize((size[0], int(round(size[0] * img.size[1] / img.size[0]))),
                             Image.ANTIALIAS)
            if crop_type == 'top':
                box = (0, 0, img.size[0], size[1])
            elif crop_type == 'middle':
                box = (0, int(round((img.size[1] - size[1]) / 2)), img.size[0],
                       int(round((img.size[1] + size[1]) / 2)))
            elif crop_type == 'bottom':
                box = (0, img.size[1] - size[1], img.size[0], img.size[1])
            else:
                raise ValueError('ERROR: invalid value for crop_type')
            img = img.crop(box)

        elif ratio < img_ratio:
            img = img.resize((int(round(size[1] * img.size[0] / img.size[1])), size[1]),
                             Image.ANTIALIAS)
            if crop_type == 'top':
                box = (0, 0, size[0], img.size[1])
            elif crop_type == 'middle':
                box = (int(round((img.size[0] - size[0]) / 2)), 0,
                       int(round((img.size[0] + size[0]) / 2)), img.size[1])
            elif crop_type == 'bottom':
                box = (img.size[0] - size[0], 0, img.size[0], img.size[1])
            else:
                raise ValueError('ERROR: invalid value for crop_type')
            img = img.crop(box)

        else:
            img = img.resize((size[0], size[1]), Image.ANTIALIAS)

        os.chdir(modified_path)
        img.save(name, "PNG")


if __name__ == "__main__":
     # wav2sepc()
     # size = 256, 128

     img_path = "E:/##kpu_capstone_voice_data/call_sangho"
     modified_path = "E:/##kpu_capstone_voice_data/#spec_data_augment/call_sangho/"
     specAug_run(img_path) #디렉토리의 이름을 추가해줌

