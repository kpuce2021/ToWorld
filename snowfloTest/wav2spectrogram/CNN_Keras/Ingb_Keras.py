import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator

# 랜덤시드 고정시키기
np.random.seed(3)

train_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
        'warehouse/data/train',
        target_size=(50, 50),
        batch_size=3,
        class_mode='categorical')

test_datagen = ImageDataGenerator(rescale=1./255)
test_generator = test_datagen.flow_from_directory(
        'warehouse/data/test',
        target_size=(50, 50),
        batch_size=3,
        class_mode='categorical')

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(50,50,3)))
#  필터 수, 필터 크기, 패딩 옵션, 활성화 함수, input_shape(가로,세로,채널)
#  필터 크기 : 3 * 3 = 필터당 학습할 weight의 수 -> 총 학습할 weight의 수 = 32 * 3 * 3
#  Dense : 이전 계층의 모든 뉴런과 결합한 형태, full-connected, dense layer
#  feature map : 출력 수, 필터 수 -> "출력 피처 맵의 수는, 필터에 영향을 미친다."
#  padding = same -> 크기 동일, valid -> 크기 감소
'''
123 가 있다면
456 12 23 이런식으로 하기 때문에 
789 45 56 나머지 36978, 14789는 영향을 미치지 않는다. -> 지역적 요소가 있다.
'''
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
#  Pooling : 축소 -> MaxPooling : 큰 것만 축소 // 학습 X
model.add(Flatten())
#  3차원 -> 1차원 : 분류 문제를 풀기 위해서는 결국 나눠야 함
model.add(Dense(128, activation='relu'))
model.add(Dense(3, activation='softmax'))

from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot
#  import pydot

SVG(model_to_dot(model, show_shapes=True).create(prog='dot', format='svg'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# model.summary()

model.fit_generator(
        train_generator,
        steps_per_epoch=119,
        epochs=10,
        validation_data=test_generator,
        validation_steps=20)

# 첫번째 인자 : 훈련데이터셋을 제공할 제네레이터를 지정합니다. 본 예제에서는 앞서 생성한 train_generator으로 지정합니다.
# steps_per_epoch : 한 epoch에 사용한 스텝 수를 지정합니다. 총 45개의 훈련 샘플이 있고 배치사이즈가 3이므로 15 스텝으로 지정합니다.
# epochs : 전체 훈련 데이터셋에 대해 학습 반복 횟수를 지정합니다. 100번을 반복적으로 학습시켜 보겠습니다.
# validation_data : 검증데이터셋을 제공할 제네레이터를 지정합니다. 본 예제에서는 앞서 생성한 validation_generator으로 지정합니다.
# validation_steps : 한 epoch 종료 시 마다 검증할 때 사용되는 검증 스텝 수를 지정합니다. 홍 15개의 검증 샘플이 있고 배치사이즈가 3이므로 5 스텝으로 지정합니다.

# 5. 모델 평가하기
print("-- Evaluate --")
scores = model.evaluate_generator(test_generator, steps=5)
print("%s: %.2f%%" %(model.metrics_names[1], scores[1]*100))

# 6. 모델 사용하기
print("-- Predict --")
output = model.predict_generator(test_generator, steps=5)
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)}) # 이건 소수점 3자리로 나오게 바꿔 주는 것
print(test_generator.class_indices) # {'g': 0, 'o': 1, 't': 2}
print(output)
