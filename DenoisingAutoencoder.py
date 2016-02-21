from keras.models import Sequential
from keras.layers.core import AutoEncoder
from keras.layers import Dense
from keras.layers import GaussianNoise
from keras.optimizers import Adagrad
from keras.callbacks import TensorBoard
from keras.layers import BatchNormalization
from keras.callbacks import EarlyStopping
from keras.layers import Activation

ae_model = Sequential()
ae_model.add(GaussianNoise(sigma=0.05, batch_input_shape=(5, 2048*3)))
ae_model.add(BatchNormalization())

ae_model.add(Dense(input_dim=2048*3, output_dim=1024*3))
ae_model.add(BatchNormalization())
ae_model.add(Activation('sigmoid'))
ae_model.add(Dense(input_dim=1024*3, output_dim=512*3))
ae_model.add(BatchNormalization())
ae_model.add(Activation('sigmoid'))

ae_model.add(Dense(input_dim=512*3, output_dim=1024*3))
ae_model.add(BatchNormalization())
ae_model.add(Activation('sigmoid'))
ae_model.add(Dense(input_dim=1024*3, output_dim=2048*3))

# encoder = containers.Sequential([Dense(input_dim=2048*3, output_dim=1024*3, activation='sigmoid'), Dense(input_dim=1024*3, output_dim=512*3, activation='sigmoid')])
# decoder = containers.Sequential([Dense(input_dim=512*3, output_dim=1024*3, activation='sigmoid'), Dense(input_dim=1024*3, output_dim=2048*3, activation='sigmoid')])
ae_model.compile(loss='mean_squared_error', optimizer=Adagrad(lr=0.2))

import Main

# for i in range(10000):
#    print("Iter " + str(i) + " :" + str(ae_model.train_on_batch(X=Main.get_batch()[0], y = Main.get_batch()[0], accuracy=True)))
# ae_model.fit_generator(Main.get_sample(), samples_per_epoch=100, nb_epoch=1000, show_accuracy=True, callbacks=[TensorBoard(log_dir='./Graph', histogram_freq=0)], nb_worker=1)

ae_model.fit(Main.get_batch(5)[0], Main.get_batch(5, step=True)[0], nb_epoch=20000, verbose=1, batch_size=5,
             show_accuracy=True, shuffle=True, validation_data=Main.get_test_batch(5),
             callbacks=[TensorBoard(log_dir='./Graph', histogram_freq=0),
             EarlyStopping(verbose=True, monitor='val_loss', patience=50)])

json_string = ae_model.to_json()
open('./Graph/dAE_arch.json', 'w').write(json_string)
ae_model.save_weights(filepath='./Graph/dAE_weights.h5', overwrite=True)