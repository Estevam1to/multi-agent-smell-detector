# https://github.com/eugeniaring/Medium-Articles/blob/main/Pytorch/denAE.ipynb

import matplotlib.pyplot as plt
import numpy as np # this module is useful to work with numerical arrays
import random # this module will be used to select random samples from a collection
import torch
import torchvision
from torchvision import transforms
from torch.utils.data import random_split
from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics import accuracy_score


data_dir = 'dataset'
### With these commands the train and test datasets, respectively, are downloaded
### automatically and stored in the local "data_dir" directory.
train_dataset = torchvision.datasets.MNIST(data_dir, train=True, download=True)


train_transform = transforms.Compose([
    transforms.ToTensor(),
])

# Set the train transform
train_dataset.transform = train_transform

m=len(train_dataset)

#random_split randomly split a dataset into non-overlapping new datasets of given lengths
#train (48,000 images), val split (5,000 images)
train_data, val_data = random_split(train_dataset, [int(m-m*0.2), int(m*0.2)])

batch_size=256

# The dataloaders handle shuffling, batching, etc...
train_loader = torch.utils.data.DataLoader(train_data, batch_size=batch_size)
valid_loader = torch.utils.data.DataLoader(val_data, batch_size=batch_size)

count = 9
randomly_selected_val_imgs = [random.randint(0,len(val_data)) for i in range(count)]


# put your image generator here
def generate_images() -> tuple:
    unsqueezed_images = []
    og_squeezed_images = []

    for i in range(count):
        og_squeezed_images.append([val_data[randomly_selected_val_imgs[i]][0]])
        img = val_data[randomly_selected_val_imgs[i]][0].unsqueeze(0)
        unsqueezed_images.append(img)
        ax = plt.subplot(3, 3, i+1)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)  
        plt.imshow(img.cpu().squeeze().numpy(), cmap='gist_gray')  
        plt.axis('off')
    plt.show()
    actual_labels = [val_data[randomly_selected_val_imgs[i]][1] for i in range(count)]
    return (unsqueezed_images, og_squeezed_images, actual_labels)

unsqueezed_images, og_squeezed_images, actual_labels = generate_images()

# put your clustering accuracy calculation here

# derived from both online examples of MNIST kmeans clustering 
# combined with github copilot suggestions
def retrieve_info(cluster_labels, actual_labels):
    ref_labels = {}
    for i in range(len(np.unique(kmeans.labels_))):
        index = np.where(cluster_labels == i, 1, 0)
        num = np.bincount(actual_labels[index == 1]).argmax()
        ref_labels[i] = num
    return ref_labels

# we must cluster all 48000 images

def run_kmeans(X_train, y_train, num_clusters):

    total_cluster = num_clusters
    # total_cluster = len(np.unique(y_train)) # should be 10
    kmeans = MiniBatchKMeans(n_clusters=total_cluster, random_state=0)
    kmeans.fit(X_train)
    # kmeans = kmeans.predict(X_train)
    kmeans.labels_


    # ref_labels = retrieve_info(kmeans.labels_, y_train)

    ref_labels = {}
    for i in range(len(np.unique(kmeans.labels_))):
        index = np.where(kmeans.labels_ == i, 1, 0)
        num = np.bincount(y_train[index == 1]).argmax()
        ref_labels[i] = num

    number_labels = np.random.rand(len(kmeans.labels_))
    # github copilot suggestion
    for i in range(len(kmeans.labels_)):
        number_labels[i] = ref_labels[kmeans.labels_[i]]

    predicted_labels = number_labels[:count].astype(int)
    print('Using {} clusters'.format(total_cluster))
    print('Predicted labels: ', predicted_labels)
    print('Actual labels: ', actual_labels)
    print('Accuracy: ', accuracy_score(actual_labels, predicted_labels))

# After spending a day attempting, I was not able to correctly shape and reshape 
# the mnist data coming from torch to appropriately work with sklean.KMeans.  
# Given that the assignment asks us to focus on the accuracy of predictions, in 
# the interest of time I decided to import the same MNIST data using Keras.
from keras.datasets import mnist as kmnist

(X_train, y_train), (X_test, y_test) = kmnist.load_data()
# X_train, X_val = random_split(X_train, [int(m-m*0.2), int(m*0.2)])
# X_val = X_train[48000:]
# X_train = X_train[:48000]
 # normalize X to be between 0 and 1
X_train = X_train.astype('float32') / 255.
X_train = X_train.reshape((len(X_train), -1))

num_clusters = [10, 20, 40, 80, 160]
for i in num_clusters:
    run_kmeans(X_train, y_train, i)

# EOF 
