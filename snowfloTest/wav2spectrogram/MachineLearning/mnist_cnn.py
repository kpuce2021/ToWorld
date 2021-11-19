from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt

# %% md

### MNIST 데이터셋 다운로드하고 준비하기

# %%

(train_images, train_labels), (test_images, test_labels) = datasets.mnist.load_data()

train_images = train_images.reshape((60000, 28, 28, 1))
test_images = test_images.reshape((10000, 28, 28, 1))

# 픽셀 값을 0~1 사이로 정규화합니다.
train_images, test_images = train_images / 255.0, test_images / 255.0

# %% md

### 합성곱 층 만들기

# 아래 6줄의 코드에서
# [Conv2D](https://www.tensorflow.org/api_docs/python/tf/keras/layers/Conv2D)와
# [MaxPooling2D](https://www.tensorflow.org/api_docs/python/tf/keras/layers/MaxPool2D) 층을 쌓는 일반적인 패턴으로 합성곱 층을 정의합니다.

# CNN은 배치(batch) 크기를 제외하고 (이미지 높이, 이미지 너비, 컬러 채널) 크기의 텐서(tensor)를 입력으로 받습니다.
# MNIST 데이터는 (흑백 이미지이기 때문에) 컬러 채널(channel)이 하나지만 컬러 이미지는 (R,G,B) 세 개의 채널을 가집니다.
# 이 예에서는 MNIST 이미지 포맷인 (28, 28, 1) 크기의 입력을 처리하는 CNN을 정의하겠습니다. 이 값을 첫 번째 층의 `input_shape` 매개변수로 전달합니다.

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))

# %% md

# 위에서 Conv2D와 MaxPooling2D 층의 출력은 (높이, 너비, 채널) 크기의 3D 텐서입니다.
# 높이와 너비 차원은 네트워크가 깊어질수록 감소하는 경향을 가집니다.
# Conv2D 층에서 출력 채널의 수는 첫 번째 매개변수에 의해 결정됩니다(예를 들면, 32 또는 64).
# 일반적으로 높이와 너비가 줄어듦에 따라 (계산 비용 측면에서) Conv2D 층의 출력 채널을 늘릴 수 있습니다.

# %% md

# 마지막에 Dense 층 추가하기

# 모델을 완성하려면 마지막 합성곱 층의 출력 텐서(크기 (4, 4, 64))를 하나 이상의 Dense 층에 주입하여 분류를 수행합니다.
# Dense 층은 벡터(1D)를 입력으로 받는데 현재 출력은 3D 텐서입니다.
# 먼저 3D 출력을 1D로 펼치겠습니다.
# 그다음 하나 이상의 Dense 층을 그 위에 추가하겠습니다.
# MNIST 데이터는 10개의 클래스가 있으므로 마지막에 Dense 층에 10개의 출력과 소프트맥스 활성화 함수를 사용합니다.

# %%

model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))

# 여기에서 볼 수 있듯이 두 개의 Dense 층을 통과하기 전에 (4, 4, 64) 출력을 (1024) 크기의 벡터로 펼쳤습니다.
model.summary()

# %% md

# 모델 컴파일과 훈련하기

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

train_history = model.fit(train_images, train_labels, epochs=5)

# %% Plot fitting result

print(train_history.history.keys())

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()

ax1.plot(train_history.history['accuracy'], 'g')
ax2.plot(train_history.history['loss'], 'r')

plt.title('saved_model accuracy & loss')
ax1.set_ylabel('accuracy')
ax2.set_ylabel('loss')

ax1.set_ylim(0.95, 1.0)
ax2.set_ylim(0.0, 0.1)

ax1.set_xlabel('epoch')
ax1.legend(['train'], loc='best')
ax2.legend(['loss'], loc='best')
plt.show()

# %% md

# 모델 평가
test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
print(test_acc)
