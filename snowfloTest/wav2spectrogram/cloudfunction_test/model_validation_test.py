import cv2
import tensorflow as tf
from tensorflow.python.keras.models import load_model
import numpy as np

# ['good_morning', 'how_working_path', 'tomorrow_weather']

check_model = load_model("model/model3.h5")

main_img = cv2.imread('D:/#2021_CAPSTONE/GitToworld/snowfloTest/wav2spectrogram/cloudfunction_test/test_remove_noise/android_denoise.png')
main_img = cv2.cvtColor(main_img, cv2.COLOR_BGR2RGB)
np.array(main_img, dtype='uint8')
images = tf.expand_dims(main_img, 0)

prediction = check_model.predict([images])

if np.argmax(prediction, axis=1) == [0]:
    print("굿모닝")
elif np.argmax(prediction, axis=1) == [1]:
    print("출근길 교통 상황 어때")
else:
    print("내일 날씨 어때")

# good_morning: oxooo
# tomorrow_weather: ooooo
# how_working_path: ooooo

