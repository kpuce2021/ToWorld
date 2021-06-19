import pandas as pd
import tensorflow as tf

tf.debugging.set_log_device_placement(True)  # gpu 사용 확인
# print(tf.__version__)

from tensorflow import keras
print(keras.__version__)  # tensorflow version

from tensorflow.python.client import device_lib
print(device_lib.list_local_devices())  # tensorflow device

a = tf.constant([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
b = tf.constant([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
c = tf.matmul(a, b)

# print(c)