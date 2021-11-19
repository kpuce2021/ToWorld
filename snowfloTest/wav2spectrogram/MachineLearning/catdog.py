# %% GPU Test

import tensorflow as tf

tf.config.list_physical_devices('GPU')

from tensorflow.python.client import device_lib

print(device_lib.list_local_devices())

# %% 작업경로 설정

import os
from tensorflow import keras

root_dir = "C:\\Users\\Ruzzy\\Desktop\\dogs-vs-cats"

raw_data_dir = os.path.join(root_dir, 'train')  # 원본 데이터(캐글 데이터) 디렉토리

# %% 작업 디렉토리 생성

work_dir = os.path.join(root_dir, "data")
if not os.path.isdir(work_dir):
    os.mkdir(work_dir)

train_dir = os.path.join(work_dir, 'train')
if not os.path.isdir(train_dir):
    os.mkdir(train_dir)

validation_dir = os.path.join(work_dir, 'validation')
if not os.path.isdir(validation_dir):
    os.mkdir(validation_dir)

test_dir = os.path.join(work_dir, 'test')
if not os.path.isdir(test_dir):
    os.mkdir(test_dir)

os.startfile(work_dir)

# %% 데이터셋 분할

from sklearn.model_selection import train_test_split


def split_dataset(path, test_size=0.2, validation_size=0.2):
    raw_dataset = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    seed = 66

    train_data, test_data = train_test_split(raw_dataset, random_state=seed, test_size=test_size)

    if validation_size > 0:
        train_data, validation_data = train_test_split(train_data, random_state=seed, test_size=validation_size)
    else:
        validation_data = []

    return [train_data, validation_data, test_data]


train, validation, test = split_dataset(raw_data_dir, 0.2, 0.2)

print('Train num'.ljust(15) + ' : ' + str(len(train)))
print('Validation num'.ljust(15) + ' : ' + str(len(validation)))
print('Test num'.ljust(15) + ' : ' + str(len(test)))

# %% 데이터 폴더별 정리

import re
import shutil


def grouping_dataset(path, files=None, copy=True):
    if not os.path.isdir(os.path.join(path, "dog")):
        os.mkdir(os.path.join(path, "dog"))
    if not os.path.isdir(os.path.join(path, "cat")):
        os.mkdir(os.path.join(path, "cat"))

    if files is None:
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        print("found {0} files in directory.".format(len(files)))
    else:
        files = [f for f in files if os.path.isfile(f)]
        print("get {0} files from list.".format(len(files)))

    regex = re.compile(r'(?P<name>\w+)\.(?P<num>\d+)\.(?P<ext>\w+)')

    i = 0
    for filepath in files:

        file = os.path.basename(filepath)
        result = regex.search(file)
        group = result.group("name")

        if i % 100 == 0:
            print(file + ' → ' + os.path.join(path, group, file) + '\t[{0} of {1}]'.format(i, len(files)))

        if copy:
            shutil.copyfile(filepath, os.path.join(path, group, file))
        else:
            os.rename(filepath, os.path.join(path, group, file))

        i += 1

    print("done with {0} files".format(i))


grouping_dataset(path=train_dir, files=train, copy=True)  # Copy=False로 해야 빠름 (파일이동)
grouping_dataset(path=validation_dir, files=validation, copy=True)
grouping_dataset(path=test_dir, files=test, copy=True)

# %% Image Generator 생성 (훈련, 검증, 테스트)

image_width = 128
image_height = 128
image_channel = 3

image_size = (image_width, image_height)
batch_size = 32

generator_train = keras.preprocessing.image.ImageDataGenerator(rescale=1. / 255,
                                                               rotation_range=15,  # 회전
                                                               shear_range=0.1,  # 기울임
                                                               zoom_range=0.2,  # 확대/축소
                                                               horizontal_flip=True,  # 좌우반전
                                                               width_shift_range=0.1,  # 평행이동 (좌우)
                                                               height_shift_range=0.1  # 평행이동 (상하)
                                                               )

generator_val = keras.preprocessing.image.ImageDataGenerator(rescale=1. / 255)
generator_test = keras.preprocessing.image.ImageDataGenerator(rescale=1. / 255)

train_images = generator_train.flow_from_directory(
    train_dir,
    batch_size=batch_size,
    class_mode='categorical',
    target_size=image_size
)

validation_images = generator_val.flow_from_directory(
    validation_dir,
    batch_size=batch_size,
    class_mode='categorical',
    target_size=image_size
)

