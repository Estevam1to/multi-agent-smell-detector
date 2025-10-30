# Author: Carter Allen
# Date: 1/8/2022
# Description: A library to represent sklearn-images and common image operations using Image objects.
# 
# Purpose:
# 1. To practice object-oriented programming in Python.
# 2. To practice using the skimage library.
# 3. To practice using Github Copilot (a lot of this code was created with the help of Copilot).

import skimage
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
import os


def plot_image(image, cmap=plt.rcParams["image.cmap"]):
    """
    Plot the image using matplotlib.
    """
    plt.figure(figsize=(8, 8))
    plt.imshow(image, cmap=cmap)
    plt.axis('off')
    plt.show()


def new_image_from_array(image):
    """
    Create a new image from a file path.

    @param image: numpy array representing the image
    @return: Image object
    """
    if image.shape[2] == 1:
        return Image(image)
    elif image.shape[2] == 3:
        return RGB_Image(image)
    else:
        print("Warning: Image has undefined number of channels (not 1 or 3). Returning Image object.")
        return Image(image)


def new_image_from_file(file_path):
    """
    Create a new image from a file path.

    @param file_path: path to the image file
    @return: Image object
    """
    image = skimage.io.imread(file_path)
    return new_image_from_array(image)


class Image:
    """
    A class to represent an image.
    """

    def __init__(self, array):
        """
        Create an Image object from a numpy array.

        @param array: numpy array representing the image
        """
        self.image = array

    def __str__(self):
        """
        Return a string representation of the image.
        """
        return f"Image: {self.image.shape}"

    def __repr__(self):
        """
        Return a string representation of the image.
        """
        return self.__str__()

    @classmethod
    def from_file(cls, file_path):
        """
        Create an Image object from a file path.

        @param file_path: path to the image file
        @return: Image object
        """
        return cls(skimage.io.imread(file_path))

    def show(self):
        """
        Show the image using matplotlib.
        """
        plot_image(self.image, cmap=plt.cm.gray)  # if RGB, colormap is ignored

    def save(self, file_path):
        """
        Save the image to a file.

        @param file_path: path to save the image to
        """
        skimage.io.imsave(file_path, self.image)

    def x_max(self):
        """
        Return the maximum x index.
        """
        return self.image.shape[1] - 1

    def y_max(self):
        """
        Return the maximum y index.
        """
        return self.image.shape[0] - 1

    def x_mid(self):
        """
        @return: midpoint x index
        """
        return self.x_max() // 2

    def y_mid(self):
        """
        @return: midpoint y index
        """
        return self.y_max() // 2

    def as_binary(self, threshold=0.5):
        """
        Return the image as a binary image.

        @param threshold: threshold to use for binarizing the image
        @return: binary image
        """
        return Image(self.image > threshold)
        
    def rotate(self, angle):
        """
        Rotate the image by the given angle.

        @param angle: angle to rotate the image by
        @return: rotated image
        """
        rotated = ndi.rotate(self.image, angle)
        return Image(rotated)

    def contours(self, level):
        """
        Find contours in the image.
        """
        return skimage.measure.find_contours(self, level)

    def active_contours(
        self, init, alpha=0.015, beta=10, gamma=0.001, w_line=0, w_edge=1,
        max_px_move=1.0, max_num_iter=2500, convergence=0.1, coordinates='rc'
    ):
        """
        Perform active contours on the image. 
        TODO: need to figure out how this works at all
        """
        return skimage.segmentation.active_contour(
            self.image, init, alpha=alpha, beta=beta, gamma=gamma, 
            w_line=w_line, w_edge=w_edge, max_px_move=max_px_move, 
            max_num_iter=max_num_iter, convergence=convergence, coordinates=coordinates
        )

    def plot_histogram(self):
        """
        Plot the histogram of the image.
        """
        plt.figure(figsize=(8, 8))
        plt.hist(self.ravel(), bins=256)
        plt.show()

    def convex_hull(self, binary_threshold):
        """
        Find the convex hull of the image.

        @param binary_threshold: threshold to use for binarizing the image
        @return: image with convex hull drawn on it
        """
        binary = self.as_binary(binary_threshold).image
        hull = skimage.morphology.convex_hull_image(binary)
        return Image(hull)

    def canny_edge_detection(self, sigma=1):
        """
        Perform canny edge detection on the image.

        @param sigma: standard deviation of the Gaussian filter
        @return: image with edges drawn on it
        """
        edges = skimage.feature.canny(self.image, sigma=sigma)
        return Image(edges)

    def draw_line(self, y0, x0, y1, x1):
        """
        Draw a line on the image.

        @param y0: y coordinate of the first point
        @param x0: x coordinate of the first point
        @param y1: y coordinate of the second point
        @param x1: x coordinate of the second point
        @return: image with line drawn on it
        """
        line = skimage.draw.line(y0, x0, y1, x1)
        self.image[line] = 1
        return self

    def draw_polygon(self, points):
        """
        Draw a polygon on the image.
        Points = [[x0, y0], [x1, y1], ...]

        @param points: list of polygon vertices
        @return: image with polygon drawn on it
        """
        polygon = skimage.draw.polygon(points[:, 1], points[:, 0])
        self.image[polygon] = 1
        return self

    def draw_circle(self, x, y, radius):
        """
        Draw a circle on the image.

        @param x: x coordinate of the center
        @param y: y coordinate of the center
        @param radius: radius of the circle
        @return: image with circle drawn on it
        """
        circle = skimage.draw.disk((y, x), radius, shape=self.image.shape)
        self.image[circle] = 1
        return self

    def skeletonize(self):
        """
        Skeletonize the image.

        @return: skeletonized image
        """
        skeleton = skimage.morphology.skeletonize(self.image)
        return Image(skeleton)

    def sobel(self):
        """
        Perform sobel edge detection on the image.

        @return: image with edges drawn on it
        """
        edges = skimage.filters.sobel(self.image)
        return Image(edges)

    def threshold_multiotsu(self, classes=3, nbins=256):
        """
        Perform multiotsu thresholding on the image.

        @return: image with thresholded pixels drawn on it
        """
        thresholds = skimage.filters.threshold_multiotsu(self.image, classes=classes, nbins=nbins)
        thresholded = np.digitize(self.image, bins=thresholds)
        return Image(thresholded)

