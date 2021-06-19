import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
import tensorflow as tf

from tensorflow import keras
from keras import layers
from keras.models import Sequential
import pathlib
import matplotlib.pyplot as plt

import os
# 사용중인 device 확인
tf.debugging.set_log_device_placement(True)

# gpu 할당하는 방법
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="0"

# gpus = tf.config.experimental.list_physical_devices('GPU')
# if gpus:
#     try:
#         # Currently, memory growth needs to be the same across GPUs
#         for gpu in gpus:
#             tf.config.experimental.set_memory_growth(gpu, True)
#         logical_gpus = tf.config.experimental.list_logical_devices('GPU')
#         print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
#     except RuntimeError as e:
#         # Memory growth must be set before GPUs have been initialized
#         print(e)
# cnn에는 동일 크기의 image_input이 필요 --> spectrogram 고정 필요가 있음.
    # input 설정

# 재희한테 물어봐
# 1번함수
def get_label(file_path):  # 클래스 이름
    # convert the path to a list of path components
    parts = tf.strings.split(file_path, os.path.sep)
    # The second to last is the class-directory
    one_hot = parts[-2] == class_names
    # Integer encode the label
    return tf.argmax(one_hot)

def decode_img(img):  # ???
    # convert the compressed string to a 3D uint8 tensor
    img = tf.image.decode_jpeg(img, channels=3)
    # resize the image to the desired size
    return tf.image.resize(img, [img_height, img_width])

def process_path(file_path):  # ???
    label = get_label(file_path)
    # load the raw data from the file as a string
    img = tf.io.read_file(file_path)
    img = decode_img(img)
    return img, label

# 2번 함수
def configure_for_performance(ds):  # ???
    ds = ds.cache()
    ds = ds.shuffle(buffer_size=1000)
    ds = ds.batch(batch_size)
    ds = ds.prefetch(buffer_size=AUTOTUNE)
    return ds

data_dir = pathlib.Path('D:/#2021_CAPSTONE/_DataSet/sound_test_data_pretreatment (spec)/final_mel_spec_data')  # file path
print(data_dir)
image_count = len(list(data_dir.glob('*/*.png')))
print(image_count)

with tf.device('/GPU:0'):
# 자기마음
    batch_size = 32  # 파일 몇 개 읽을지
    # 순서가 세로/가로임 --> 그래서 세로/가로로 함 input_size
    img_height = 210
    img_width = 432
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(  # train
        data_dir,
        validation_split=0.2,  # test --> 0.2, train --> 0.8
        subset="training",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(  # validation
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)


    class_names = train_ds.class_names
    print(class_names)
    num_classes = len(class_names)
    print(num_classes)

    AUTOTUNE = tf.data.experimental.AUTOTUNE

    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)

    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
    normalization_layer = layers.experimental.preprocessing.Rescaling(1./255)
    normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
    image_batch, labels_batch = next(iter(normalized_ds))
    first_image = image_batch[0]
    # Notice the pixels values are now in `[0,1]`.
    print(np.min(first_image), np.max(first_image))

    # 모델
    model = Sequential([
        layers.experimental.preprocessing.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
        layers.Conv2D(16, (3,3), padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, (3,3), padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, (3,3), padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Dropout(0.2),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes)
    ])
    # 모델 컴파일
    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])
    # 모델 정보
    model.summary()

    # 에폭시 --> 반복수
    EPOCHS = 100

    # ???
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS,
        #callbacks=tf.keras.callbacks.EarlyStopping(verbose=1, patience=2)
    )

    train_avg = np.mean(history.history['accuracy'])  # 평균
    test_avg = np.mean(history.history['val_accuracy'])  # 평균
    print('train_avg = {0:.4f}'.format(train_avg))
    print('test_avg = {0:.4f}'.format(test_avg))

    print(history)

    #model.evaluate_generator()

    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']

    loss=history.history['loss']
    val_loss=history.history['val_loss']

    epochs_range = range(EPOCHS)

    # 그래프 1
    plt.figure(figsize=(8, 8))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')
    # 그래프 2
    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.show()

import cv2
import numpy as np

'''
 - channel : 컬러 3, 흑백 1
 - stride : 이동 크기
 - padding : 출력 데이터 크기 맞추기
 - pooling : feature 강조
 https://statinknu.tistory.com/25
 
 error: 이미지 크기 문제
'''