test_images = generator_test.flow_from_directory(
    test_dir,
    batch_size=32,
    class_mode='categorical',
    target_size=image_size
)

# %% 데이터 시각화

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['toolbar'] = 'None'
plt.rcParams['figure.raise_window'] = 'True'

fig, axs = plt.subplots(3, 3, figsize=(10, 10))
fig.canvas.manager.set_window_title('Cats vs Dogs')
fig.suptitle('Train Dataset Batch Sample', fontsize=16)

images, labels = train_images.next()

class_names = train_images.class_indices
label_map = dict((v, k) for k, v in train_images.class_indices.items())

for i in range(9):
    image = images[i]
    idx = np.argmax(labels[i], axis=-1)
    ax = axs[int(i / 3), i % 3]
    ax.imshow(image)
    ax.set_title(label_map[idx])
    ax.axis("off")

train_images.reset()

# %% CNN 모델 구성

model = keras.Sequential(
    name="CatDog_Classifier",
    layers=[
        # Input layer
        keras.layers.Conv2D(
            name='Input',
            filters=32,
            kernel_size=(3, 3),
            activation='relu',
            input_shape=(image_width, image_height, image_channel)
        ),
        keras.layers.BatchNormalization(),
        keras.layers.MaxPooling2D(pool_size=(2, 2)),
        keras.layers.Dropout(0.25),

        # Hidden 1 layer (Convolution)
        keras.layers.Conv2D(
            name='Hidden_1',
            filters=64,
            kernel_size=(3, 3),
            activation='relu'
        ),
        keras.layers.BatchNormalization(),
        keras.layers.MaxPooling2D(pool_size=(2, 2)),
        keras.layers.Dropout(0.25),

        # Hidden 2 layer (Convolution)
        keras.layers.Conv2D(
            name='Hidden_2',
            filters=64,
            kernel_size=(3, 3),
            activation='relu'
        ),
        keras.layers.BatchNormalization(),
        keras.layers.MaxPooling2D(pool_size=(2, 2)),
        keras.layers.Dropout(0.25),

        # Hidden 3 layer (Convolution)
        keras.layers.Conv2D(
            name='Hidden_3',
            filters=128,
            kernel_size=(3, 3),
            activation='relu'
        ),
        keras.layers.BatchNormalization(),
        keras.layers.MaxPooling2D(pool_size=(2, 2)),
        keras.layers.Dropout(0.25),

        # Hidden 4 layer (Fully Connected)
        keras.layers.Flatten(),

        keras.layers.Dense(units=512, activation='relu', name="Dense_1"),
        keras.layers.BatchNormalization(),
        keras.layers.Dropout(0.25),

        # Output layer (Softmax)
        keras.layers.Dense(units=2, activation='softmax', name="Output"),
    ]
)

model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.summary()

# %%

train_history = model.fit(train_images,
                          validation_data=validation_images,
                          steps=np.ceil(train_images.samples / batch_size),
                          epochs=5)

# %% 학습된 가중치 저장

model.save_weights('./checkpoints/model_catdog_5epoch')

# %% 학습된 가중치 불러오기

model.load_weights('./checkpoints/model_catdog_5epoch')

# %% 학습 결과 플롯

print(train_history.history.keys())

plt.plot(train_history.history['accuracy'], 'g')
plt.plot(train_history.history['loss'], 'r')

plt.ylim(0.0, 1.0)

plt.title('Model accuracy & loss')
plt.ylabel('accuracy & loss')
plt.xlabel('epoch')
plt.legend(['train'], loc='upper left')
plt.show()

# %% 모델 학습결과 평가

test_loss, test_acc = model.evaluate(test_images,
                                     steps=np.ceil(test_images.samples / batch_size))

print('\nTest accuracy:', test_acc)

# %% 모델 테스트 예측 및 시각화

fig, axs = plt.subplots(3, 3, figsize=(10, 10))

fig.canvas.manager.set_window_title('Cats vs Dogs')
fig.suptitle('Test Prediction Result', fontsize=16)

test_images.shuffle = True
images, labels = test_images.next()

predict = model.predict(images)
prediction = np.argmax(predict, axis=-1)

for i in range(9):
    image = images[i]
    idx = np.argmax(labels[i], axis=-1)
    ax = axs[int(i / 3), i % 3]
    ax.imshow(image)
    ax.set_title(label_map[idx])
    ax.axis("off")

    if idx == prediction[i]:
        color = 'green'
    else:
        color = 'red'
    ax.text(0.5, 15.5, "This is {0}".format(label_map[prediction[i]]), fontsize=20, color=color)

test_images.reset()


