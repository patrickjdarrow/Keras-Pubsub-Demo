# ADAPTED FROM https://keras.io/applications/#inceptionv3

from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing import image
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras import backend as K
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import SGD

# create the base pre-trained model
base_model = InceptionV3(weights='imagenet',
						include_top=False,
						input_shape=(299,299,3))

# add a global spatial average pooling layer
x = base_model.output
x = GlobalAveragePooling2D()(x)
# let's add a fully-connected layer
x = Dense(1024, activation='relu')(x)
# and a logistic layer -- let's say we have 200 classes
predictions = Dense(2, activation='softmax')(x)

# this is the model we will train
model = Model(inputs=base_model.input, outputs=predictions)

# we use SGD with a low learning rate
model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss='categorical_crossentropy')
model.summary()

# we train our model again (this time fine-tuning the top 2 inception blocks
# alongside the top Dense layers
bs = 32

train_datagen = ImageDataGenerator(rescale=1./255,
        					horizontal_flip=True)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = test_datagen.flow_from_directory(
								'data/train',
								target_size=(299,299),
								batch_size=bs,)

validation_generator = test_datagen.flow_from_directory(
								'data/test',
								target_size=(299,299),
								batch_size=bs,)

model.fit_generator(train_generator,
					steps_per_epoch=int(1500/bs),
					epochs=50,
					validation_data=validation_generator,
					validation_steps=int(150/bs),
					max_queue_size=bs,
					workers=2,
					use_multiprocessing=True)