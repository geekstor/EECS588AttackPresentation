# import tensorflow as tf
# import math
#
# sess = tf.InteractiveSession()
#
# NUM_CHARS = 62
# CHAR_IMAGE_HEIGHT = 128
# CHAR_IMAGE_WIDTH = 16
# CHAR_IMAGE_SIZE = CHAR_IMAGE_HEIGHT * CHAR_IMAGE_WIDTH
#
# x = tf.placeholder(tf.float32, shape=[None, CHAR_IMAGE_SIZE], name="Img.")
# y_ = tf.placeholder(tf.float32, shape=[None, NUM_CHARS + 1], name="GNDTruth")
#
#
# W = tf.Variable(tf.zeros([CHAR_IMAGE_SIZE, NUM_CHARS], name="Weights"))
# b = tf.Variable(tf.zeros([NUM_CHARS]), name="Bias")
#
# def weight_variable(shape, name):
#     initial = tf.truncated_normal(shape, stddev = 0.1)
#     return tf.Variable(initial, name=name)
#
# def bias_variable(shape, name):
#     initial = tf.constant(0.1, shape=shape)
#     return tf.Variable(initial, name=name)
#
# W_conv1 = weight_variable([5, 5, 1, 32], "ConvLayer1Weights")
# b_conv1 = bias_variable([32], "ConvLayer1Bias")
#
# x_image = tf.reshape(x, [-1, int(math.sqrt(CHAR_IMAGE_SIZE)), int(math.sqrt(CHAR_IMAGE_SIZE)), 1], name="Reshape")
#
# def conv2d(x, W, name):
#     return tf.nn.conv2d(x, W,  strides=[1, 1, 1, 1], padding='SAME', name=name)
#
# def max_pool_2x2(x, name):
#     return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
#                         strides=[1, 2, 2, 1], padding='SAME', name=name)
#
# h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1, "ConvLayer1") + b_conv1, name="ReLULayer1")
# h_pool1 = max_pool_2x2(h_conv1, "MaxPoolLayer1")
#
# W_conv2 = weight_variable([5, 5, 32, 64], "ConvLayer2Weights")
# b_conv2 = bias_variable([64], "ConvLayer2Bias")
#
# h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2, "ConvLayer2") + b_conv2, name="ReLULayer2")
# h_pool2 = max_pool_2x2(h_conv2, "MaxPoolLayer2")
#
# W_fc1 = weight_variable([7 * 7 * 64, 1024], "FullyConnectedLayerWeights")
# b_fc1 = bias_variable([1024], "FullyConnectedLayerBias")
#
# h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64], "ReshapeForOutputLayer")
# h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1, "ReLUPre-OutputLayer")
#
#
#
# keep_prob = tf.placeholder(tf.float32, name="DropoutProbPlaceholder")
# h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob, name="FullyConnectedLayerDropout")
#
# W_fc2 = weight_variable([1024, NUM_CHARS], name="WeightsPostDropout")
# b_fc2 = bias_variable([NUM_CHARS], name="BiasPostDropout")
#
# y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2, name="OutputLayerSoftmax")
#
# sess.run(tf.initialize_all_variables())
#
# writer = tf.train.SummaryWriter("./Graph/", sess.graph_def)
# writer.flush()
# sess.close()

import tensorflow as tf
from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.

max_caption_len = 16
vocab_size = 10000

# first, let's define an image model that
# will encode pictures into 128-dimensional vectors.
# it should be initialized with pre-trained weights.
image_model = Sequential()
image_model.add(Convolution2D(32, 3, 3, border_mode='valid', input_shape=(3, 100, 100)))
image_model.add(Activation('relu'))
image_model.add(Convolution2D(32, 3, 3))
image_model.add(Activation('relu'))
image_model.add(MaxPooling2D(pool_size=(2, 2)))

image_model.add(Convolution2D(64, 3, 3, border_mode='valid'))
image_model.add(Activation('relu'))
image_model.add(Convolution2D(64, 3, 3))
image_model.add(Activation('relu'))
image_model.add(MaxPooling2D(pool_size=(2, 2)))

image_model.add(Flatten())
image_model.add(Dense(128))

# let's load the weights from a save file.
image_model.load_weights('weight_file.h5')

# next, let's define a RNN model that encodes sequences of words
# into sequences of 128-dimensional word vectors.
language_model = Sequential()
language_model.add(Embedding(vocab_size, 256, input_length=max_caption_len))
language_model.add(GRU(output_dim=128, return_sequences=True))
language_model.add(TimeDistributedDense(128))

# let's repeat the image vector to turn it into a sequence.
image_model.add(RepeatVector(max_caption_len))

# the output of both models will be tensors of shape (samples, max_caption_len, 128).
# let's concatenate these 2 vector sequences.
model = Merge([image_model, language_model], mode='concat', concat_axis=-1)
# let's encode this vector sequence into a single vector
model.add(GRU(256, 256, return_sequences=False))
# which will be used to compute a probability
# distribution over what the next word in the caption should be!
model.add(Dense(vocab_size))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

# "images" is a numpy float array of shape (nb_samples, nb_channels=3, width, height).
# "captions" is a numpy integer array of shape (nb_samples, max_caption_len)
# containing word index sequences representing partial captions.
# "next_words" is a numpy float array of shape (nb_samples, vocab_size)
# containing a categorical encoding (0s and 1s) of the next word in the corresponding
# partial caption.
model.fit([images, partial_captions], next_words, batch_size=16, nb_epoch=100)