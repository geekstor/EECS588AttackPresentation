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

import Main

import tensorflow as tf

from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Activation
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Merge
from keras.layers import TimeDistributedDense
from keras.layers import Embedding
from keras.layers import GRU
from keras.layers import RepeatVector
from keras.layers import GaussianNoise
from keras.layers import BatchNormalization
from keras.layers import containers
from keras.layers import AutoEncoder
from keras.optimizers import Adagrad
from keras.models import model_from_json

# first, let's define an image model that
# will encode pictures into 128-dimensional vectors.
# it should be initialized with pre-trained weights.
# ae_model = Sequential()
# ae_model.add(GaussianNoise(sigma=0.05, batch_input_shape=(100, 2048*3)))
# ae_model.add(BatchNormalization())
# encoder = containers.Sequential([Dense(input_dim=2048*3, output_dim=1024*3, activation='sigmoid'), BatchNormalization(), Dense(input_dim=1024*3, output_dim=512*3, activation='sigmoid'), BatchNormalization()])
# decoder = containers.Sequential([Dense(input_dim=512*3, output_dim=1024*3, activation='sigmoid'), BatchNormalization(), Dense(input_dim=1024*3, output_dim=2048*3, activation='sigmoid')])
# ae_model.add(AutoEncoder(encoder=encoder, decoder=decoder, output_reconstruction=True))
# let's load the weights from a save file.

ae_model = model_from_json(open('./Graph/dAE_arch.json').read())
ae_model.load_weights('./Graph/dAE_weights.h5')

# next, let's define a RNN model that encodes sequences of words
# into sequences of 128-dimensional word vectors.
language_model = Sequential()
language_model.add(Embedding(Main.vocab_size, 128, input_length=Main.max_caption_len, batch_input_shape=(5, Main.vocab_size)))
language_model.add(GRU(output_dim=128*3, return_sequences=True))
language_model.add(TimeDistributedDense(512*3))

# let's repeat the image vector to turn it into a sequence.
ae_model.add(RepeatVector(Main.max_caption_len))

# the output of both models will be tensors of shape (samples, max_caption_len, 128).
# let's concatenate these 2 vector sequences.
model = Sequential()
model.add(Merge([ae_model, language_model], mode='concat', concat_axis=-1))
# let's encode this vector sequence into a single vector
model.add(GRU(output_dim=256, input_dim=256, return_sequences=False))
# which will be used to compute a probability
# distribution over what the next word in the caption should be!
model.add(Dense(output_dim=Main.vocab_size))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='rmsprop')



# model.fit([images, partial_captions], next_words, batch_size=16, nb_epoch=100)

from keras.callbacks import TensorBoard
from keras.callbacks import EarlyStopping
model.fit([Main.get_batch(5, partial_answer=True)[0], Main.get_batch(5, partial_answer=True)[1]],
             Main.get_batch(5, True, True)[2], nb_epoch=20000, verbose=1, batch_size=5,
             show_accuracy=True, shuffle=True, #validation_data=Main.get_test_batch(5),
             callbacks=[TensorBoard(log_dir='./Graph', histogram_freq=0),
             EarlyStopping(verbose=True, monitor='val_loss', patience=50)])