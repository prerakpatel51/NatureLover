import tensorflow
from tensorflow.compat.v1 import ConfigProto


# import the libraries as shown below

from tensorflow.keras.layers import Input, Lambda, Dense, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.applications.inception_v3 import InceptionV3
#from keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator,load_img
from tensorflow.keras.models import Sequential
import numpy as np
from glob import glob
#import matplotlib.pyplot as plt



# re-size all the images to this
IMAGE_SIZE = [256, 256]

train_path = 'datasets/train'
valid_path = 'datasets/test'



inception = InceptionV3(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)


for layer in inception.layers:
    layer.trainable = False
    
folders = glob('datasets/train/*')

x = Flatten()(inception.output)
# prediction = Dense(len(folders), activation='softmax')(x)
# Replace `len(folders)` with the number of classes in your dataset (5 in this case)
prediction = Dense(38, activation='softmax')(x)

# create a model object
model = Model(inputs=inception.input, outputs=prediction)


# view the structure of the model
model.compile(
  loss='categorical_crossentropy',
  optimizer='adam',
  metrics=['accuracy']
)


from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)



training_set = train_datagen.flow_from_directory('datasets/train',
                                                 target_size = (256, 256),
                                                 batch_size = 32,
                                                 class_mode = 'categorical')


test_set = test_datagen.flow_from_directory('datasets/test',
                                            target_size = (256, 256),
                                            batch_size = 32,
                                            class_mode = 'categorical')


# fit the model
# Run the cell. It will take some time to execute
# r = model.fit_generator(
#   training_set,
#   validation_data=test_set,
#   epochs=20,
#   steps_per_epoch=len(training_set),
#   validation_steps=len(test_set)
# )


r = model.fit(
    training_set,
    validation_data=test_set,
    epochs=8,
    steps_per_epoch=len(training_set),
    validation_steps=len(test_set)
)



from tensorflow.keras.models import load_model

model.save('all_disease_model.h5')