class RGB_Image(Image):
    """
    RGB_Image class.
    """

    @classmethod
    def from_generic_image(cls, image):
        """
        Create an RGB_Image object from a generic Image object.

        @param image: generic Image object
        @return: RGB_Image object
        """
        return cls(image.image)

    def as_grayscale(self):
        """
        Return the image as a grayscale image.

        @return: grayscale image as generic Image object
        """
        return Image(skimage.color.rgb2gray(self.image))

    def as_binary(self, threshold=0.5):
        """
        Return the image as a binary image. Casts to grayscale first.

        @param threshold: threshold to use for binarizing the image
        @return: binary image as generic Image object
        """
        return Image.as_binary(self.as_grayscale(), threshold)             

    def contours(self, level):
        """
        Find contours in the image. Casts to grayscale first.

        @param level: level to use for contouring
        """
        Image.contours(self.as_grayscale(), level)

    def canny_edge_detection(self, sigma=1):
        """
        Perform canny edge detection on the image. Casts to grayscale first.

        @param sigma: standard deviation of the Gaussian filter
        @return: image with edges drawn on it
        """
        return Image.canny_edge_detection(self.as_grayscale(), sigma)

    def plot_histogram(self):
        """
        Plot the histogram of the image. Casts to grayscale first.
        """
        Image.plot_histogram(self.as_grayscale())

    def rotate(self, angle):
        """
        Rotate the image by the given angle.

        @param angle: angle to rotate by
        @return: rotated image as RGB_Image object
        """
        return self.from_generic_image( # return as RGB_Image
            super().rotate(angle)
        )

    def draw_line(self, y0, x0, y1, x1, color=(0, 0, 0)):
        """
        Draw a line on the image.

        @param y0: y coordinate of the first point
        @param x0: x coordinate of the first point
        @param y1: y coordinate of the second point
        @param x1: x coordinate of the second point
        @param color: color of the line
        @return: image with line drawn on it
        """
        line = skimage.draw.line(y0, x0, y1, x1)
        self.image[line] = color
        return self

    def draw_polygon(self, points, color=(0, 0, 0)):
        """
        Draw a polygon on the image.
        Points = [[x0, y0], [x1, y1], ...]

        @param points: list of polygon vertices
        @param color: color of the polygon
        @return: image with polygon drawn on it
        """
        polygon = skimage.draw.polygon(points[:, 1], points[:, 0])
        self.image[polygon] = color
        return self
        
    def draw_circle(self, x, y, radius, color=(0, 0, 0)):
        """
        Draw a circle on the image.

        @param x: x coordinate of the center
        @param y: y coordinate of the center
        @param radius: radius of the circle
        @param color: color of the circle
        @return: image with circle drawn on it
        """
        circle = skimage.draw.disk((y, x), radius, shape=self.image.shape)
        self.image[circle] = color
        return self

    def skeletonize(self):
        """
        Skeletonize the image.

        @return: skeletonized image as RGB_Image object
        """
        return self.as_binary().skeletonize()

    def sobel(self):
        """
        Perform sobel edge detection on the image.

        @return: image with edges drawn on it
        """
        return self.as_grayscale().sobel()

    def threshold_multiotsu(self, classes=3, nbins=256):
        return self.as_grayscale().threshold_multiotsu(classes, nbins)


