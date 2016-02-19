import os

path = 'captcha-images'

labeled_samples = {}
unlabeled_samples = {}

for possibledir in os.listdir(path):
    if not possibledir.startswith('.'):
        if os.path.isdir(os.path.join(path, possibledir)):
            contents_of_dir = [file for file in os.listdir(os.path.join(path, possibledir))]
            if "control.txt" in contents_of_dir:
                labeled_samples[possibledir] = [file for file in contents_of_dir if ".png" in file or ".jpeg" in file or ".jpg" in file]
            else:
                unlabeled_samples[possibledir] = [file for file in contents_of_dir if ".png" in file or ".jpeg" in file or ".jpg" in file]


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

# For displaying captcha

# import matplotlib
# matplotlib.use('macosx')
# import matplotlib.pyplot as plt
# plt.imshow(labeled_samples['xanga'][72][0])
# print labeled_samples['xanga'][72][1]
# plt.show()


