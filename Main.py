import os

path = 'captcha-images'

labeled_samples = {}
unlabeled_samples = {}

for possibledir in os.listdir(path):
    if not possibledir.startswith('.'):
        if os.path.isdir(os.path.join(path, possibledir)):
            contents_of_dir = [file for file in os.listdir(os.path.join(path, possibledir))]
            if "control.txt" in contents_of_dir:
                labeled_samples[possibledir] = [file for file in contents_of_dir if ".gif" in file or ".png" in file or ".jpeg" in file or ".jpg" in file]
            else:
                unlabeled_samples[possibledir] = [file for file in contents_of_dir if ".gif" in file or ".png" in file or ".jpeg" in file or ".jpg" in file]


print(labeled_samples)

for k, v in labeled_samples.items():
    f = open(path + "/" + k + "/control.txt")
    answers = f.readlines()
    answers = [answer.replace("\n", "") for answer in answers]
    labeled_samples[k] = zip(labeled_samples[k], answers)

from scipy import misc

for k in labeled_samples:
    for i in range(len(list(labeled_samples[k]))):
        labeled_samples[k][i] = tuple([misc.imread(path + "/" + k + "/" + labeled_samples[k][i][0]),
                                        labeled_samples[k][i][1]])


# Generate training examples from key if provided, otherwise pick randomly among keys
from random import randint
def get_train_batch(batch_size, key = None):
    keys = []
    images = []
    answers = []

    key_names = labeled_samples.keys()
    
    if key == None or key not in key_names:
        num_keys = len(labeled_samples)

        for i in range(0, batch_size):
            key = key_names[randint(0, num_keys-1)]
            keys.append(key)
            num_images = len(labeled_samples[key])

            image_ind = randint(0, num_images-1)
            image = labeled_samples[key][image_ind]
            images.append(image[0])
            answers.append(image[1])
    else:
        num_images = len(labeled_samples[key])
        for i in range(0, batch_size):
            keys.append(key)
            image_ind = randint(0, num_images-1)
            image = labeled_samples[key][image_ind]
            images.append(image[0])
            answers.append(image[1])

    return (keys, images, answers)
keys, images, answers = get_train_batch(50)

# unsure what exactly you wanted to be different about test batch, right now just
# returning images without answers
def get_test_batch(batch_size, key = None):
    keys, images, answers = get_train_batch(batch_size)
    return (keys, images)




# For displaying captcha

# import matplotlib
# matplotlib.use('macosx')
# import matplotlib.pyplot as plt
# plt.imshow(labeled_samples['xanga'][72][0])
# print labeled_samples['xanga'][72][1]
# plt.show()


