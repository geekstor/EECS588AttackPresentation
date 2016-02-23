import os

path = 'captcha-images'

vocab_size = 62 + 1
max_caption_len = 10

labeled_samples = {}
unlabeled_samples = {}

for possibledir in os.listdir(path):
    if not possibledir.startswith('.'):
        if os.path.isdir(os.path.join(path, possibledir)):
            contents_of_dir = [file for file in os.listdir(os.path.join(path, possibledir))]
            if "control.txt" in contents_of_dir:
                labeled_samples[possibledir] = [file for file in contents_of_dir if ".png" in file or ".jpeg" in file or ".jpg" in file or ".gif" in file]
            else:
                unlabeled_samples[possibledir] = [file for file in contents_of_dir if ".png" in file or ".jpeg" in file or ".jpg" in file or ".gif" in file]


for k, v in labeled_samples.items():
    f = open(path + "/" + k + "/control.txt")
    answers = f.readlines()
    answers = [answer.replace("\n", "") for answer in answers]
    labeled_samples[k] = zip(labeled_samples[k], answers)

from scipy import misc
from scipy.ndimage import imread

for k in labeled_samples:
    for i in range(len(list(labeled_samples[k]))):
        labeled_samples[k][i] = tuple([misc.imresize(imread(path + "/" + k + "/" + labeled_samples[k][i][0], mode='RGB'),
                                        size=(128, 16)).flatten()/float(256.0),
                                        labeled_samples[k][i][1]])

for k in unlabeled_samples:
    for i in range(len(list(unlabeled_samples[k]))):
        unlabeled_samples[k][i] = misc.imresize(imread(path + "/" + k + "/" + unlabeled_samples[k][i], mode='RGB'),
                                size=(128, 16)).flatten()/float(256.0)

# For displaying captcha

# import matplotlib
# matplotlib.use('macosx')
# import matplotlib.pyplot as plt
# plt.imshow(labeled_samples['xanga'][72][0])
# print labeled_samples['xanga'][72][1]
# plt.show()

import numpy
import random
import sys
import string

rand_seed_value = 0

mapping = {}

idx = 0
for c in string.digits:
    mapping[c] = ord(c) - 48

idx += len(string.digits)

for c in string.uppercase:
    mapping[c] = ord(c) - 65 + idx

idx += len(string.uppercase)

for c in string.ascii_lowercase:
    mapping[c] = ord(c) - 97 + idx


def get_batch(size, partial_answer=False, step=False):
    img_list = []
    answer_list = []
    partial_answer_list = []
    rest_answer_list = []
    global rand_seed_value
    random.seed(rand_seed_value)
    for i in range(size):
        rand_key = labeled_samples.keys()[random.randint(0, len(labeled_samples)) - 1]
        rand_ind = random.randint(0, len(list(labeled_samples[rand_key])) - 1)
        img_list.append(labeled_samples[rand_key][rand_ind][0])
        if not partial_answer:
            answer_list.append(labeled_samples[rand_key][rand_ind][1])
        else:
            rand_end_char = random.randint(0, len(labeled_samples[rand_key][rand_ind][1]) - 1)
            partial_answer_t = [len(mapping.keys())] * (max_caption_len - rand_end_char)
            partial_answer_t = partial_answer_t + [mapping[c]
                                        for c in labeled_samples[rand_key][rand_ind][1][:rand_end_char]]
            partial_answer_list.append(partial_answer_t)
            rest_answer_list.append(numpy.eye(vocab_size)[mapping[labeled_samples[rand_key][rand_ind][1][rand_end_char]]])

    if step:
        rand_seed_value = random.randint(0, sys.maxint)

    if not partial_answer:
        return [numpy.array(img_list, dtype=float), answer_list]
    else:
        return [numpy.array(img_list, dtype=float), numpy.array(partial_answer_list), numpy.array(rest_answer_list)]

def get_test_batch(size):
    img_list = []
    for i in range(size):
        rand_key = unlabeled_samples.keys()[numpy.random.randint(low=0, high=len(unlabeled_samples))]
        rand_ind = numpy.random.randint(low=0, high=len(list(unlabeled_samples[rand_key])))
        img_list.append(unlabeled_samples[rand_key][rand_ind])
    return numpy.array(img_list, dtype=float), numpy.array(img_list, dtype=float)
#
# def get_sample():
#     global labeled_samples
#     labeled_samples = labeled_samples
#     while True:
#         rand_key = labeled_samples.keys()[numpy.random.randint(low=0, high=len(labeled_samples))]
#         rand_ind = numpy.random.randint(low=0, high=len(list(labeled_samples[rand_key])))
#         yield numpy.array(labeled_samples[rand_key][rand_ind][0]).reshape(1, 2048*3), numpy.array(labeled_samples[rand_key][rand_ind][0]).reshape(1, 2048*3)