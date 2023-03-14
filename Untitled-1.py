import cv2
import numpy as np

# wczytanie obrazu
img = cv2.imread(r'test.png', 0)
img = cv2.resize(img, (400, 400))

# konwersja trybu kolorów na 3 kanały
img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

# określenie kernela
kernel = np.ones((5, 5), np.uint8)

# zastosowanie dylatacji z wykorzystaniem kernela
dilation = cv2.dilate(img, kernel, iterations=8)

# dodanie marginesów między obrazami
img = cv2.copyMakeBorder(img, 0, 0, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))
dilation = cv2.copyMakeBorder(dilation, 0, 0, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))

# utworzenie obrazu szarego jako tła okna
background = np.zeros((500, 880, 3), dtype=np.uint8)  #trzeba zmieniać 880 żeby dostosować tablice, czemu nie wiem ale nie ma wyjścia xd
background[:] = (128, 128, 128)

# dodanie opisu na górze obrazów
cv2.putText(background, "Image 1", (80, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(background, "Image 2", (500, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

# umieszczenie obrazów na tle
background[50:450, 50:450] = img
background[50:450, 470:870] = dilation

# wyświetlenie obrazów przed i po dylatacji
cv2.imshow('Result', background)
cv2.waitKey(0)
cv2.destroyAllWindows()


