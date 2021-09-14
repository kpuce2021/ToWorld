# # 사용할 모듈 정의
from PIL import Image
import tensorflow as tf
from keras import layers, Input
import pathlib
from tensorflow.keras.models import Sequential
from keras.models import Model, load_model
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Dense

def convolution(email):
    # 새로 학습할 데이터가 있는 디렉토리
    new_data_dir='temp/'+ email +'/data'
    batch_size = 32
    split_percent=0.3
    rand_seed=123
    shuffle_num=1000
    EPOCHS=150
    # 모델 세이브
    save_model_name='temp/'+email+'/model/model.h5'
    

    # .png 형식의 데이터 인식
    data_dir = pathlib.Path(new_data_dir)
    image_list = list(data_dir.glob('*/*.png'))
    image_size = Image.open(image_list[0]).size
    img_width=image_size[0]
    img_height=image_size[1]

    # train data set
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=split_percent,
        subset="training",
        seed=rand_seed,
        image_size=(img_height, img_width),
        batch_size=batch_size)

    # test data set
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=split_percent ,
        subset="validation",
        seed=rand_seed,
        image_size=(img_height, img_width),
        batch_size=batch_size)

    # data preprocessing
    class_names = train_ds.class_names
    num_classes = len(class_names)
    AUTOTUNE = tf.data.experimental.AUTOTUNE
    train_ds = train_ds.cache().shuffle(shuffle_num).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
    normalization_layer = layers.experimental.preprocessing.Rescaling(1./255)
    normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
    image_batch, labels_batch = next(iter(normalized_ds))

    load_model_name='temp/' + email + '/model/model.h5'

    test_h5 = load_model(load_model_name)

    for layer in test_h5.layers[:-1]:
        layer.trainable = False
        
    maintain_class_layer = test_h5.layers[-1]

    diff = test_h5.layers[-1].get_weights()[1].shape[0] - num_classes
    if (diff!=0):
        add_class_layer = test_h5.layers[-2].output
        add_class_layer = Dense(num_classes, activation='softmax')(add_class_layer)
        transfer_model = Model(test_h5.input, outputs=add_class_layer)
        
        weights_bak = test_h5.layers[-1].get_weights()
 
        weights_new = transfer_model.layers[-1].get_weights()
   
        weights_new[0][:, :diff] = weights_bak[0]
        weights_new[1][:diff] = weights_bak[1]
        transfer_model.layers[-1].set_weights(weights_new)
        
    else:
        transfer_model = Model(test_h5.input, maintain_class_layer(test_h5.layers[-2].output))

    transfer_model.compile(optimizer='adam',
                loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                metrics=['accuracy'])

    history = transfer_model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS,
    )
    
    transfer_model.save(save_model_name)