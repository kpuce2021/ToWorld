# import tensorflow as tf
from tensorflow import keras

import numpy as np
import matplotlib.pyplot as plt

mnist = keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# %% show sample image data
plt.rcParams['toolbar'] = 'None'

fg1 = plt.figure(1, figsize=(3, 3))
# fg1.canvas.window().statusBar().setVisible(False)
ax1 = fg1.add_axes([0, 0, 1, 1])
ax1.imshow(train_images[0], cmap='gray', aspect='auto')
ax1.axis('off')
ax1.text(1, 1, "Label : {}".format(train_labels[0]), fontsize=10, color='white')

fg2 = plt.figure(2, figsize=(3, 3))
# fg2.canvas.window().statusBar().setVisible(False)
ax2 = fg2.add_axes([0, 0, 1, 1])
ax2.imshow(test_images[0], cmap='gray', aspect='auto')
ax2.axis('off')
ax2.text(1, 1, "Label : {}".format(test_labels[0]), fontsize=10, color='white')

# %% normalize
train_input = train_images / 255.0
test_input = test_images / 255.0

# %% target to one-hot vector
train_target = keras.utils.to_categorical(train_labels)
test_target = keras.utils.to_categorical(test_labels)

# def mycategorical(test_labels):
#     arr = np.zeros(test_labels.length, 10)
#     for label in test_labels:
#         arr[label] = 1.0


# %% define network
model = keras.Sequential(
    layers=[
        keras.layers.Flatten(input_shape=(28, 28), name='Input'),  # input
        keras.layers.Dense(128, activation='relu', name='Hidden_1'),  # hidden 1
        keras.layers.Dropout(0.5),
        keras.layers.Dense(128, activation='relu', name='Hidden_2'),  # hidden 2
        keras.layers.Dropout(0.5),
        keras.layers.Dense(128, activation='relu', name='Hidden_3'),  # hidden 3
        keras.layers.Dropout(0.5),
        keras.layers.Dense(10, activation='relu', name='Output')  # output
    ],
    name="MNIST_Classifier"
)
model.summary()

model.compile(optimizer=keras.optimizers.Adam(lr=0.001),
              loss='mean_squared_error',
              metrics=['accuracy'])
# model.compile(optimizer=keras.optimizers.SGD(lr=0.2),
#               loss='mean_squared_error',
#               metrics=['accuracy'])

# %% Tensorboard
import datetime

log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

# %% fit model to train data
# model.fit(train_input, train_target, epochs=20, verbose=2)
# model.fit(train_input, train_target, epochs=20, batch_size=32, verbose=2)
train_history = model.fit(train_input, train_target,
                          epochs=20, batch_size=32,
                          callbacks=[tensorboard_callback])

# %% Plot fitting result
print(train_history.history.keys())

plt.plot(train_history.history['accuracy'], 'g')
# plt.plot(train_history.history['loss'], 'r')

plt.ylim(0.9, 1.0)

plt.title('model accuracy & loss')
plt.ylabel('accuracy & loss')
plt.xlabel('epoch')
plt.legend(['train'], loc='upper left')
plt.show()

# %% evaluate model by test data
test_loss, test_acc = model.evaluate(test_input, test_target, verbose=2)
print('\nTest accuracy:', test_acc)

predictions = model.predict(test_input)

# %% show sample data prediction
sample_idx = np.random.randint(0, 9999)
test_sample = test_input[sample_idx].reshape([1, 28, 28])
test_sample_label = test_labels[sample_idx]

fg3 = plt.figure(4, figsize=(3, 3))
# fg3.canvas.window().statusBar().setVisible(False)
ax3 = fg3.add_axes([0, 0, 1, 1])
ax3.cla()
ax3.imshow(test_input[sample_idx], cmap='gray', aspect='auto')
ax3.axis('off')

sample_pred = model.predict(test_sample)
sample_result = np.argmax(sample_pred)

ax3.text(0.5, 2.5, "Label : {}".format(test_sample_label), fontsize=20, color='white')
ax3.text(0.5, 5.5, "Prediction : {}".format(sample_result), fontsize=20, color='red')

# fg3.canvas.manager.window.raise_()