import cv2
import numpy as np

# wczytanie obrazu
img = cv2.imread('D:\Programowanie\Python\image.png', 0)

# określenie kernela
kernel = np.ones((5, 5), np.uint8)

# zastosowanie dylatacji z wykorzystaniem kernela
dilation = cv2.dilate(img, kernel, iterations=8)

# wyświetlenie obrazów przed i po dylatacji
cv2.imshow('Original Image', img)
cv2.imshow('Dilation', dilation)
cv2.waitKey(0)
cv2.destroyAllWindows()