import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread('cv_lab_image.jpeg')


def brightness_adjustment(image, value):
    adjusted_image = np.clip(image.astype(int) + value, 0, 255).astype(np.uint8)
    return adjusted_image


RGB_TO_GRAYSCALE_COEFFICIENTS = np.array([0.2989, 0.5870, 0.1140])


def grayscale(image):
    gray_image = np.dot(image[..., :3], RGB_TO_GRAYSCALE_COEFFICIENTS)
    return np.dstack([gray_image] * 3).astype(np.uint8)


def negative(image):
    return 255 - image


SEPIA_FILTER_COEFFICIENTS = np.array([
    [0.393, 0.769, 0.189],
    [0.349, 0.686, 0.168],
    [0.272, 0.534, 0.131]
])


def sepia_gradient(image):
    sepia_image = np.dot(image, SEPIA_FILTER_COEFFICIENTS.T)
    height, width = image.shape[:2]
    X, Y = np.meshgrid(np.arange(width), np.arange(height))
    distance_from_center = np.sqrt((X - width / 2) ** 2 + (Y - height / 2) ** 2)
    gradient_to_center = distance_from_center / distance_from_center.max()
    gradient_from_center = 1 - gradient_to_center

    sepia_gradient_image = sepia_image * gradient_from_center[:, :, np.newaxis] + image * gradient_to_center[:, :, np.newaxis]
    return sepia_gradient_image.astype(np.uint8)


brightened_image = brightness_adjustment(image, 70)
grayscale_image = grayscale(image)
negative_image = negative(image)
sepia_gradient_image = sepia_gradient(image)

def show_image_with_matplotlib(img, title):
    # Convert BGR image to RGB
    img_RGB = img[:, :, ::-1]
    plt.imshow(img_RGB)
    plt.title(title)
    plt.axis('off')

plt.figure(figsize=(20, 10))

plt.subplot(151), show_image_with_matplotlib(image, 'Original Image')
plt.subplot(152), show_image_with_matplotlib(brightened_image, 'Brightened Image')
plt.subplot(153), show_image_with_matplotlib(grayscale_image, 'Grayscale Image')
plt.subplot(154), show_image_with_matplotlib(negative_image, 'Negative Image')
plt.subplot(155), show_image_with_matplotlib(sepia_gradient_image, 'Sepia Gradient Image')

plt.show()
