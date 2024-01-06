import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Lambda, Dense, Flatten, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from glob import glob

# Re-size all the images to this
IMAGE_SIZE = [256, 256]

train_path = 'datasets/train'
valid_path = 'datasets/valid'  # Path to validation dataset
test_path = 'datasets/test'    # Path to test dataset

# Load InceptionV3 with pre-trained weights
inception = InceptionV3(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)

# Freeze the layers of InceptionV3
for layer in inception.layers:
    layer.trainable = False

# Add more Conv2D and MaxPooling2D layers
x = Conv2D(32, (3, 3), activation='relu', padding='same')(inception.output)
x = MaxPooling2D((2, 2))(x)

x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
x = MaxPooling2D((2, 2))(x)

x = Flatten()(x)
x = Dropout(0.5)(x)  # Add dropout layer to prevent overfitting
prediction = Dense(38, activation='softmax')(x)  # Replace 38 with the number of classes in your dataset
model = Model(inputs=inception.input, outputs=prediction)

# Compile the model
model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

# Set up data generators for training, validation, and test data
train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

valid_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

# Calculate total number of training and validation samples
total_train_samples = len(glob(train_path + '/*/*'))
total_valid_samples = len(glob(valid_path + '/*/*'))

# Adjust the batch size
batch_size = 32


training_set = train_datagen.flow_from_directory(
    train_path,
    target_size=(256, 256),
    batch_size=batch_size,
    class_mode='categorical'
)

validation_set = valid_datagen.flow_from_directory(
    valid_path,
    target_size=(256, 256),
    batch_size=batch_size,
    class_mode='categorical'
)

test_set = test_datagen.flow_from_directory(
    test_path,
    target_size=(256, 256),
    batch_size=batch_size,
    class_mode='categorical'
)

# Train the model with training and validation data
# r = model.fit(
#     training_set,
#     validation_data=validation_set,
#     epochs=20,  # Increase the number of epochs
#     steps_per_epoch=total_train_samples // batch_size,
#     validation_steps=total_valid_samples // batch_size
# )
r = model.fit_generator(
  training_set,
  validation_data=test_set,
  epochs=10,
  steps_per_epoch=len(training_set),
  validation_steps=len(test_set)
)

# Evaluate the model on the test data
test_loss, test_accuracy = model.evaluate(test_set, steps=len(test_set))
print("Test Loss:", test_loss)
print("Test Accuracy:", test_accuracy)

# Save the trained model
model.save('all_disease_model_optimized.h5')
