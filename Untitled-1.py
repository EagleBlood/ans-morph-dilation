import cv2
import numpy as np

# wczytanie obrazu
img = cv2.imread(r'ertka.bmp', 0)

dimensions = img.shape
height, width = img.shape[:2]

# konwersja trybu kolorów na 3 kanały
img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

# określenie kernela
kernel = np.ones((3, 3), np.uint8)

# zastosowanie filtru maksymalnego z wykorzystaniem kernela
dilation = cv2.dilate(img, kernel, iterations=1)

# dodanie marginesów między obrazami
img = cv2.copyMakeBorder(img, 0, 0, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))
dilation = cv2.copyMakeBorder(dilation, 0, 0, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))

# utworzenie obrazu szarego jako tła okna
background = np.zeros((height*2, width*3, 3), dtype=np.uint8)
background[:] = (128, 128, 128)

# dodanie opisu na górze obrazów
cv2.putText(background, "Image 1", (80, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(background, "Image 2", (500, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

# umieszczenie obrazów na tle
background[50:height+50, 50:width+50] = img
background[50:height+50, 150+width:150+(2*width)] = dilation

# wyświetlenie obrazów przed i po dylatacji
cv2.imshow('Result', background)
cv2.waitKey(0)
cv2.destroyAllWindows()