class ImageCollection:
    """
    ImageCollection class.
    """

    def __init__(self, images):
        """
        Initialize the ImageCollection object.

        @param images: list of Image objects
        """
        self.images = images

    def __getitem__(self, key):
        """
        Get an image from the collection.

        @param key: index of the image
        @return: Image object
        """
        return self.images[key]

    def __setitem__(self, key, value):
        """
        Set an image in the collection.

        @param key: index of the image
        @param value: Image object
        """
        self.images[key] = value

    def __len__(self):
        """
        Get the number of images in the collection.

        @return: number of images in the collection
        """
        return len(self.images)

    def __iter__(self):
        """
        Iterate over the images in the collection.

        @return: iterator over the images in the collection
        """
        return iter(self.images)

    def __repr__(self):
        """
        Get the string representation of the ImageCollection object.

        @return: string representation of the ImageCollection object
        """
        return f"ImageCollection with {len(self)} images"

    def __str__(self):
        """
        Get the string representation of the ImageCollection object.

        @return: string representation of the ImageCollection object
        """
        return self.__repr__()

    def __add__(self, other):
        """
        Add two ImageCollection objects together.

        @param other: ImageCollection object to add to this one
        @return: ImageCollection object with the images from both collections
        """
        return ImageCollection(self.images + other.images)

    @classmethod
    def from_directory(cls, directory):
        """
        Create an ImageCollection object from a directory.

        @param directory: directory to load images from
        @return: ImageCollection object
        """
        images = []
        for filename in os.listdir(directory):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                images.append(new_image_from_file(os.path.join(directory, filename)))
        return cls(images)

    def save_to_directory(self, directory, output_name=None):
        """
        Save the images in the collection to a directory.

        @param directory: directory to save images to
        """
        if output_name is None:
            output_name = 'output'
        
        if not os.path.isdir(directory):
            os.mkdir(directory)

        for i, image in enumerate(self.images):
            image.save(os.path.join(directory, f'{output_name}_{i}.png'))