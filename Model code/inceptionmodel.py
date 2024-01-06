



from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.applications.inception_v3 import InceptionV3



from tensorflow.keras.preprocessing.image import ImageDataGenerator
from glob import glob



# re-size all the images to this
IMAGE_SIZE = [224, 224]

train_path = 'dataset/train'
valid_path = 'dataset/test'



inception = InceptionV3(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)


for layer in inception.layers:
    layer.trainable = False
    
    
# When we create the inception model using InceptionV3, it contains multiple layers, including convolutional layers, pooling layers, fully connected layers, etc. During the training process, these layers' weights are updated to learn from the data and improve the model's performance on the specific task.By setting layer.trainable = False, we are freezing the layers of the InceptionV3 model, making them non-trainable or untrainable. 
folders = glob('dataset/train/*')

x = Flatten()(inception.output)
# 4 D tensor ne 2D tensor ma convert kare 
prediction = Dense(4, activation='softmax')(x)

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



training_set = train_datagen.flow_from_directory('dataset/train',
                                                 target_size = (224, 224),
                                                 batch_size = 32,
                                                 class_mode = 'categorical')


test_set = test_datagen.flow_from_directory('dataset/test',
                                            target_size = (224, 224),
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
    epochs=20,
    steps_per_epoch=len(training_set),
    validation_steps=len(test_set)
)





model.save('model_inception.h5')