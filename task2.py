import cv2
import matplotlib.pyplot as plt

image = cv2.imread('cv_lab_image.jpeg')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

blurred = cv2.GaussianBlur(gray, (5, 5), 0)

edges = cv2.Canny(blurred, 50, 150)

contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

countrered = cv2.drawContours(image, contours, -1, (0, 255, 0), 2)


def show_image_with_matplotlib(img, title):
    # Convert BGR image to RGB
    img_RGB = img[:, :, ::-1]
    plt.imshow(img_RGB)
    plt.title(title)
    plt.axis('off')

plt.figure(figsize=(20, 10))

plt.subplot(151), show_image_with_matplotlib(cv2.imread('cv_lab_image.jpeg'), 'Original')
plt.subplot(152), show_image_with_matplotlib(countrered, 'Contours Applied')

plt.show()
